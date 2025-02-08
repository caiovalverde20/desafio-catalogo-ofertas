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
from decimal import Decimal

def configurar_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def extrair_preco(texto_preco):
    if not texto_preco or not isinstance(texto_preco, str):
        return None
    numeros = re.findall(r'\d+', texto_preco)
    return Decimal("".join(numeros)) if numeros else None

def acessar_mercado_livre(driver, termo_pesquisa):
    print("Acessando Mercado Livre...")
    driver.get("https://www.mercadolivre.com.br")
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@class="nav-search-input"]'))
    )
    search_box.send_keys(termo_pesquisa)
    search_box.submit()

def rolar_pagina(driver):
    print("Carregando resultados...")
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def coletar_produtos(driver):
    return WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//li[contains(@class, "ui-search-layout__item")]'))
    )

def extrair_imagem(produto):
    try:
        imagem_element = produto.find_element(By.XPATH, './/img[contains(@class, "poly-component__picture")]')
        driver = produto._parent
        WebDriverWait(driver, 5).until(lambda d: imagem_element.get_attribute("src") not in ["", None])
        imagem = imagem_element.get_attribute("src")
        if not imagem or "data:image" in imagem:
            imagem = imagem_element.get_attribute("data-src")
        return imagem
    except Exception as e:
        print(f"Erro ao extrair imagem: {e}")
        return ""

def extrair_dados_produto(produto):
    try:
        nome = produto.find_element(By.XPATH, './/h3[@class="poly-component__title-wrapper"]/a').text

        preco_element = produto.find_element(By.XPATH, './/div[@class="poly-price__current"]/span')
        preco = extrair_preco(preco_element.get_attribute("aria-label")) if preco_element else None

        imagem = extrair_imagem(produto)

        link = produto.find_element(By.XPATH, './/h3[@class="poly-component__title-wrapper"]/a').get_attribute("href")
        parcelamento = extrair_texto(produto, './/span[contains(@class,"poly-price__installments")]')
        preco_sem_desconto = extrair_preco(extrair_texto(produto, './/s[contains(@class,"andes-money-amount")]'))
        percentual_desconto = calcular_desconto(preco, preco_sem_desconto)
        tipo_entrega = "full" if verificar_elemento(produto, './/span[contains(@class, "poly-component__shipped-from")]') else "normal"
        frete_gratis = "grátis" in (extrair_texto(produto, './/div[contains(@class, "poly-component__shipping")]', default="")).lower()

        return {
            "nome": nome,
            "preco": preco,
            "imagem": imagem,
            "link": link,
            "parcelamento": parcelamento,
            "preco_sem_desconto": preco_sem_desconto,
            "percentual_desconto": percentual_desconto,
            "tipo_entrega": tipo_entrega,
            "frete_gratis": frete_gratis
        }
    except Exception as e:
        print(f"Erro ao processar um produto: {e}")
        return None

def extrair_texto(produto, xpath, default=None):
    try:
        return produto.find_element(By.XPATH, xpath).text.strip()
    except:
        return default

def verificar_elemento(produto, xpath):
    try:
        produto.find_element(By.XPATH, xpath)
        return True
    except:
        return False

def calcular_desconto(preco, preco_sem_desconto):
    if preco and preco_sem_desconto and preco_sem_desconto > preco:
        return round(((preco_sem_desconto - preco) / preco_sem_desconto) * 100, 2)
    return None

def buscar_ofertas():
    driver = configurar_driver()
    try:
        acessar_mercado_livre(driver, "Computador Gamer i7 16gb ssd 1tb")
        rolar_pagina(driver)
        produtos = coletar_produtos(driver)
        print(f"{len(produtos)} produtos encontrados.")
        ofertas = [extrair_dados_produto(produto) for produto in produtos if extrair_dados_produto(produto)]
    finally:
        driver.quit()
    atualizar_ofertas(ofertas)