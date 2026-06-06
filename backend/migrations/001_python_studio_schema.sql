-- Unified Python Learning Studio schema extensions
-- Adds code execution columns, code_submissions, and snippets tables

ALTER TABLE questions
  ADD COLUMN IF NOT EXISTS starter_code       TEXT,
  ADD COLUMN IF NOT EXISTS expected_output    TEXT,
  ADD COLUMN IF NOT EXISTS expected_output_type VARCHAR(20) DEFAULT 'exact',
  ADD COLUMN IF NOT EXISTS run_in_browser     BOOLEAN DEFAULT TRUE,
  ADD COLUMN IF NOT EXISTS time_limit_ms      INTEGER DEFAULT 5000,
  ADD COLUMN IF NOT EXISTS test_cases         JSONB,
  ADD COLUMN IF NOT EXISTS pep8_required      BOOLEAN DEFAULT FALSE;

CREATE TABLE IF NOT EXISTS code_submissions (
  id                SERIAL PRIMARY KEY,
  user_id           UUID NOT NULL REFERENCES users(id),
  question_id       INTEGER NOT NULL REFERENCES questions(id),
  submitted_code    TEXT NOT NULL,
  actual_output     TEXT,
  is_correct        BOOLEAN,
  pep8_score        INTEGER,
  execution_time_ms INTEGER,
  error_message     TEXT,
  submitted_at      TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS snippets (
  id          SERIAL PRIMARY KEY,
  title       VARCHAR(200) NOT NULL,
  slug        VARCHAR(200) UNIQUE,
  description TEXT,
  code        TEXT NOT NULL,
  module_id   INTEGER REFERENCES topics(id),
  tags        TEXT[],
  difficulty  VARCHAR(20),
  is_featured BOOLEAN DEFAULT FALSE,
  created_at  TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_code_submissions_user_id ON code_submissions(user_id);
CREATE INDEX IF NOT EXISTS idx_code_submissions_question_id ON code_submissions(question_id);
CREATE INDEX IF NOT EXISTS idx_snippets_module_id ON snippets(module_id);
CREATE INDEX IF NOT EXISTS idx_snippets_slug ON snippets(slug);
