from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "creds" DROP COLUMN "login";
        ALTER TABLE "user" ALTER COLUMN "first_name" DROP NOT NULL;
        ALTER TABLE "user" ALTER COLUMN "username" SET NOT NULL;
        CREATE UNIQUE INDEX "uid_user_usernam_9987ab" ON "user" ("username");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "idx_user_usernam_9987ab";
        ALTER TABLE "user" ALTER COLUMN "first_name" SET NOT NULL;
        ALTER TABLE "user" ALTER COLUMN "username" DROP NOT NULL;
        ALTER TABLE "creds" ADD "login" VARCHAR(255) NOT NULL;"""
