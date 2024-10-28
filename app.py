"""Recursos Externos"""
import os
import re
import time
import psycopg2
from flask import Flask, jsonify, request
from flasgger import Swagger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

"""Recursos Propios"""
from model import db, LoanModel 
from schema import SimulatorSchema,FilterSchema,FindLoansSchema

# Cargar las variables de entorno
load_dotenv()  

app = Flask(__name__)
swagger = Swagger(app)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://default:J4GN8aXizguC@ep-solitary-bonus-a4lghu3s-pooler.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy
db.init_app(app)

# Crear las tablas en la base de datos (si aún no existen)
with app.app_context():
    db.create_all()

# Conexión a la base de datos
def connect_db():
    try:
        conn = psycopg2.connect(os.getenv("POSTGRES_URL"))
        return conn
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        return None

@app.route('/api/simulator', methods=['POST'])
def simular_financiacion():
    """
    Endpoint para simular financiación y obtener información de préstamos para múltiples CUITs.
    ---
    parameters:
      - name: cuit_list
        in: body
        required: true
        schema:
          type: object
          properties:
            cuit_list:
              type: array
              items:
                type: string
                description: "Lista de CUITs para los que se desea simular financiación"
    responses:
      200:
        description: Información de préstamos obtenida exitosamente
        schema:
          type: object
          properties:
            resultados:
              type: array
              items:
                type: object
                properties:
                  cuit:
                    type: string
                  nombre_persona:
                    type: string
                  prestamos:
                    type: array
                    items:
                      type: object
                      properties:
                        nombre:
                          type: string
                        tipo_tasa:
                          type: string
                        monto_maximo:
                          type: string
      400:
        description: Error en los datos de entrada
      500:
        description: Error en el procesamiento
    """
    try:
      data = SimulatorSchema().load(request.get_json())
      # data = request.get_json()
      if not data or 'cuit_list' not in data:
          return jsonify({"error": "CUIT es requerido"}), 400


      cuit_list = data['cuit_list']
      resultados = []
      no_calificados = []  # Lista para almacenar CUITs no calificados

      # 1) Inicializamos el navegador , activamos el driver y abrimos la pagina de inicio
      driver = webdriver.Chrome()  
      driver.get("https://wsec06.bancogalicia.com.ar")  

      # Esperamos un poco para que la página cargue
      time.sleep(2)

      # 2) Buscamos los campos de nombre de usuario y contraseña
      username_field = WebDriverWait(driver, 10).until(
          EC.visibility_of_element_located((By.NAME, "UserID"))
      )
      password_field = WebDriverWait(driver, 10).until(
          EC.visibility_of_element_located((By.NAME, "Password"))
      )

          #2.1) Ingresamos las credenciales de acceso
      username_field.send_keys("xxxxxx")  #Colocar usuario
      password_field.send_keys("xxxxx") #Colocar password 

          #2.2) Buscamos el botón de inicio de sesión
      login_button = WebDriverWait(driver, 10).until(
          EC.element_to_be_clickable((By.ID, "submitButton"))
      )
      driver.execute_script("arguments[0].click();", login_button)

      time.sleep(5)

      # 3) Buscamos la pestaña de 'Financiaciones' y hacemos click
      financiaciones_tab = WebDriverWait(driver, 10).until(
          EC.element_to_be_clickable((By.XPATH, "//a[text()='Financiaciones']"))
      )
      financiaciones_tab.click()

      # 4) Una vez abierto el modal, buscamos la opción  'Socio de valor' y también hacemos click
      socio_de_valor_tab = WebDriverWait(driver, 10).until(
          EC.element_to_be_clickable((By.XPATH, "//a[text()='Socio de valor']"))
      )
      socio_de_valor_tab.click()

      time.sleep(5)


      # 5) Búsqueda de líneas de crédito disponibles por cuit.
      no_califica = False
      count = 0
      for cuit_value in cuit_list:

          # 5.1)  Hacemos clic en el botón 'Simular'. 

          #Como solo hacemos click en el primer caso de búsqueda, establecemos un control de uso
          if not count > 0 or no_califica == True:

              simular_button = WebDriverWait(driver, 10).until(
                  EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Simular']"))
              )
              simular_button.click()
              
              no_califica = False
              time.sleep(10)

          # 5.2) Ingresamos el CUIT
          cuit_input = WebDriverWait(driver, 10).until(
              EC.visibility_of_element_located((By.ID, "INGRESO-INPUT-CUIT"))
          )
          cuit_input.send_keys(cuit_value)

          # 5.3) Hacemos click en el botón 'Continuar'
          continuar_button = WebDriverWait(driver, 10).until(
              EC.element_to_be_clickable((By.ID, "INGRESO-BUTTON-CONTINUAR"))
          )
          continuar_button.click()

          time.sleep(25)

          try:
            notification = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.Notification--Content"))
            )
            if "no podemos ofrecerte Socio de Valor" in notification.text:
                no_calificados.append(cuit_value)
                no_califica = True
                #print(f"CUIT no calificado: {cuit_value}")

               # Hacer clic en el botón "Aceptar"
                aceptar_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "FEEDBACK-BUTTON_PRIMARY"))
                )
                aceptar_button.click()  # Click en el botón 'Aceptar'
                

                time.sleep(15)
                continue  # Continúa al siguiente CUIT
          except:
              pass  # Si no se encuentra el elemento, simplemente continúa


          # 5.4) Buscamos el contenedor que muestra los préstamos disponibles.
          prestamos_container = WebDriverWait(driver, 10).until(
              EC.presence_of_element_located((By.CSS_SELECTOR, "div.grid-base"))
          )
          time.sleep(35)

          # 5.5) Almacenamos la propiedad 'textContent' de la div que contiene todos los préstamos
          all_prestamos_text = prestamos_container.text

          # 5.6) Almacenamos el nombre de la persona (titular del cuit)
          nombre_persona = all_prestamos_text.split("financiación para ")[1].split("\n")[0]

          # 5.7) Filtramos la información para que nos quede solo lo referido a los préstamos
          prestamos_info = re.findall(r'Préstamo (.*?)\n(.*?)\nPuede pedir hasta\n(\$[\d\.,]+)', all_prestamos_text, re.DOTALL)

          # 5.8) Estructuramos el json a devolver
          prestamos_resultados = []
          for prestamo in prestamos_info:
              nombre, tipo_tasa, monto_maximo = prestamo
              prestamos_resultados.append({
                  "nombre": nombre.strip(),
                  "tipo_tasa": tipo_tasa.strip(),
                  "monto_maximo": monto_maximo.strip()
              })

          # Agregamos a la base de datos la información del prestamo
              new_loan = LoanModel(
                  cuit=cuit_value,
                  name_person=nombre_persona.strip(),
                  name_loan=nombre.strip(),
                  interest_rate=tipo_tasa.strip(),
                  max_amoun=monto_maximo.strip()
              )
              db.session.add(new_loan)
              

          resultados.append({
          "cuit": cuit_value,
          "nombre_persona": nombre_persona.strip(),
          "prestamos": prestamos_resultados
              })
          
          # 5.9) Hacemos click en el botón 'Volver'
          volver_button = WebDriverWait(driver, 10).until(
              EC.element_to_be_clickable((By.ID, "INGRESO-BUTTON-VOLVER"))
          )
          volver_button.click()

          count +=1 #modifcamos la variable de control.
          
          time.sleep(15)
       
       # Al finalizar, intentamos hacer commit y capturamos cualquier excepción.
      try:
          db.session.commit()
      except Exception as e:
          print("Error al hacer commit:", e)# Aunque haya un error, seguimos mostrando los resultados.


      # Al finalizar, cerramos el navegador
     
      driver.quit()
      

      return jsonify({"resultados": resultados,"no_calificados": no_calificados}), 200
    
    except Exception as error:
        return{"status":500,"message":str(error)},500


@app.route('/api/filter_loans', methods=['POST'])
def filter_loans():
    """
    Endpoint para filtrar préstamos según los criterios proporcionados.
    ---
    parameters:
      - name: filter
        in: body
        required: true
        schema:
          type: object
          properties:
            name_loan:
              type: string
            interest_rate:
              type: string
            name_person:
              type: string
            cuit:
              type: string
    responses:
      200:
        description: Lista de préstamos filtrados
        schema:
          type: object
          properties:
            loans:
              type: array
              items:
                type: object
                properties:
                  cuit:
                    type: string
                  name_person:
                    type: string
                  name_loan:
                    type: string
                  interest_rate:
                    type: string
                  max_amoun:
                    type: string
      400:
        description: Error en los datos de entrada
    """
    try:
      data =  FilterSchema().load(request.get_json())
     

      name_loan = data['name_loan']
      interest_rate = data['interest_rate']
      name_person = data['name_person']
      cuit = data['cuit']

      # Filtrar préstamos en la base de datos
      loans = LoanModel.query.filter_by(
          # name_loan=name_loan,
          # interest_rate=interest_rate,
          # name_person=name_person,
          cuit = cuit
      ).all()

      loans_schema = FindLoansSchema().dump(loans,many=True)
      if loans:
        return jsonify({"loans": loans_schema}), 200
      else:
          raise Exception ("No se encuentran datos cargados con esos parámetros.")
    except Exception as error:
      return{"status":500,"message":str(error)},500
        

        
    
if __name__ == '__main__':
    conn = connect_db()
    if conn:
        print("Conexión a la base de datos establecida correctamente.")
        conn.close()  # Cierra la conexión después de comprobarla
        app.run(debug=True, port=5001)
    else:
        print("No se pudo establecer la conexión a la base de datos. La aplicación no se iniciará.")
