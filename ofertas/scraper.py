import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from ofertas.services import atualizar_ofertas

def extrair_preco(texto_preco):
    """ Extrai corretamente o valor numérico do preço. """
    numeros = re.findall(r'\d+', texto_preco)
    if not numeros:
        return None
    return int("".join(numeros))

def buscar_ofertas():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        print("Acessando Mercado Livre...")
        driver.get("https://www.mercadolivre.com.br")

        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@class="nav-search-input"]'))
        )
        search_box.send_keys("Computador Gamer i7 16gb ssd 1tb")
        search_box.submit()

        print("Carregando resultados...")

        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        produtos = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//li[contains(@class, "ui-search-layout__item")]'))
        )

        print(f"{len(produtos)} produtos encontrados.")

        ofertas = []

        for produto in produtos:
            try:
                nome = produto.find_element(By.XPATH, './/h3[@class="poly-component__title-wrapper"]/a').text
                
                preco_element = produto.find_element(By.XPATH, './/div[@class="poly-price__current"]/span')
                preco = extrair_preco(preco_element.get_attribute("aria-label")) if preco_element else None

                try:
                    imagem_element = produto.find_element(By.XPATH, './/img[contains(@class, "poly-component__picture")]')
                    WebDriverWait(driver, 5).until(lambda d: imagem_element.get_attribute("src") != "")
                    imagem = imagem_element.get_attribute("src")
                    if not imagem or "data:image" in imagem:
                        imagem = imagem_element.get_attribute("data-src")
                except:
                    imagem = ""

                link_element = produto.find_element(By.XPATH, './/h3[@class="poly-component__title-wrapper"]/a')
                link = link_element.get_attribute("href") if link_element else ""

                try:
                    parcelamento_element = produto.find_element(By.XPATH, './/span[contains(@class,"poly-price__installments")]')
                    parcelamento = parcelamento_element.text.strip()
                except:
                    parcelamento = ""

                try:
                    preco_sem_desconto_element = produto.find_element(By.XPATH, './/s[contains(@class,"andes-money-amount")]')
                    preco_sem_desconto = extrair_preco(preco_sem_desconto_element.text) if preco_sem_desconto_element else None
                except:
                    preco_sem_desconto = None

                if preco and preco_sem_desconto and preco_sem_desconto > preco:
                    percentual_desconto = round(((preco_sem_desconto - preco) / preco_sem_desconto) * 100, 2)
                else:
                    percentual_desconto = None

                try:
                    produto.find_element(By.XPATH, './/span[contains(@class, "poly-component__shipped-from")]')
                    tipo_entrega = "full"
                except:
                    tipo_entrega = "normal"

                try:
                    if produto.find_element(By.XPATH, './/div[contains(@class, "poly-component__shipping")]'):
                        frete_gratis_element = produto.find_element(By.XPATH, './/div[contains(@class, "poly-component__shipping")]').text
                        frete_gratis = "grátis" in frete_gratis_element.lower()
                    else:
                        frete_gratis = False
                except:
                    frete_gratis = False

                ofertas.append({
                    "nome": nome,
                    "preco": preco,
                    "imagem": imagem,
                    "link": link,
                    "parcelamento": parcelamento,
                    "preco_sem_desconto": preco_sem_desconto,
                    "percentual_desconto": percentual_desconto,
                    "tipo_entrega": tipo_entrega,
                    "frete_gratis": frete_gratis
                })

            except Exception as e:
                print(f"Erro ao processar um produto: {e}")

    finally:
        driver.quit()

    atualizar_ofertas(ofertas)
