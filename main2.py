from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import re

# Inicializar el navegador
driver = webdriver.Chrome()  # Asegúrate de que el ChromeDriver esté en tu PATH
driver.get("https://wsec06.bancogalicia.com.ar")  # Abre la página de inicio de sesión

# Esperar un poco para que la página cargue
time.sleep(3)

# Encontrar los campos de nombre de usuario y contraseña
username_field = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.NAME, "UserID"))
)
password_field = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.NAME, "Password"))
)

# Ingresar las credenciales
username_field.send_keys("jquinonez001")  # Tu nombre de usuario
password_field.send_keys("Siembro08$")  # Tu contraseña

# Encontrar el botón de inicio de sesión
login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "submitButton"))
)

# Hacer clic en el botón de inicio de sesión usando JavaScript
driver.execute_script("arguments[0].click();", login_button)

# Esperar un poco para que la página de destino cargue
time.sleep(5)

# Hacer clic en la pestaña de 'Financiaciones'
financiaciones_tab = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[text()='Financiaciones']"))
)

# Hacer clic en el elemento
financiaciones_tab.click()

# Hacer clic en 'Socio de valor'
socio_de_valor_tab = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[text()='Socio de valor']"))
)
socio_de_valor_tab.click()

# Esperar un poco para que se cargue la nueva página
time.sleep(5)

# Hacer clic en el botón 'Simular'
simular_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Simular']"))
)
simular_button.click()

# Esperar un poco para que se cargue la nueva página
time.sleep(5)

# Ingresar el CUIT
cuit_value = "30717432114"#"20111686441"  # Define el CUIT que deseas ingresar
cuit_input = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "INGRESO-INPUT-CUIT"))
)
cuit_input.send_keys(cuit_value)

# Hacer clic en el botón 'Continuar'
continuar_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "INGRESO-BUTTON-CONTINUAR"))
)
continuar_button.click()

# Esperar un poco para que se cargue la nueva página
time.sleep(5)

# Esperar a que el contenedor de préstamos esté presente
prestamos_container = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div.grid-base"))
)

# Asegúrate de que el contenedor se haya cargado completamente
time.sleep(2)

# Capturar el textContent de la div que contiene todos los préstamos
all_prestamos_text = prestamos_container.text

# Ajustar la expresión regular
prestamos_info = re.findall(r'Préstamo (.*?)\n(.*?)\nPuede pedir hasta\n(\$[\d\.,]+)', all_prestamos_text, re.DOTALL)

# Mostrar resultados
for prestamo in prestamos_info:
    nombre, tipo_tasa, monto_maximo = prestamo
    print(f"Nombre del Préstamo: {nombre.strip()}, Tipo de Tasa: {tipo_tasa.strip()}, Monto Máximo: {monto_maximo.strip()}")
# Imprimir el texto de todos los préstamos
print("Información de todos los préstamos:")
print(all_prestamos_text)

# Cerrar el navegador al final
#driver.quit()
