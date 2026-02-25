import asyncio
import asyncpg
import os
from dotenv import load_dotenv
from scraper import fetch_start_page, extract_car_links, parse_car_page, fetch_car_page
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
    # connect to DB
    conn = await asyncpg.connect(
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        database=os.getenv("POSTGRES_DB"),
        host=os.getenv("POSTGRES_HOST"),
        port=5432,
    )
    print("✅ DB connected")

    # create table if not exists
    await create_table(conn)
    print("✅ Table created")

    
    # parcing test
    html = await fetch_start_page()
    links = extract_car_links(html)

    # print(links[:10])  

    # fetch and parse first car page
    # first_car_url = links[3]
    first_car_url = "https://auto.ria.com/uk/auto_mercedes_benz_s_class_39172208.html"

    car_html = await fetch_car_page(first_car_url)
    car_data = parse_car_page(car_html, first_car_url)


    # close connection 
    await conn.close()

asyncio.run(main())