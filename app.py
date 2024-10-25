import requests
import json
from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

BASE_URL = "https://wsec06.bancogalicia.com.ar/"
LOGIN_URL =f" {BASE_URL}Users/LogIn"  # Asegúrate de que esta URL sea correctahttps://wsec06.bancogalicia.com.ar/Users/LogIn
OFERTAS_URL = f"{BASE_URL}api/ofertas"

# Credenciales (se pueden mover a un archivo de configuración o variables de entorno)
USERNAME = "jquinonez001"
PASSWORD = "Siembro08$"
@app.route('/api/login', methods=['POST'])
def login():
    """
    Endpoint para autenticarse en el sistema de Banco Galicia.
    ---
    responses:
      200:
        description: Autenticación exitosa
        schema:
          type: object
          properties:
            token:
              type: string
      401:
        description: Error de autenticación
    """
    session = requests.Session()

    # Realizar la primera solicitud para cargar el dispositivo de autenticación
    response = session.get(BASE_URL)
    if response.status_code != 200:
        return jsonify({"error": "Error al cargar el dispositivo de autenticación"}), 401

    # Datos de autenticación
    login_data = {
        'username': USERNAME,
        'password': PASSWORD,
        '__RequestVerificationToken': response.cookies.get('__RequestVerificationToken')  # Asumiendo que se necesita este token
    }

    # Realizar la solicitud de login
    response = session.post(LOGIN_URL, data=login_data, allow_redirects=True)

    # Manejar redirecciones
    if response.history:
        for resp in response.history:
            print(f"Redirected from {resp.url} to {response.url}")

    if response.status_code == 200:
        # Aquí ajusta según cómo obtienes el token
        bearer_token = response.cookies.get('session_id')  # Ejemplo de cómo obtener la cookie de sesión
        if bearer_token:
            return jsonify({"token": bearer_token}), 200
        else:
            return jsonify({"error": "Token no encontrado en la respuesta"}), 401
    else:
        return jsonify({"error": "Error de autenticación"}), 401

# @app.route('/api/ofertas', methods=['GET'])
# def get_ofertas():
#     """
#     Obtener líneas de financiamiento disponibles para un CUIT.
#     ---
#     parameters:
#       - name: cuit
#         in: query
#         type: string
#         required: true
#     responses:
#       200:
#         description: Listado de líneas de préstamo y montos máximos
#         schema:
#           id: Ofertas
#           properties:
#             ofertas:
#               type: array
#               items:
#                 type: object
#                 properties:
#                   nombre:
#                     type: string
#                   monto_maximo:
#                     type: number
#       400:
#         description: Error de entrada
#     """
#     cuit = request.args.get('cuit')
#     if not cuit:
#         return jsonify({"error": "CUIT es requerido"}), 400

#     session = requests.Session()

#     # Realizar login primero
#     login_data = {'username': USERNAME, 'password': PASSWORD}
#     response = session.post(LOGIN_URL, data=login_data)

#     if response.status_code != 200:
#         return jsonify({"error": "Error de autenticación"}), 401

#     # Obtener ofertas
#     ofertas_response = session.get(OFERTAS_URL, params={'cuit': cuit})

#     if ofertas_response.status_code != 200:
#         return jsonify({"error": "Error al obtener ofertas"}), 400

#     ofertas_data = ofertas_response.json()
#     result = [{"nombre": oferta["nombre"], "monto_maximo": oferta["montoMaximo"]} for oferta in ofertas_data]

#     # Generar archivo JSON de ejemplo
#     with open(f"{cuit}_ofertas.json", 'w') as outfile:
#         json.dump(result, outfile)

#     return jsonify({"ofertas": result})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
