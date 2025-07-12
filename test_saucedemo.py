from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pytest

BASE_URL = "https://www.saucedemo.com/"

EXPECTED_IMAGES = {
    "Sauce Labs Backpack":           "sauce-backpack-1200x1500.jpg",
    "Sauce Labs Bike Light":         "bike-light-1200x1500.jpg",
    "Sauce Labs Bolt T-Shirt":       "bolt-shirt-1200x1500.jpg",
    "Sauce Labs Fleece Jacket":      "fleece-jacket-1200x1500.jpg",
    "Sauce Labs Onesie":             "onesie-1200x1500.jpg",
    "Test.allTheThings() T-Shirt (Red)": "red-tatt-1200x1500.jpg",
}
GLITCH_THRESHOLD = 3.0

@pytest.fixture(scope="module")
def driver():
    # Inicializa o Chrome
    options = webdriver.ChromeOptions()
    prefs = {
        # desabilita o serviço de credenciais e o prompt normal de salvar senha
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        # desabilita a checagem de vazamento de senhas (o “unsafe password”) -> stack overflow.com/questions/74793098/selenium-chrome-unsafe-password-popup
        "profile.password_manager_leak_detection": False,
        # desativa o Safe Browsing que dispara esse pop-up :contentReference[oaicite:1]{index=1} -> stackoverflow.com/questions/74793098/selenium-chrome-unsafe-password-popup
        "safebrowsing.enabled": False
    }
    options.add_experimental_option("prefs", prefs)
    
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    
    drv = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield drv
    drv.quit()

def test_fluxo_completo(driver):
    # 1. Acessar a página de login  
    driver.get(BASE_URL)
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    assert "inventory.html" in driver.current_url
    
    produtos = driver.find_elements(By.CSS_SELECTOR, ".inventory_item")
    adiciona_btns = driver.find_elements(By.CSS_SELECTOR, ".btn_inventory")
    # os produtos são adicionados ao carrinho todos
    adiciona_btns[0].click()
    adiciona_btns[1].click()
    # adiciona_btns[2].click()
    # adiciona_btns[3].click()
    # adiciona_btns[4].click()
    # adiciona_btns[5].click()
    
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    assert "cart.html" in driver.current_url
    
    driver.find_element(By.CSS_SELECTOR, ".cart_item .btn_secondary").click()  # remove o primeiro
    itens = driver.find_elements(By.CSS_SELECTOR, ".cart_item")
    assert len(itens) == 1
    
    driver.find_element(By.ID, "checkout").click()
    assert "checkout-step-one.html" in driver.current_url
    driver.find_element(By.ID, "first-name").send_keys("Henrique")
    driver.find_element(By.ID, "last-name").send_keys("Pontes")
    driver.find_element(By.ID, "postal-code").send_keys("12345")
    
    
    driver.find_element(By.ID, "continue").click()
    assert "checkout-step-two.html" in driver.current_url
    
    driver.find_element(By.ID, "finish").click()
    assert "checkout-complete.html" in driver.current_url

    # 6. Verificar mensagem de confirmação
    mensagem = driver.find_element(By.CSS_SELECTOR, ".complete-header").text
    assert mensagem.strip("!").upper() == "THANK YOU FOR YOUR ORDER"

    # tempo para esperar a página carregar
    # time.sleep(2)


def test_locked_user(driver):
    # 1. Acessar a página de login
    driver.get(BASE_URL)
    driver.find_element(By.ID, "user-name").send_keys("locked_out_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    
    # 2. Verificar mensagem de erro
    mensagem = driver.find_element(By.CSS_SELECTOR, ".error-message-container").text
    assert mensagem == "Epic sadface: Sorry, this user has been locked out."

# @pytest.mark.xfail(reason="bug conhecido: imagens trocadas para problem_user")
def test_problem_user(driver):
    # 1. Acessar a página de login
    driver.get(BASE_URL)
    driver.find_element(By.ID, "user-name").send_keys("problem_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    # 2) Aguarda inventário carregar
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item"))
    )

    # 3) Varre itens e coleta quais têm imagem “errada”
    mismatches = []
    for item in driver.find_elements(By.CLASS_NAME, "inventory_item"):
        nome = item.find_element(By.CLASS_NAME, "inventory_item_name").text
        src = item.find_element(By.CSS_SELECTOR, ".inventory_item_img img") \
                   .get_attribute("src")
        arquivo = src.split("/")[-1]  # pega só o arquivo
        esperado = EXPECTED_IMAGES.get(nome)
        if esperado and arquivo != esperado:
            mismatches.append((nome, esperado, arquivo))
        
    assert len(mismatches) == len(driver.find_elements(By.CLASS_NAME, "inventory_item"))
    
    # 2) Adiciona o primeiro item
    add_btn = driver.find_elements(By.CSS_SELECTOR, ".btn_inventory")[0]
    add_btn.click()
    
    # 3) Tenta remover o mesmo item
    remove_btn = driver.find_element(By.CSS_SELECTOR, ".btn_secondary")
    remove_btn.click()
    
    # 4) Verifica que o item NÃO foi removido do inventário
    items_after = driver.find_elements(By.CLASS_NAME, "inventory_item")
    assert len(items_after) >= 6, (
        "Esperava que o inventário continuasse com todos os itens, "
        f"mas encontrou apenas {len(items_after)}"
    )
    
    # 5) Navega para o checkout para reproduzir o glitch de input
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    driver.find_element(By.ID, "checkout").click()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "first-name")))
    
    # 6) Digita um nome e confirma que o valor exibido está VA RIAD O
    first_name = driver.find_element(By.ID, "first-name")
    first_name.send_keys("Henrique")
    driver.find_element(By.ID, "last-name").send_keys("Pontes")
    driver.find_element(By.ID, "postal-code").send_keys("12345")
    
    time.sleep(3)
    
    
def test_performance_glitch_user(driver):
    # 1. Acessar a página de login
    driver.get(BASE_URL)
    driver.find_element(By.ID, "user-name").send_keys("performance_glitch_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    
    # 2. Dispara o login e começa a medir
    start = time.perf_counter()
    driver.find_element(By.ID, "login-button").click()

    # 3. Aguarda os itens aparecerem (até um timeout razoável)
    WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item"))
    )
    load_time = time.perf_counter() - start

    # 4. Valida que houve redirecionamento correto
    assert "inventory.html" in driver.current_url, "Não redirecionou para inventory.html"

    # 5. Verifica que sofreu o “glitch” (levou mais do que o normal)
    assert load_time > GLITCH_THRESHOLD, (
        f"Esperava que o inventory demorasse > {GLITCH_THRESHOLD:.1f}s "
        f"para performance_glitch_user, mas carregou em {load_time:.2f}s"
    )

    # 6. (Opcional) Garante ainda que não ultrapassou um limite máximo aceitável
    assert load_time < 15, f"Carregamento muito lento: {load_time:.2f}s"

    print(f"[PERF] performance_glitch_user inventory carregou em {load_time:.2f}s")
    
def test_error_user(driver):
    # 1. Acessar a página de login
    driver.get(BASE_URL)
    driver.find_element(By.ID, "user-name").send_keys("error_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    
    # 2. Dispara o login
    driver.find_element(By.ID, "login-button").click()
    
    

