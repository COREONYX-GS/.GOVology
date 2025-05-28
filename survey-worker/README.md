# Worker

This directory contains a Cloudflare Worker for voting on `.gov` domains.

## Commands

The following wrangler commands assume that the [`wrangler`](https://developers.cloudflare.com/workers/wrangler/) CLI is installed and authenticated.

```bash
# Create the D1 database and apply the initial schema
wrangler d1 create govology
wrangler d1 migrations apply govology ## Note: not clear if this works
npx wrangler d1 execute govology --local --file="./migrations/0001_init.sql"
npx wrangler d1 execute govology --local --command="DROP table votes"
npx wrangler d1 execute govology --remote --file="./migrations/0002_init.sql"
npx wrangler d1 execute govology --remote --command="SELECT * from user"

# Test the database exists, --local can be swapped with --remote
 npx wrangler d1 execute govology --local --command="SELECT * from votes"

# Dump data to CSV
wrangler d1 execute govology --remote \
  --command "SELECT * FROM votes" \
  --output csv > domain_votes_dump.csv
```

## Binding

Don't forget to bind the database in your `wrangler.jsonc` file, something like:

```
     "d1_databases": [
       {
         "binding": "DB",
         "database_name": "govology",
         "database_id": "<uniqie-ID-for-the-database>"
       }
     ],
     ```

## Endpoints

After deploying the worker, the following endpoints are available:

- `GET /domains.json` – returns all domain records as JSON.
- `GET /domains.csv` – returns all domain records as CSV.
- `POST /admin/init` – creates the table if it does not already exist.
- `POST /admin/load` – accepts the contents of `federal-domains.csv` and populates the table.