-- SQLite schema for AI assistant audit trail (requirement.md §2.2)

CREATE TABLE IF NOT EXISTS ai_requests (
    id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    user_prompt TEXT NOT NULL,
    model TEXT,
    explanation TEXT,
    generated_code TEXT,
    raw_model_response TEXT
);

CREATE TABLE IF NOT EXISTS executions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    final_code TEXT NOT NULL,
    status TEXT NOT NULL,
    stdout TEXT,
    stderr TEXT,
    duration_ms INTEGER,
    output_paths TEXT,
    FOREIGN KEY (request_id) REFERENCES ai_requests(id)
);

CREATE INDEX IF NOT EXISTS idx_executions_request_id ON executions(request_id);
CREATE INDEX IF NOT EXISTS idx_ai_requests_created ON ai_requests(created_at DESC);
