from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from ofertas.models import Produto

def buscar_ofertas():
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        print("Abrindo Mercado Livre...")
        driver.get("https://www.mercadolivre.com.br")
        
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@class="nav-search-input"]'))
        )
        search_box.send_keys("Computador Gamer i7 16gb ssd 1tb")
        search_box.submit()
        
        print("Aguardando resultados...")
        produtos = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//li[contains(@class, "ui-search-layout__item")]'))
        )
        
        print(f"Encontrados {len(produtos)} produtos.")
        
        for produto in produtos:
            try:
                nome = produto.find_element(By.XPATH, './/h3[@class="poly-component__title-wrapper"]/a').text
                
                preco_element = produto.find_element(By.XPATH, './/div[@class="poly-price__current"]/span')
                preco = preco_element.get_attribute("aria-label").replace(' reais', '').replace(',', '.') if preco_element else "0.00"
                
                try:
                    imagem_element = produto.find_element(By.XPATH, './/img[contains(@class, "poly-component__picture")]')
                    imagem = imagem_element.get_attribute("src") if imagem_element else ""
                except:
                    imagem = ""
                
                link_element = produto.find_element(By.XPATH, './/h3[@class="poly-component__title-wrapper"]/a')
                link = link_element.get_attribute("href") if link_element else ""
                
                Produto.objects.create(
                    nome=nome,
                    preco=float(preco),
                    imagem=imagem,
                    link=link
                )
                print(f"Produto salvo no banco de dados: {nome}")

            except Exception as e:
                print(f"Erro ao processar um produto: {e}")
    
    finally:
        driver.quit()