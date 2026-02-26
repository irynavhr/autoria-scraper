# AutoRia Async Scraper

An asynchronous application for scraping used car listings from the AutoRia platform and storing collected data in a PostgreSQL database.

This project was implemented as a technical assignment for a Junior Python Developer position.

---

## Description

The application navigates through AutoRia listing pages, opens each car detail page, extracts required information, and saves it into a PostgreSQL database while preventing duplicate records.

Scraping is implemented using asynchronous requests to improve performance and efficiency.

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
│   ├── main.py        # application entry point and database logic
│   ├── scraper.py     # scraping and parsing logic
│
├── dumps/             # database backups (if enabled)
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
| url            | TEXT      | Car listing URL                    |
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
SCRAPE_TIME=12:00
```

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

* PostgreSQL container initializes automatically
* the application connects to the database
* scraping process begins

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

## Application Workflow

1. The start page of AutoRia listings is requested.
2. Links to individual car pages are extracted.
3. Each car page is fetched and parsed.
4. Data is normalized:

   * mileage is converted into a numeric value
   * duplicates are checked before insertion
5. Records are stored in PostgreSQL.

---

## Implementation Notes

* Asynchronous requests are used to improve scraping performance.
* Docker Compose is used to run both the application and the database.
* Environment variables allow flexible configuration without code changes.
* The project structure allows further extension and scaling.

---

## Limitations

* Changes in AutoRia HTML structure may require updating parsing selectors.
* Scraping speed depends on network conditions and website limitations.

---

## Author

Iryna Hrytsenko
Junior Python Developer
