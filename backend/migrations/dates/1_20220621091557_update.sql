-- upgrade --
CREATE TABLE IF NOT EXISTS "popularmonth" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "month" INT NOT NULL UNIQUE,
    "days_checked" INT NOT NULL  DEFAULT 0
);
-- downgrade --
DROP TABLE IF EXISTS "popularmonth";
