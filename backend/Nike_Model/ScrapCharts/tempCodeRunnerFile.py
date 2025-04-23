from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service

driver_path = "msedgedriver.exe"
service = Service(driver_path)

driver = webdriver.Edge(service=service)

def get_url_data(url):