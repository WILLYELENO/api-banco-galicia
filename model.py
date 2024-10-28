from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import func

# Crear una instancia de SQLAlchemy
db = SQLAlchemy()

class LoanModel(db.Model):
    __tablename__ = 'loans'  

    id_loan_model = db.Column(db.Integer, primary_key=True)  # ID del préstamo
    cuit = db.Column(db.String(20), nullable=True)  # CUIT asociado al préstamo
    name_person = db.Column(db.String(100), nullable=True)  # Nombre de la persona
    name_loan = db.Column(db.String(100), nullable=True)  # Nombre del préstamo
    interest_rate = db.Column(db.String(50), nullable=True)  # Tipo de tasa del préstamo
    max_amoun = db.Column(db.String(20), nullable=True)  # Monto máximo del préstamo
    #create_date = db.Column(db.TIMESTAMP,nullable=True,server_default = func.now())

    def __repr__(self):
        return f'<Prestamo {self.nombre}>'