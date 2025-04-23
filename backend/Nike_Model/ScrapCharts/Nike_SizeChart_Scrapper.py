from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service

driver_path = "msedgedriver.exe"
service = Service(driver_path)

driver = webdriver.Edge(service=service)

def get_url_data(url):
    try:
        driver.get(url)

        tables = driver.find_elements(By.CLASS_NAME, "size-chart-table")
        
        for idx, table in enumerate(tables, start=1):
            print(f"\nExtracting data from Table {idx} for url {url}:")
            rows = table.find_elements(By.TAG_NAME, "tr")
            data = []
        
            for row in rows:
                rnames = row.find_elements(By.TAG_NAME, "th")
                columns = row.find_elements(By.TAG_NAME, "td")

                row_data = []

                for name in rnames:
                    row_data.append(name.text.strip())

                for col in columns:
                    row_data.append(col.text.strip())
            
                if row_data: 
                    data.append(row_data)

            for row in data:
                print(row)

    except Exception as e:
        print(f"Error processing {url}: {e}")

urls = [
    "https://www.nike.com/in/size-fit/mens-tops-asian-alpha",
    "https://www.nike.com/in/size-fit/mens-tops-alpha",
    "https://www.nike.com/in/size-fit/mens-bottoms-asian-alpha",
    "https://www.nike.com/in/size-fit/mens-bottoms-alpha",
    "https://www.nike.com/in/size-fit/mens-footwear",
    "https://www.nike.com/in/size-fit/mens-sand-sport-swimwear",
    "https://www.nike.com/in/size-fit/womens-tops-asian-alpha",
    "https://www.nike.com/in/size-fit/womens-tops-alpha",
    "https://www.nike.com/in/size-fit/womens-bottoms-asian-alpha",
    "https://www.nike.com/in/size-fit/womens-bottoms-alpha",
    "https://www.nike.com/in/size-fit/skirts-and-dresses-asian-sizing",
    "https://www.nike.com/in/size-fit/skirts-and-dresses-sizing",
    "https://www.nike.com/in/size-fit/womens-footwear",
    "https://www.nike.com/in/size-fit/womens-sport-swimwear",
    "https://www.nike.com/in/size-fit/womens-leggings-asian",
    "https://www.nike.com/in/size-fit/womens-leggings",
    "https://www.nike.com/in/size-fit/womens-bras-asian",
    "https://www.nike.com/in/size-fit/womens-bras",
    "https://www.nike.com/in/size-fit/unisex-socks"
]

for url in urls:
    get_url_data(url)

driver.quit()