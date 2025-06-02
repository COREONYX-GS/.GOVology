CREATE TABLE IF NOT EXISTS votes (
  domain TEXT PRIMARY KEY,
  votes_y INTEGER DEFAULT 0,
  votes_n INTEGER DEFAULT 0
);

DROP TABLE IF EXISTS user_votes;

CREATE TABLE IF NOT EXISTS user_votes (
  session_id TEXT PRIMARY KEY,
  domain TEXT,
  vote BOOLEAN
);