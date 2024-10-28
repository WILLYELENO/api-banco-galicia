# Api-Banco-Galicia

# API de Simulación de Préstamos

## Descripción

Esta API permite simular financiación y gestionar préstamos para múltiples CUITs. Utiliza Selenium para interactuar con la página web de Banco Galicia y proporciona endpoints para simular préstamos y filtrar resultados según criterios específicos.

## Tecnologías Utilizadas

- **Flask**: Framework para desarrollar aplicaciones web.
- **Flask-SQLAlchemy**: ORM para facilitar la interacción con la base de datos.
- **PostgreSQL**: Sistema de gestión de bases de datos relacional.
- **Selenium**: Herramienta para automatizar navegadores web.
- **Flasgger**: Extensión para documentación de API en Swagger.
- **Psycopg2**: Adaptador PostgreSQL para Python.

## Instalación

### Requisitos Previos

- Python 3.6 o superior.
- PostgreSQL (asegúrate de tener las credenciales de conexión).

### Clonar el Repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_REPOSITORIO>


### Crear un Entorno Virtual

python -m venv venv
source venv/bin/activate  # En Linux/Mac
venv\Scripts\activate     # En Windows

### Instalar Dependencias

pip install -r requirements.txt

###Configuración de Variables de Entorno

POSTGRES_URL="postgres://<usuario>:<contraseña>@<host>:<puerto>/<nombre_base_datos>"

###Uso

from app import db
with app.app_context():
    db.create_all()

### Ejecutar la Aplicación
python app.py



## Endpoints

## Simulación de Préstamos
URL: /api/simulator
Método: POST
Descripción: Simula financiación para múltiples CUITs.
Parámetros:
cuit_list: Lista de CUITs para los que se desea simular financiación.

###Ejemplo de Solicitud

{
  "cuit_list": ["2011168XXXX", "3071824XXXX"]
}

###Respuesta Exitosa

{
  "resultados": [
    {
      "cuit": "20111XXXXX",
      "nombre_persona": "XXXX,LUIS MIGUEL",
      "prestamos": [
        {
          "nombre": "Inmediato Corto Plazo",
          "tipo_tasa": "Tasa Fija",
          "monto_maximo": "$225.000.000"
        }
      ]
    }
  ],
  "no_calificados": [
    "30718244044"
  ]
}

##Filtrar Préstamos
URL: /api/filter_loans
Método: POST
Descripción: Filtra préstamos según los criterios proporcionados.
Parámetros:
name_loan: Nombre del préstamo.
interest_rate: Tipo de tasa del préstamo.
name_person: Nombre de la persona.
cuit: CUIT asociado.

###Ejemplo de Solicitud

{
  "name_loan": "Inmediato Corto Plazo",
  "interest_rate": "Tasa Fija",
  "name_person": "ARROSPIDE,LUIS MIGUEL",
  "cuit": "20111686441"
}


###Respuesta Exitosa

{
  "loans": [
    {
      "cuit": "20111686441",
      "name_person": "ARROSPIDE,LUIS MIGUEL",
      "name_loan": "Inmediato Corto Plazo",
      "interest_rate": "Tasa Fija",
      "max_amoun": "$225.000.000"
    }
  ]
}
