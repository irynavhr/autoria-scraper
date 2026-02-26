import asyncio
import asyncpg
import os
from dotenv import load_dotenv
from scraper import START_URL,  scrape_all_pages
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

async def connect_to_db():
    for i in range(10):
        try:
            conn = await asyncpg.connect(
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
                database=os.getenv("POSTGRES_DB"),
                host=os.getenv("POSTGRES_HOST"),
                port=5432,
            )
            print("Connected to DB")
            return conn

        except Exception:
            print("Waiting for DB...")
            await asyncio.sleep(2)

    raise Exception("Database is not available")

async def main():
    # connect to DB
    conn = await connect_to_db()
    

    # create table if not exists
    await create_table(conn)
    print("✅ Table created")


    await scrape_all_pages(conn, START_URL)


    # print all rows from DB
    rows = await conn.fetch("SELECT * FROM cars")
    for row in rows:
        print(dict(row))

asyncio.run(main())