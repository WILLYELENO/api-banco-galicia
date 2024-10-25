def obtener_ofertas(session, cuit):
    url_ofertas = "https://aple.bff.bancogalicia.com.ar/api/ofertas"
    params = {'cuit': cuit}


    # Realizar la solicitud a la API con las cookies y autenticación de la sesión
    response = session.get(url_ofertas, params=params)

    if response.status_code == 200:
        ofertas = response.json()
        return ofertas
    else:
        print("Error al obtener ofertas:", response.status_code)
        return None