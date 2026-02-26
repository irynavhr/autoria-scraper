import httpx
from bs4 import BeautifulSoup
import re



START_URL = "https://auto.ria.com/uk/car/used/"


async def fetch_start_page():
    async with httpx.AsyncClient() as client:
        response = await client.get(START_URL)

    print("Status:", response.status_code)

    return response.text


def extract_car_links(html: str):
    soup = BeautifulSoup(html, "html.parser")

    links = []

    # всі <a> теги з посиланнями
    for a in soup.find_all("a", class_ = "m-link-ticket", href=True):
        href = a["href"]

        # AutoRia карточки авто виглядають так:
        # https://auto.ria.com/auto_....
        if "/auto_" in href and "auto.ria.com" in href:
            links.append(href)

    print(f"Found {len(links)} links before deduplication")
    # прибираємо дублікати
    links = list(set(links))

    print(f"Found {len(links)} car links")

    return links


# async def fetch_car_page(url: str):
#     async with httpx.AsyncClient() as client:
#         response = await client.get(url)

#     print(f"Opened car page: {response.status_code}")

#     return response.text

async def fetch_car_page(url: str):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url)

        print(f"Opened car page: {response.status_code}")

        if response.status_code != 200:
            print(f"Skip {url} - status {response.status_code}")
            return None

        return response.text

    except httpx.RequestError as e:
        print(f"Request error for {url}: {e}")
        return None





def parse_car_page(html: str, url: str):
    if html is None:
        print(f"No HTML to parse for {url}")
        return None
    soup = BeautifulSoup(html, "html.parser")

    # ---------------- TITLE ----------------
    parent = soup.find(id="basicInfoTitle")
    title_tag = parent.find("h1", class_="titleL")
    title = title_tag.get_text(strip=True) if title_tag else None

    # ---------------- PRICE USD ----------------
    price = None
    parent = soup.find(id="basicInfoPrice")
    price_tag = parent.find("strong", class_="titleL")
    if price_tag:
        price_text = price_tag.get_text(strip=True)
        price = int(re.sub(r"\D", "", price_text))

    # ---------------- ODOMETER ----------------
    odometer = None
    parent = soup.find(id="basicInfoTableMainInfo0")
    odometer_tag = parent.find("span", class_="body")

    if odometer_tag:
        text = odometer_tag.get_text(strip=True).lower()
        number = int(re.search(r"\d+", text).group())
        odometer = number * 1000 if "тис" in text else number
        
       

    # ---------------- USERNAME ----------------
    username = None
    seller_tag = None
    parent = soup.find(id="sellerInfoUserName")
    if parent:
        seller_tag = parent.find("span", class_="common-text ws-pre-wrap titleM")
    if seller_tag:
        username = seller_tag.get_text(strip=True)

    # ---------------- PHONE ----------------!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    phone_number = None
    parent = soup.find(id="sellerInfo")
    if parent:
        parent = parent.find("div", class_="button-main mt-12")
    phone_tag = None
    if parent:
        phone_tag = parent.find("span", class_="common-text ws-pre-wrap action")
    if phone_tag:
        text = phone_tag.get_text(strip=True)
        phone_number = re.search(r"\d+", text).group()
        if phone_number[:2] != "38":
            phone_number = "38" + phone_number
        # phone_number = int(phone_number)
   

    # ---------------- IMAGE ----------------
    image_url = None
    parent = soup.find("span", class_="picture")
    img_tag = soup.find("img")
    if img_tag:
        image_url = img_tag["data-src"]

    # ---------------- IMAGES COUNT ----------------
    images_count = 0
    parent = soup.find(class_="common-badge alpha medium")
    spans = parent.find_all("span")
    nums = []
    for span in spans:
        text = span.get_text(strip=True)
        if text.isdigit():
            nums.append(int(text))
    images_count = nums[1]

    # ---------------- CAR NUMBER & VIN ----------------
    car_number = None
    parent = soup.find("div", class_="car-number")  
    
    car_number_tag = None
    if parent:
        car_number_tag = parent.find("span", class_="body")
    if car_number_tag:
        car_number = car_number_tag.get_text(strip=True)
  

    # VIN ----------------
    car_vin = None
    parent = soup.find("div", class_="badge-template")  
    
    car_vin_tag = None
    if parent:
        car_vin_tag = parent.find("span", class_="badge")
    
    if car_vin_tag:
        car_vin = car_vin_tag.get_text(strip=True)
    


    data = {
        "url": url,
        "title": title,
        "price_usd": price,
        "odometer": odometer,
        "username": username,
        "phone_number": phone_number,
        "image_url": image_url,
        "images_count": images_count,
        "car_number": car_number,
        "car_vin": car_vin,
    }

    print("\nParsed car:")
    for k, v in data.items():
        print(k, "=", v)


    

    return data