import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()


async def create_table(conn):
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            id SERIAL PRIMARY KEY,
            url TEXT UNIQUE,
            title TEXT,
            price_usd INTEGER,
            odometer INTEGER,
            username TEXT,
            phone_number TEXT,
            image_url TEXT,
            images_count INTEGER,
            car_number TEXT,
            car_vin TEXT,
            datetime_found TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)


async def main():
    conn = await asyncpg.connect(
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        database=os.getenv("POSTGRES_DB"),
        host=os.getenv("POSTGRES_HOST"),
        port=5432,
    )

    print("✅ DB connected")

    await create_table(conn)

    print("✅ Table created")

    await conn.close()


asyncio.run(main())