/**
 * Welcome to Cloudflare Workers! This is your first worker.
 *
 * - Run `npm run dev` in your terminal to start a development server
 * - Open a browser tab at http://localhost:8787/ to see your worker in action
 * - Run `npm run deploy` to publish your worker
 *
 * Learn more at https://developers.cloudflare.com/workers/
 */

export default {
	async fetch(request, env, ctx) {
		const url = new URL(request.url);
		console.log("URL PATH:", url.pathname);
		console.log("FETCH REQUEST:", request.method, request.url);

		if (request.method.toUpperCase() === "GET" && url.pathname === "/") { 

			try {
				const htmlContent = await env.ASSETS.fetch('https://assets.local/survey.html');

				return new Response(await htmlContent.text(), {
					headers: { "Content-Type": "text/html" },
				});
			} catch (err) {
				console.log({ "message": "Error reading the HTML file", "error": err });
				return new Response("Error loading the survey.", { status: 500 });
			}

		} // end if GET '/'
	},
};
