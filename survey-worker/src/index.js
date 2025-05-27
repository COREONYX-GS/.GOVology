/**
 * Welcome to Cloudflare Workers! This is your first worker.
 *
 * - Run `npm run dev` in your terminal to start a development server
 * - Open a browser tab at http://localhost:8787/ to see your worker in action
 * - Run `npm run deploy` to publish your worker
 *
 * Learn more at https://developers.cloudflare.com/workers/
 */
function parseCookies(header) {
  const cookies = {};
  if (!header) return cookies;
  header.split(';').forEach(part => {
    const [key, ...v] = part.split('=');
    cookies[key.trim()] = v.join('=').trim();
  });
  return cookies;
}

function cookieHeader(name, value, opts = {}) {
  let cookie = `${name}=${value}`;
  if (opts.path) cookie += `; Path=${opts.path}`;
  if (opts.maxAge !== undefined) cookie += `; Max-Age=${opts.maxAge}`;
  if (opts.httpOnly) cookie += '; HttpOnly';
  if (opts.sameSite) cookie += `; SameSite=${opts.sameSite}`;
  return cookie;
}

export default {
	async fetch(request, env, ctx) {
		const url = new URL(request.url);
		const cookies = parseCookies(request.headers.get('Cookie'));
		let sessionId = cookies['session_id'];

		if (request.method.toUpperCase() === "GET" && url.pathname === "/") { 

			try {
				const htmlContent = await env.ASSETS.fetch('https://assets.local/index.html');

				return new Response(await htmlContent.text(), {
					headers: { "Content-Type": "text/html" },
				});
			} catch (err) {
				console.log({ "message": "Error reading the HTML file", "error": err });
				return new Response("Error loading the survey.", { status: 500 });
			}

		} // end if GET '/'
		else if (request.method.toUpperCase() === "GET" && url.pathname === "/logout") {
			return Response.redirect(url.origin + '/', 302, {
				headers: {
					"Set-Cookie": cookieHeader('session_id', '', { path: '/', maxAge: 0 })
				}
			});
		} // end if GET '/logout'
		else if (request.method.toUpperCase() === "GET" && url.pathname === "/votes") {
						
			const sql = `SELECT domain, votes_y, votes_n FROM votes ORDER BY domain;`;
			const { results } = await env.DB.prepare(sql).all();
			
			return new Response( JSON.stringify(results, null, 2),
								{ status: 200, headers: { "Content-Type": "application/json" } } );

		} // end if GET '/votes' for stats
		else if (request.method.toUpperCase() === "POST" && url.pathname === "/vote") {
			console.log("Processing vote request...");
			const voteData = await request.json();
			try {
				
				console.log("Vote Data Received:", voteData);

				try { // Insert or update the vote in the database
					const domain = voteData['domain'];
					const vote = voteData['vote']; 
					
					if (!domain || typeof domain !== "string" || !(vote === true || vote === false)) {
						throw new Error("Invalid vote data");
					}
					else {
						const voteY = vote ? 1 : 0;
    					const voteN = vote ? 0 : 1;
						
						const sql = `
							INSERT INTO votes(domain, votes_y, votes_n)
							VALUES (?, ?, ?)
							ON CONFLICT(domain) DO UPDATE
								SET
								votes_y = votes_y + excluded.votes_y,
								votes_n = votes_n + excluded.votes_n
							RETURNING votes_y, votes_n;
							`;
						const { results } = await env.DB.prepare(sql)
      													.bind(domain, voteY, voteN)
      													.all();
						
						return new Response(
								JSON.stringify({ domain: domain, yourVote: vote, result: results[0] }, null, 2),
								{ status: 200, headers: { "Content-Type": "application/json" } } );
					}
				} catch (err) {
					console.log({ "message": "Error processing the vote", "error": err });
					return new Response("Error processing the vote request.", { status: 500 });
				}

			} catch (err) {
				console.log({ "message": "Error processing the vote", "data": voteData, "error": err });
				return new Response("Error processing the vote.", { status: 500 });
			}
		}
		else if (request.method.toUpperCase() === "POST" && url.pathname === "/survey") {
			if (!sessionId) {
				sessionId = crypto.randomUUID();
			}

			try {
				const formData = await request.formData();
				const surveyData = Object.fromEntries(formData.entries());

				// Here you would typically process the survey data, e.g., save it to a database
				console.log("Survey Data Received:", surveyData);

				return new Response( JSON.stringify( { data: surveyData, cookies: cookies }, null, 2), {
						status: 200, headers: { "Content-Type": "application/json",  //for MaxAge - One Day in seconds is: 86400
												'Set-Cookie': cookieHeader('session_id', sessionId, { path: '/', maxAge: 300 }) } }
				);
			} catch (err) {
				console.log({ "message": "Error processing the survey request", "error": err });
				return new Response("Error processing the survey request.", { status: 500 });
			}

		} // end if POST '/survey' - this is how we start the survey
		else {
			console.log("Unhandled request method or path:", request.method, url.pathname);
			return new Response("Not Found", { status: 404 });
		}
	}
};
