# AutoRia Async Scraper

An asynchronous application for scraping used car listings from the AutoRia platform and storing collected data in a PostgreSQL database.

This project was implemented as a technical assignment for a Junior Python Developer position. The scraper is designed with performance, configurability, and stability in mind, using asynchronous requests and controlled concurrency.

---

## Description

The application iterates through AutoRia listing pages, visits individual car detail pages, extracts required information, and stores it in a PostgreSQL database while preventing duplicate records.

Scraping is performed asynchronously and supports pagination across listing pages. During development and testing, execution can be limited to a configurable number of pages to avoid long runtimes and website rate limiting.

---

## Technologies Used

* Python 3.11+
* asyncio
* httpx (asynchronous HTTP client)
* BeautifulSoup4
* PostgreSQL
* asyncpg
* Docker
* docker-compose
* python-dotenv

---

## Project Structure

```
.
├── app/
│   ├── main.py        # application entry point
│   ├── scraper.py     # scraping and pagination logic
│   ├── db.py          # database operations
│
├── dumps/             # database backups (optional)
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
└── README.md
```

---

## Database Schema

Table: `cars`

| Field          | Type      | Description                        |
| -------------- | --------- | ---------------------------------- |
| url            | TEXT      | Car listing URL (unique)           |
| title          | TEXT      | Vehicle title                      |
| price_usd      | INTEGER   | Price in USD                       |
| odometer       | INTEGER   | Mileage converted to numeric value |
| username       | TEXT      | Seller name                        |
| phone_number   | TEXT      | Seller phone number                |
| image_url      | TEXT      | Main image URL                     |
| images_count   | INTEGER   | Number of images                   |
| car_number     | TEXT      | License plate number               |
| car_vin        | TEXT      | VIN code                           |
| datetime_found | TIMESTAMP | Time when record was stored        |

Duplicate records are prevented using a unique constraint on the `url` field.

---

## Configuration

Application settings are stored in a `.env` file.

Example:

```
POSTGRES_DB=autoria
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
START_URL=https://auto.ria.com/uk/car/used/
MAX_PAGES=3
```

### Configuration Notes

* `START_URL` — initial AutoRia listings page.
* `MAX_PAGES` — limits the number of processed pages during development/testing.
  If omitted or set to `0`, the scraper processes all available pages.

---

## Running the Project

### 1. Clone the repository

```
git clone <repository_url>
cd autoria-scraper
```

### 2. Start the application using Docker

```
docker compose up --build
```

After startup:

* PostgreSQL container initializes automatically.
* The application connects to the database.
* Scraping begins according to configuration.

---

## Application Workflow

1. The scraper requests a listing page.
2. Pagination iterates through pages sequentially.
3. Links to individual car listings are extracted.
4. Car pages are processed concurrently using `asyncio.gather`.
5. Parsed data is normalized and inserted into PostgreSQL.
6. Duplicate entries are ignored automatically.

---

## Performance and Stability Improvements

The scraper includes several optimizations:

* **Concurrent scraping** using `asyncio.gather` to process multiple car pages simultaneously.
* **Pagination support** to iterate through all listing pages.
* **Controlled concurrency** to reduce request bursts and improve stability.
* **Timeout handling** to prevent application crashes caused by slow responses.
* **Configurable page limits** (`MAX_PAGES`) for faster development and safer testing.

These decisions help balance performance with website rate limiting and network reliability.

---

## Checking Stored Data

Connect to the database container:

```
docker exec -it postgres_db psql -U postgres
```

Query stored records:

```
SELECT * FROM cars;
```

---

## Limitations

* Website structure changes may require updating parsing selectors.
* Large-scale scraping may be affected by website rate limiting.
* For development purposes, page limits are recommended to avoid excessive runtime.

---

## Author

Iryna Hrytsenko
Junior Python Developer
