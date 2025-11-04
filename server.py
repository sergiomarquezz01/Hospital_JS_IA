from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import random

app = Flask(__name__, static_folder="static", static_url_path="/static")
CORS(app)

# ======================================================
# DATOS INICIALES
# ======================================================

pacientes = [
    {"id": 1, "nombre": "Ana López", "edad": 32, "dni": "12345678A"},
    {"id": 2, "nombre": "Carlos Ramírez", "edad": 45, "dni": "23456789B"},
    {"id": 3, "nombre": "María Pérez", "edad": 28, "dni": "34567890C"},
    {"id": 4, "nombre": "José Martínez", "edad": 51, "dni": "45678901D"},
    {"id": 5, "nombre": "Lucía Fernández", "edad": 37, "dni": "56789012E"},
    {"id": 6, "nombre": "Antonio García", "edad": 41, "dni": "67890123F"},
    {"id": 7, "nombre": "Laura Ruiz", "edad": 25, "dni": "78901234G"},
    {"id": 8, "nombre": "Pedro Jiménez", "edad": 39, "dni": "89012345H"},
    {"id": 9, "nombre": "Marta Castillo", "edad": 29, "dni": "90123456I"},
    {"id": 10, "nombre": "David Torres", "edad": 34, "dni": "01234567J"},
    {"id": 11, "nombre": "Rosa Morales", "edad": 48, "dni": "11223344K"},
    {"id": 12, "nombre": "Sergio Navarro", "edad": 33, "dni": "22334455L"},
    {"id": 13, "nombre": "Patricia Vega", "edad": 30, "dni": "33445566M"},
    {"id": 14, "nombre": "Javier Herrera", "edad": 47, "dni": "44556677N"},
    {"id": 15, "nombre": "Cristina Díaz", "edad": 27, "dni": "55667788O"},
    {"id": 16, "nombre": "Andrés Molina", "edad": 36, "dni": "66778899P"},
    {"id": 17, "nombre": "Silvia Rojas", "edad": 31, "dni": "77889900Q"},
    {"id": 18, "nombre": "Raúl Gómez", "edad": 40, "dni": "88990011R"},
    {"id": 19, "nombre": "Isabel Núñez", "edad": 44, "dni": "99001122S"},
    {"id": 20, "nombre": "Tomás Peña", "edad": 52, "dni": "11112223T"},
    {"id": 21, "nombre": "Sofía Ortega", "edad": 26, "dni": "12131415U"},
    {"id": 22, "nombre": "Emilio Cabrera", "edad": 49, "dni": "13141516V"},
    {"id": 23, "nombre": "Teresa León", "edad": 42, "dni": "14151617W"},
    {"id": 24, "nombre": "Fernando Blanco", "edad": 38, "dni": "15161718X"},
    {"id": 25, "nombre": "Beatriz Romero", "edad": 35, "dni": "16171819Y"},
    {"id": 26, "nombre": "Pablo Herrera", "edad": 46, "dni": "17181920Z"},
    {"id": 27, "nombre": "Natalia Cano", "edad": 29, "dni": "18192021A"},
    {"id": 28, "nombre": "Óscar Serrano", "edad": 50, "dni": "19202122B"},
    {"id": 29, "nombre": "Elena Ruiz", "edad": 33, "dni": "20212223C"},
    {"id": 30, "nombre": "Gabriel Vidal", "edad": 39, "dni": "21222324D"},
]

medicos = [
    {"id": 1, "nombre": "Dr. José Sánchez", "especialidad": "Cardiología"},
    {"id": 2, "nombre": "Dra. Marta González", "especialidad": "Pediatría"},
    {"id": 3, "nombre": "Dr. Luis Romero", "especialidad": "Neurología"},
    {"id": 4, "nombre": "Dra. Ana Torres", "especialidad": "Dermatología"},
    {"id": 5, "nombre": "Dr. Juan Pérez", "especialidad": "Traumatología"},
    {"id": 6, "nombre": "Dra. Laura Rivas", "especialidad": "Ginecología"},
    {"id": 7, "nombre": "Dr. Alberto López", "especialidad": "Psiquiatría"},
    {"id": 8, "nombre": "Dr. Enrique Ortega", "especialidad": "Oftalmología"},
    {"id": 9, "nombre": "Dra. Paula Navarro", "especialidad": "Oncología"},
    {"id": 10, "nombre": "Dr. Javier Marín", "especialidad": "Endocrinología"},
]

citas = [
    {"id": 1, "paciente": "Ana López", "medico": "Dr. José Sánchez", "fecha": "2025-11-04", "motivo": "Chequeo anual"},
    {"id": 2, "paciente": "Carlos Ramírez", "medico": "Dra. Marta González", "fecha": "2025-11-05", "motivo": "Dolor de garganta"},
    {"id": 3, "paciente": "María Pérez", "medico": "Dr. Luis Romero", "fecha": "2025-11-06", "motivo": "Dolor de cabeza"},
    {"id": 4, "paciente": "Lucía Fernández", "medico": "Dra. Ana Torres", "fecha": "2025-11-07", "motivo": "Revisión dermatológica"},
    {"id": 5, "paciente": "José Martínez", "medico": "Dr. Juan Pérez", "fecha": "2025-11-08", "motivo": "Lesión muscular"},
    {"id": 6, "paciente": "Laura Ruiz", "medico": "Dra. Laura Rivas", "fecha": "2025-11-09", "motivo": "Control ginecológico"},
    {"id": 7, "paciente": "David Torres", "medico": "Dr. Alberto López", "fecha": "2025-11-10", "motivo": "Ansiedad"},
    {"id": 8, "paciente": "Antonio García", "medico": "Dr. Enrique Ortega", "fecha": "2025-11-11", "motivo": "Problemas de visión"},
    {"id": 9, "paciente": "Marta Castillo", "medico": "Dra. Paula Navarro", "fecha": "2025-11-12", "motivo": "Seguimiento oncológico"},
    {"id": 10, "paciente": "Rosa Morales", "medico": "Dr. Javier Marín", "fecha": "2025-11-13", "motivo": "Chequeo endocrino"},
]

# ======================================================
# ENDPOINTS DE API
# ======================================================

@app.route("/api/pacientes", methods=["GET"])
def get_pacientes():
    return jsonify(pacientes)

@app.route("/api/medicos", methods=["GET"])
def get_medicos():
    return jsonify(medicos)

@app.route("/api/citas", methods=["GET"])
def get_citas():
    return jsonify(citas)

# ================== AÑADIR (POST) ====================

@app.route("/api/pacientes", methods=["POST"])
def add_paciente():
    data = request.get_json()
    nuevo = {
        "id": len(pacientes) + 1,
        "nombre": data.get("nombre"),
        "edad": data.get("edad"),
        "dni": data.get("dni")
    }
    pacientes.append(nuevo)
    return jsonify({"message": "✅ Paciente añadido correctamente", "paciente": nuevo}), 201

@app.route("/api/medicos", methods=["POST"])
def add_medico():
    data = request.get_json()
    nuevo = {
        "id": len(medicos) + 1,
        "nombre": data.get("nombre"),
        "especialidad": data.get("especialidad")
    }
    medicos.append(nuevo)
    return jsonify({"message": "✅ Médico añadido correctamente", "medico": nuevo}), 201

@app.route("/api/citas", methods=["POST"])
def add_cita():
    data = request.get_json()
    nuevo = {
        "id": len(citas) + 1,
        "paciente": data.get("paciente"),
        "medico": data.get("medico"),
        "fecha": data.get("fecha"),
        "motivo": data.get("motivo")
    }
    citas.append(nuevo)
    return jsonify({"message": "✅ Cita añadida correctamente", "cita": nuevo}), 201

# ======================================================
# ENDPOINT IA PREDICTIVA
# ======================================================
@app.route("/api/predict", methods=["GET"])
def predict():
    """
    Simula una predicción basada en los datos actuales.
    Ejemplo: si hay muchas citas por médico, alerta de saturación.
    """
    num_pacientes = len(pacientes)
    num_medicos = len(medicos)
    num_citas = len(citas)

    if num_medicos == 0:
        prediccion = "⚠️ No hay médicos disponibles."
        mensaje = "Añada médicos para atender las citas."
    else:
        carga = num_citas / num_medicos
        if carga < 3:
            prediccion = "✅ Hospital estable"
            mensaje = f"Carga media por médico: {carga:.2f} citas."
        elif carga < 6:
            prediccion = "⚠️ Alta demanda"
            mensaje = f"Carga media por médico: {carga:.2f} citas. Se recomienda incorporar más personal."
        else:
            prediccion = "🚨 Riesgo de colapso"
            mensaje = f"Cada médico tiene más de {carga:.2f} citas en promedio."

    return jsonify({
        "prediccion": prediccion,
        "mensaje": mensaje,
        "num_pacientes": num_pacientes,
        "num_medicos": num_medicos,
        "num_citas": num_citas
    })

# ======================================================
# RUTA PRINCIPAL PARA MOSTRAR LA WEB
# ======================================================
@app.route("/")
def home():
    return send_from_directory("static", "index.html")

# ======================================================
# MAIN
# ======================================================
if __name__ == "__main__":
    app.run(debug=True, port=5000)