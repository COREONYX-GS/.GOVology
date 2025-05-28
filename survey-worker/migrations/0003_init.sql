CREATE TABLE IF NOT EXISTS votes (
  domain TEXT PRIMARY KEY,
  votes_y INTEGER DEFAULT 0,
  votes_n INTEGER DEFAULT 0
);

DROP TABLE IF EXISTS votes_by_user;

CREATE TABLE IF NOT EXISTS votes_by_user (
  session_id TEXT NOT NULL,
  domain TEXT NOT NULL,
  vote INTEGER NOT NULL CHECK (vote IN (0, 1)),
  PRIMARY KEY (session_id, domain)
);
