import requests

# Crear una sesión para manejar cookies automáticamente
session = requests.Session()

# URL de inicio de sesión
login_url = "https://wsec06.bancogalicia.com.ar/Users/LogIn"

# Datos de inicio de sesión (ajusta los nombres de los campos si es necesario)
payload = {
    'username': 'tu_usuario',  # Cambia esto al nombre correcto
    'password': 'tu_contraseña'  # Cambia esto al nombre correcto
}

try:
    # Intentar iniciar sesión
    initial_response = session.post(login_url, data=payload)

    # Comprobar el código de estado
    initial_response.raise_for_status()

    # Verificar si hay un error en la respuesta
    if "ERGO0005" in initial_response.text:
        print("Error en el inicio de sesión: ERGO0005. Revisa tu conexión o sesión abierta.")
    else:
        print("Inicio de sesión exitoso.")
        
        # Verifica si la respuesta fue redirigida
        if initial_response.history:
            for resp in initial_response.history:
                print(f"Redirigido de {resp.url} a {initial_response.url}")

except requests.exceptions.HTTPError as err:
    print(f"Error HTTP: {err}")
except requests.exceptions.RequestException as e:
    print(f"Ocurrió un error: {e}")
