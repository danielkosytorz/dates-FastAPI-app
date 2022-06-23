-- upgrade --
CREATE TABLE IF NOT EXISTS "date" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "month" INT NOT NULL,
    "day" INT NOT NULL,
    "fact" VARCHAR(300) NOT NULL,
    CONSTRAINT "uid_date_month_57e7c4" UNIQUE ("month", "day")
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
