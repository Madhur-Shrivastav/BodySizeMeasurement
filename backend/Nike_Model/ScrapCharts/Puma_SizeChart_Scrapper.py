from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os

driver_path = "msedgedriver.exe"
service = Service(driver_path)
driver = webdriver.Edge(service=service)

def get_url_data(url,category):
    try:

        driver.get(url)

        driver.implicitly_wait(10)

        size_guide_button = driver.find_element(By.CSS_SELECTOR, "button[data-test-id='size-guide-btn']")
        driver.execute_script("arguments[0].click();", size_guide_button)

        time.sleep(2)

        modal = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "modal"))
        )
        
        print("Modal found:", modal)
        
        WebDriverWait(driver, 10).until(
            EC.visibility_of(modal)
        )
        
        print("Modal is visible.")

        size_guide_tables = WebDriverWait(modal, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "table")))

        print("Size Tables: ",size_guide_tables)
        size_guide_json = {}
        for index, table in enumerate(size_guide_tables):  
            # if index in [4, 6]:
            #    continue
            
            script = """
            let table = arguments[0];
            return [...table.rows].map(row => [...row.cells].map(cell => cell.innerText.trim()));
            """
            size_guide_data = driver.execute_script(script, table)
    
            if size_guide_data:
                size_guide_json[f"table_{index}"] = size_guide_data
   
            size_guide_json[f"table_{index}"] = size_guide_data
        
        output_folder = "Puma_size_guide_charts"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        output_file = os.path.join(output_folder, category)
        with open(output_file, "w", encoding="utf-8") as json_file:
            json.dump(size_guide_json, json_file, indent=4, ensure_ascii=False)
        print(f"JSON data saved to: {output_file}")
  
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

urls = [
        {"https://in.puma.com/in/en/pd/puma-x-teenage-mutant-ninja-turtles-mens-relaxed-fit-graphic-tee/630099?swatch=01","tshirts-tops"},
        {"https://in.puma.com/in/en/pd/mens-classics-graphic-polo/681034?swatch=20","polo"},
        {"https://in.puma.com/in/en/pd/puma-warmcell-lightweight-slim-fit-mens-jacket/849401?swatch=01","jackets"},
        {"https://in.puma.com/in/en/pd/puma-x-one8-deltaknit-mens-hoodie/628281?swatch=30","sweatshirts-hoodies"},
        {"https://in.puma.com/in/en/pd/zippered-mens-jersey-pants/849323?swatch=06","pants"},
        {"https://in.puma.com/in/en/pd/puma-x-teenage-mutant-ninja-turtles-mens-relaxed-fit--7%22-shorts/630101?swatch=01","shorts"},
        {"https://in.puma.com/in/en/pd/mens-poly-piping-tracksuit/684852?swatch=01","tracksuits"},
        {"https://in.puma.com/in/en/pd/bfc-home-replica-mens-slim-fit-football-jersey/607032?swatch=01","jersey"},
        {"https://in.puma.com/in/en/pd/mens-long-sleeve-thermal-top/677829?swatch=02","thermal-top"},
        {"https://in.puma.com/in/en/pd/puma-supima-mens-briefs/688422?swatch=01","inner-wear"},
        {"https://in.puma.com/in/en/pd/bmw-m-motorsport-mt7%2B-mens-track-jacket/624139?swatch=05","motorsports"}
    ]

for url, category in urls:
    get_url_data(url, category)

driver.quit()