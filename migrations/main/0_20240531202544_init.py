from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "cities" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "manufacturers" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "year_of_creation" INT NOT NULL,
    "city_id" INT REFERENCES "cities" ("id") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "beer" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "style" VARCHAR(255),
    "abv" DOUBLE PRECISION,
    "plato" DOUBLE PRECISION,
    "ibu" DOUBLE PRECISION,
    "manufacturer_id" INT REFERENCES "manufacturers" ("id") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(20),
    "first_name" VARCHAR(255) NOT NULL,
    "last_name" VARCHAR(255),
    "birthday" DATE,
    "reg_date" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "creds" (
    "login" VARCHAR(255) NOT NULL,
    "passwd" VARCHAR(60) NOT NULL,
    "user_id" INT NOT NULL  PRIMARY KEY REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "review" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "review" TEXT,
    "rating" INT NOT NULL,
    "beer_id" INT REFERENCES "beer" ("id") ON DELETE CASCADE,
    "user_id" INT REFERENCES "user" ("id") ON DELETE SET NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
