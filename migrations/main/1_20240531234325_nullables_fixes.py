from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "manufacturers" ALTER COLUMN "year_of_creation" DROP NOT NULL;
        ALTER TABLE "review" ALTER COLUMN "beer_id" SET NOT NULL;
        ALTER TABLE "review" ALTER COLUMN "user_id" SET NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "review" ALTER COLUMN "beer_id" DROP NOT NULL;
        ALTER TABLE "review" ALTER COLUMN "user_id" DROP NOT NULL;
        ALTER TABLE "manufacturers" ALTER COLUMN "year_of_creation" SET NOT NULL;"""
