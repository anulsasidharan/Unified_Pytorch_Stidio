-- CreateEnum
CREATE TYPE "LearningLevel" AS ENUM ('beginner', 'intermediate', 'advanced');

-- CreateEnum
CREATE TYPE "Difficulty" AS ENUM ('basic', 'intermediate', 'advanced');

-- CreateEnum
CREATE TYPE "AttemptStatus" AS ENUM ('accepted', 'wrong_answer', 'time_limit', 'runtime_error', 'incomplete');

-- CreateEnum
CREATE TYPE "ProgressStatus" AS ENUM ('not_attempted', 'attempted', 'solved', 'mastered');

-- CreateEnum
CREATE TYPE "QuestionSource" AS ENUM ('internal', 'leetcode', 'hackerrank', 'codeforces', 'interview', 'custom');

-- CreateEnum
CREATE TYPE "ImportMethod" AS ENUM ('manual', 'csv', 'json', 'url');

-- CreateTable
CREATE TABLE "users" (
    "user_id" TEXT NOT NULL,
    "username" VARCHAR(50) NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "password_hash" VARCHAR(255) NOT NULL,
    "full_name" VARCHAR(100),
    "avatar_url" TEXT,
    "learning_level" "LearningLevel" NOT NULL DEFAULT 'beginner',
    "target_goal" TEXT,
    "daily_target" INTEGER NOT NULL DEFAULT 3,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "last_active" TIMESTAMP(3),
    "total_questions_solved" INTEGER NOT NULL DEFAULT 0,
    "current_streak" INTEGER NOT NULL DEFAULT 0,
    "longest_streak" INTEGER NOT NULL DEFAULT 0,

    CONSTRAINT "users_pkey" PRIMARY KEY ("user_id")
);

-- CreateTable
CREATE TABLE "topics" (
    "topic_id" TEXT NOT NULL,
    "topic_name" VARCHAR(100) NOT NULL,
    "slug" VARCHAR(100) NOT NULL,
    "category" VARCHAR(50),
    "description" TEXT,
    "difficulty_level" "Difficulty" NOT NULL,
    "prerequisites" JSONB NOT NULL DEFAULT '[]',
    "total_questions" INTEGER NOT NULL DEFAULT 0,
    "icon_url" TEXT,
    "order_index" INTEGER,
    "is_active" BOOLEAN NOT NULL DEFAULT true,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "topics_pkey" PRIMARY KEY ("topic_id")
);

-- CreateTable
CREATE TABLE "questions" (
    "question_id" TEXT NOT NULL,
    "topic_id" TEXT NOT NULL,
    "title" VARCHAR(255) NOT NULL,
    "slug" VARCHAR(255) NOT NULL,
    "description" TEXT NOT NULL,
    "difficulty" "Difficulty" NOT NULL,
    "constraints" TEXT,
    "input_format" TEXT,
    "output_format" TEXT,
    "time_complexity" VARCHAR(50),
    "space_complexity" VARCHAR(50),
    "hints" JSONB NOT NULL DEFAULT '[]',
    "tags" JSONB NOT NULL DEFAULT '[]',
    "source" "QuestionSource" NOT NULL DEFAULT 'internal',
    "source_url" TEXT,
    "is_premium" BOOLEAN NOT NULL DEFAULT false,
    "acceptance_rate" DECIMAL(5,2),
    "total_attempts" INTEGER NOT NULL DEFAULT 0,
    "total_solved" INTEGER NOT NULL DEFAULT 0,
    "created_by" TEXT,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,
    "is_active" BOOLEAN NOT NULL DEFAULT true,

    CONSTRAINT "questions_pkey" PRIMARY KEY ("question_id")
);

-- CreateTable
CREATE TABLE "test_cases" (
    "test_case_id" TEXT NOT NULL,
    "question_id" TEXT NOT NULL,
    "input" TEXT NOT NULL,
    "expected_output" TEXT NOT NULL,
    "explanation" TEXT,
    "is_sample" BOOLEAN NOT NULL DEFAULT false,
    "is_hidden" BOOLEAN NOT NULL DEFAULT false,
    "order_index" INTEGER,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "test_cases_pkey" PRIMARY KEY ("test_case_id")
);

-- CreateTable
CREATE TABLE "solutions" (
    "solution_id" TEXT NOT NULL,
    "question_id" TEXT NOT NULL,
    "language" VARCHAR(30) NOT NULL,
    "approach_name" VARCHAR(100),
    "code" TEXT NOT NULL,
    "explanation" TEXT,
    "time_complexity" VARCHAR(50),
    "space_complexity" VARCHAR(50),
    "is_optimal" BOOLEAN NOT NULL DEFAULT false,
    "created_by" TEXT,
    "upvotes" INTEGER NOT NULL DEFAULT 0,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "solutions_pkey" PRIMARY KEY ("solution_id")
);

-- CreateTable
CREATE TABLE "user_attempts" (
    "attempt_id" TEXT NOT NULL,
    "user_id" TEXT NOT NULL,
    "question_id" TEXT NOT NULL,
    "language" VARCHAR(30),
    "submitted_code" TEXT,
    "status" "AttemptStatus" NOT NULL,
    "test_cases_passed" INTEGER NOT NULL DEFAULT 0,
    "total_test_cases" INTEGER,
    "execution_time" DECIMAL(10,2),
    "memory_used" DECIMAL(10,2),
    "attempted_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "notes" TEXT,
    "is_bookmarked" BOOLEAN NOT NULL DEFAULT false,
    "difficulty_rating" INTEGER,

    CONSTRAINT "user_attempts_pkey" PRIMARY KEY ("attempt_id")
);

-- CreateTable
CREATE TABLE "user_progress" (
    "progress_id" TEXT NOT NULL,
    "user_id" TEXT NOT NULL,
    "question_id" TEXT NOT NULL,
    "topic_id" TEXT NOT NULL,
    "status" "ProgressStatus" NOT NULL DEFAULT 'not_attempted',
    "first_attempt_date" TIMESTAMP(3),
    "last_attempt_date" TIMESTAMP(3),
    "solved_date" TIMESTAMP(3),
    "total_attempts" INTEGER NOT NULL DEFAULT 0,
    "time_spent_minutes" INTEGER NOT NULL DEFAULT 0,
    "best_execution_time" DECIMAL(10,2),
    "need_revision" BOOLEAN NOT NULL DEFAULT false,
    "next_revision_date" TIMESTAMP(3),
    "revision_count" INTEGER NOT NULL DEFAULT 0,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "user_progress_pkey" PRIMARY KEY ("progress_id")
);

-- CreateTable
CREATE TABLE "daily_activity" (
    "activity_id" TEXT NOT NULL,
    "user_id" TEXT NOT NULL,
    "activity_date" DATE NOT NULL,
    "questions_attempted" INTEGER NOT NULL DEFAULT 0,
    "questions_solved" INTEGER NOT NULL DEFAULT 0,
    "time_spent_minutes" INTEGER NOT NULL DEFAULT 0,
    "topics_covered" JSONB NOT NULL DEFAULT '[]',
    "streak_day" INTEGER,
    "daily_goal_met" BOOLEAN NOT NULL DEFAULT false,
    "notes" TEXT,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "daily_activity_pkey" PRIMARY KEY ("activity_id")
);

-- CreateTable
CREATE TABLE "revision_queue" (
    "queue_id" TEXT NOT NULL,
    "user_id" TEXT NOT NULL,
    "question_id" TEXT NOT NULL,
    "scheduled_date" DATE NOT NULL,
    "priority" INTEGER NOT NULL DEFAULT 1,
    "reason" VARCHAR(50),
    "completed" BOOLEAN NOT NULL DEFAULT false,
    "completed_at" TIMESTAMP(3),
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "revision_queue_pkey" PRIMARY KEY ("queue_id")
);

-- CreateTable
CREATE TABLE "user_notes" (
    "note_id" TEXT NOT NULL,
    "user_id" TEXT NOT NULL,
    "question_id" TEXT NOT NULL,
    "note_text" TEXT NOT NULL,
    "is_pinned" BOOLEAN NOT NULL DEFAULT false,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "user_notes_pkey" PRIMARY KEY ("note_id")
);

-- CreateTable
CREATE TABLE "custom_questions" (
    "custom_question_id" TEXT NOT NULL,
    "user_id" TEXT NOT NULL,
    "question_id" TEXT NOT NULL,
    "source_name" VARCHAR(100),
    "source_url" TEXT,
    "import_method" "ImportMethod" NOT NULL,
    "original_content" JSONB,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "custom_questions_pkey" PRIMARY KEY ("custom_question_id")
);

-- CreateIndex
CREATE UNIQUE INDEX "users_username_key" ON "users"("username");

-- CreateIndex
CREATE UNIQUE INDEX "users_email_key" ON "users"("email");

-- CreateIndex
CREATE UNIQUE INDEX "topics_topic_name_key" ON "topics"("topic_name");

-- CreateIndex
CREATE UNIQUE INDEX "topics_slug_key" ON "topics"("slug");

-- CreateIndex
CREATE INDEX "topics_category_idx" ON "topics"("category");

-- CreateIndex
CREATE INDEX "topics_difficulty_level_idx" ON "topics"("difficulty_level");

-- CreateIndex
CREATE UNIQUE INDEX "questions_slug_key" ON "questions"("slug");

-- CreateIndex
CREATE INDEX "questions_topic_id_idx" ON "questions"("topic_id");

-- CreateIndex
CREATE INDEX "questions_difficulty_idx" ON "questions"("difficulty");

-- CreateIndex
CREATE INDEX "questions_slug_idx" ON "questions"("slug");

-- CreateIndex
CREATE INDEX "user_attempts_user_id_question_id_idx" ON "user_attempts"("user_id", "question_id");

-- CreateIndex
CREATE INDEX "user_attempts_attempted_at_idx" ON "user_attempts"("attempted_at" DESC);

-- CreateIndex
CREATE UNIQUE INDEX "user_attempts_user_id_question_id_attempted_at_key" ON "user_attempts"("user_id", "question_id", "attempted_at");

-- CreateIndex
CREATE INDEX "user_progress_user_id_status_idx" ON "user_progress"("user_id", "status");

-- CreateIndex
CREATE INDEX "user_progress_user_id_topic_id_idx" ON "user_progress"("user_id", "topic_id");

-- CreateIndex
CREATE UNIQUE INDEX "user_progress_user_id_question_id_key" ON "user_progress"("user_id", "question_id");

-- CreateIndex
CREATE INDEX "daily_activity_user_id_activity_date_idx" ON "daily_activity"("user_id", "activity_date");

-- CreateIndex
CREATE UNIQUE INDEX "daily_activity_user_id_activity_date_key" ON "daily_activity"("user_id", "activity_date");

-- CreateIndex
CREATE INDEX "revision_queue_user_id_scheduled_date_idx" ON "revision_queue"("user_id", "scheduled_date");

-- CreateIndex
CREATE UNIQUE INDEX "revision_queue_user_id_question_id_scheduled_date_key" ON "revision_queue"("user_id", "question_id", "scheduled_date");

-- AddForeignKey
ALTER TABLE "questions" ADD CONSTRAINT "questions_topic_id_fkey" FOREIGN KEY ("topic_id") REFERENCES "topics"("topic_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "questions" ADD CONSTRAINT "questions_created_by_fkey" FOREIGN KEY ("created_by") REFERENCES "users"("user_id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "test_cases" ADD CONSTRAINT "test_cases_question_id_fkey" FOREIGN KEY ("question_id") REFERENCES "questions"("question_id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "solutions" ADD CONSTRAINT "solutions_question_id_fkey" FOREIGN KEY ("question_id") REFERENCES "questions"("question_id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "solutions" ADD CONSTRAINT "solutions_created_by_fkey" FOREIGN KEY ("created_by") REFERENCES "users"("user_id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "user_attempts" ADD CONSTRAINT "user_attempts_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("user_id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "user_attempts" ADD CONSTRAINT "user_attempts_question_id_fkey" FOREIGN KEY ("question_id") REFERENCES "questions"("question_id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "user_progress" ADD CONSTRAINT "user_progress_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("user_id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "user_progress" ADD CONSTRAINT "user_progress_question_id_fkey" FOREIGN KEY ("question_id") REFERENCES "questions"("question_id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "user_progress" ADD CONSTRAINT "user_progress_topic_id_fkey" FOREIGN KEY ("topic_id") REFERENCES "topics"("topic_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "daily_activity" ADD CONSTRAINT "daily_activity_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("user_id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "revision_queue" ADD CONSTRAINT "revision_queue_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("user_id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "revision_queue" ADD CONSTRAINT "revision_queue_question_id_fkey" FOREIGN KEY ("question_id") REFERENCES "questions"("question_id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "user_notes" ADD CONSTRAINT "user_notes_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("user_id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "user_notes" ADD CONSTRAINT "user_notes_question_id_fkey" FOREIGN KEY ("question_id") REFERENCES "questions"("question_id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "custom_questions" ADD CONSTRAINT "custom_questions_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("user_id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "custom_questions" ADD CONSTRAINT "custom_questions_question_id_fkey" FOREIGN KEY ("question_id") REFERENCES "questions"("question_id") ON DELETE CASCADE ON UPDATE CASCADE;
