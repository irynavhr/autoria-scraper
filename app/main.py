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

async def insert_car(conn, car: dict):
    # check if car already exists in DB
    existing = await conn.fetchrow(
        "SELECT id FROM cars WHERE url = $1",
        car["url"]
    )

    # if exists - skip
    if existing:
        print("Car already exists, skip")
        return
    
    # else - insert
    await conn.execute("""
        INSERT INTO cars (
            url,
            title,
            price_usd,
            odometer,
            username,
            phone_number,
            image_url,
            images_count,
            car_number,
            car_vin
        )
        VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)
    """,
        car.get("url"),
        car.get("title"),
        car.get("price_usd"),
        car.get("odometer"),
        car.get("username"),
        car.get("phone_number"),
        car.get("image_url"),
        car.get("images_count"),
        car.get("car_number"),
        car.get("car_vin"),
    )
    print("Inserted new car")

async def main():
    # connect to DB
    conn = await connect_to_db()
    

    # create table if not exists
    await create_table(conn)
    print("✅ Table created")

    
    # parcing test
    html = await fetch_start_page()
    links = extract_car_links(html)

    # print(links[:10])  

    # fetch and parse first car page
    # first_car_url = links[3]
    # first_car_url = "https://auto.ria.com/uk/auto_skoda_octavia_38735104.html"
    # car_html = await fetch_car_page(first_car_url)
    # car_data = parse_car_page(car_html, first_car_url)
    
    for each in links:
        try:
            car_html = await fetch_car_page(each)
            car_data = parse_car_page(car_html, each)
            try:
                await insert_car(conn, car_data)
            except Exception as e:
                print(f"Error inserting {each} into DB: {e}")
                continue
        except Exception as e:
            print(f"Error processing {each}: {e}")
            continue

    # print all rows from DB
    rows = await conn.fetch("SELECT * FROM cars")
    for row in rows:
        print(dict(row))

asyncio.run(main())