from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_cors import CORS
import random
import io
import pandas as pd

app = Flask(__name__, static_folder="static", static_url_path="/static")
CORS(app)

# ======================================================
# DATOS SIMULADOS DE LA BASE DE DATOS
# ======================================================

pacientes = [
    {"id": 1, "nombre": "Laura Gómez", "edad": 32, "dni": "12345678A"},
    {"id": 2, "nombre": "Carlos Ruiz", "edad": 41, "dni": "98765432B"},
    {"id": 3, "nombre": "María López", "edad": 29, "dni": "45612378C"},
    {"id": 4, "nombre": "Javier Ortega", "edad": 52, "dni": "74125896D"},
    {"id": 5, "nombre": "Sofía Molina", "edad": 38, "dni": "85296374E"},
    {"id": 6, "nombre": "Antonio Herrera", "edad": 65, "dni": "96374125F"},
    {"id": 7, "nombre": "Lucía Fernández", "edad": 27, "dni": "35795128G"},
    {"id": 8, "nombre": "Pedro Gutiérrez", "edad": 45, "dni": "15975364H"},
    {"id": 9, "nombre": "Raquel Pérez", "edad": 36, "dni": "25874196I"},
    {"id": 10, "nombre": "Diego Navarro", "edad": 54, "dni": "75395146J"},
    {"id": 11, "nombre": "Elena Vargas", "edad": 22, "dni": "10293847K"},
    {"id": 12, "nombre": "Gabriel Soto", "edad": 70, "dni": "47382910L"},
    {"id": 13, "nombre": "Irene Torres", "edad": 48, "dni": "65432109M"},
    {"id": 14, "nombre": "Marcos Gil", "edad": 33, "dni": "34567890N"},
    {"id": 15, "nombre": "Nerea Rivas", "edad": 59, "dni": "78901234O"},
    {"id": 16, "nombre": "Óscar Prieto", "edad": 25, "dni": "21098765P"},
    {"id": 17, "nombre": "Paula Castro", "edad": 61, "dni": "56789012Q"},
    {"id": 18, "nombre": "Quique Sanz", "edad": 19, "dni": "89012345R"},
    {"id": 19, "nombre": "Rosa Fuentes", "edad": 44, "dni": "11223344S"},
    {"id": 20, "nombre": "Samuel León", "edad": 50, "dni": "99887766T"},
    {"id": 21, "nombre": "Teresa Mora", "edad": 30, "dni": "54321098U"},
    {"id": 22, "nombre": "Vicente Cruz", "edad": 75, "dni": "87654321V"},
    {"id": 23, "nombre": "Yolanda Salas", "edad": 28, "dni": "23456789W"},
    {"id": 24, "nombre": "Ángel Martín", "edad": 49, "dni": "67890123X"},
    {"id": 25, "nombre": "Berta Díaz", "edad": 56, "dni": "13579246Y"},
    {"id": 26, "nombre": "Camilo Vera", "edad": 39, "dni": "97531864Z"},
    {"id": 27, "nombre": "Diana Lemos", "edad": 68, "dni": "36925814A"},
    {"id": 28, "nombre": "Ernesto Ramos", "edad": 24, "dni": "70147258B"},
    {"id": 29, "nombre": "Fátima Noguera", "edad": 51, "dni": "48291037C"},
    {"id": 30, "nombre": "Gonzalo Ferrer", "edad": 43, "dni": "91028374D"},
    {"id": 31, "nombre": "Héctor Vidal", "edad": 35, "dni": "62738495E"},
    {"id": 32, "nombre": "Inés Bravo", "edad": 63, "dni": "19283746F"},
    {"id": 33, "nombre": "Juan Gallardo", "edad": 26, "dni": "53421678G"},
    {"id": 34, "nombre": "Kira Montes", "edad": 40, "dni": "84756910H"},
    {"id": 35, "nombre": "Leo Núñez", "edad": 72, "dni": "26173849I"},
    {"id": 36, "nombre": "Mónica Rico", "edad": 31, "dni": "70392817J"},
    {"id": 37, "nombre": "Nico Alarcón", "edad": 57, "dni": "45670123K"},
    {"id": 38, "nombre": "Olga Benítez", "edad": 20, "dni": "90123456L"},
    {"id": 39, "nombre": "Pablo Moya", "edad": 69, "dni": "34567891M"},
    {"id": 40, "nombre": "Queralt Marín", "edad": 46, "dni": "12345670N"},
    {"id": 41, "nombre": "Ramón Soto", "edad": 55, "dni": "87654320O"},
    {"id": 42, "nombre": "Sara Pardo", "edad": 23, "dni": "21098760P"},
    {"id": 43, "nombre": "Tomás Heredia", "edad": 60, "dni": "56789010Q"},
    {"id": 44, "nombre": "Úrsula Vives", "edad": 37, "dni": "89012340R"},
    {"id": 45, "nombre": "Víctor Melián", "edad": 71, "dni": "11223340S"},
    {"id": 46, "nombre": "Wendy Roca", "edad": 42, "dni": "99887760T"},
    {"id": 47, "nombre": "Xavi Ferrer", "edad": 34, "dni": "54321090U"},
    {"id": 48, "nombre": "Yurena Gil", "edad": 66, "dni": "87654320V"},
    {"id": 49, "nombre": "Zoe Pardo", "edad": 21, "dni": "23456780W"},
    {"id": 50, "nombre": "Adrián Santos", "edad": 53, "dni": "67890120X"},
    {"id": 51, "nombre": "Blanca Ramos", "edad": 47, "dni": "13579240Y"},
    {"id": 52, "nombre": "César Montes", "edad": 62, "dni": "97531860Z"},
    {"id": 53, "nombre": "Dana Vidal", "edad": 27, "dni": "36925810A"},
    {"id": 54, "nombre": "Elías Bravo", "edad": 73, "dni": "70147250B"},
    {"id": 55, "nombre": "Gema Rojas", "edad": 38, "dni": "48291030C"},
    {"id": 56, "nombre": "Hugo Déniz", "edad": 58, "dni": "91028370D"},
    {"id": 57, "nombre": "Iris Soler", "edad": 29, "dni": "62738490E"},
    {"id": 58, "nombre": "Joel Pérez", "edad": 64, "dni": "19283740F"},
    {"id": 59, "nombre": "Lidia Torres", "edad": 33, "dni": "53421670G"},
    {"id": 60, "nombre": "Mario Vega", "edad": 50, "dni": "84756910H"},
]
medicos = [
    {"id": 1, "nombre": "Dr. Manuel Torres", "especialidad": "Cardiología"},
    {"id": 2, "nombre": "Dra. Ana López", "especialidad": "Pediatría"},
    {"id": 3, "nombre": "Dr. Jorge Sánchez", "especialidad": "Neurología"},
    {"id": 4, "nombre": "Dra. Carmen Díaz", "especialidad": "Dermatología"},
    {"id": 5, "nombre": "Dr. José Martín", "especialidad": "Traumatología"},
    {"id": 6, "nombre": "Dra. Silvia Moreno", "especialidad": "Oncología"},
    {"id": 7, "nombre": "Dr. Luis Pérez", "especialidad": "Psiquiatría"},
    {"id": 8, "nombre": "Dra. Marta González", "especialidad": "Ginecología"},
    {"id": 9, "nombre": "Dr. Enrique Rojas", "especialidad": "Urología"},
    {"id": 10, "nombre": "Dra. Clara Navarro", "especialidad": "Medicina Interna"},
    {"id": 11, "nombre": "Dr. Ricardo Vega", "especialidad": "Oftalmología"},
    {"id": 12, "nombre": "Dra. Elena Rubio", "especialidad": "Endocrinología"},
    {"id": 13, "nombre": "Dr. Pablo Gil", "especialidad": "Neumología"},
    {"id": 14, "nombre": "Dra. Isabel Castro", "especialidad": "Reumatología"},
    {"id": 15, "nombre": "Dr. Francisco Soler", "especialidad": "Cirugía General"},
    {"id": 16, "nombre": "Dra. Victoria Rey", "especialidad": "Hematología"},
    {"id": 17, "nombre": "Dr. Andrés Molina", "especialidad": "Nefrología"},
    {"id": 18, "nombre": "Dra. Nuria Prieto", "especialidad": "Otorrinolaringología"},
    {"id": 19, "nombre": "Dr. Sergio Bravo", "especialidad": "Gastroenterología"},
    {"id": 20, "nombre": "Dra. Rosa Jiménez", "especialidad": "Anestesiología"},
]


citas = []
for i in range(1, 61):  
    paciente = random.choice(pacientes)
    medico = random.choice(medicos)
    citas.append({
        "id": i,
        "paciente": paciente["nombre"],
        "medico": medico["nombre"],
        "fecha": f"2025-11-{random.randint(1, 30):02d}",
        "motivo": random.choice(["Revisión", "Dolor", "Consulta general", "Seguimiento", "Análisis", "Vacunación"])
    })



@app.route("/")
def home():
    return send_from_directory("static", "index.html")

@app.route("/api/pacientes", methods=["GET", "POST"])
def handle_pacientes():
    if request.method == "POST":
        data = request.get_json()
        nuevo = {
            "id": len(pacientes) + 1,
            "nombre": data["nombre"],
            "edad": data["edad"],
            "dni": data["dni"]
        }
        pacientes.append(nuevo)
        return jsonify({"message": "Paciente añadido", "paciente": nuevo}), 201
    return jsonify(pacientes)

@app.route("/api/medicos", methods=["GET", "POST"])
def handle_medicos():
    if request.method == "POST":
        data = request.get_json()
        nuevo = {
            "id": len(medicos) + 1,
            "nombre": data["nombre"],
            "especialidad": data["especialidad"]
        }
        medicos.append(nuevo)
        return jsonify({"message": "Médico añadido", "medico": nuevo}), 201
    return jsonify(medicos)

@app.route("/api/citas", methods=["GET", "POST"])
def handle_citas():
    if request.method == "POST":
        data = request.get_json()
        nuevo = {
            "id": len(citas) + 1,
            "paciente": data["paciente"],
            "medico": data["medico"],
            "fecha": data["fecha"],
            "motivo": data["motivo"]
        }
        citas.append(nuevo)
        return jsonify({"message": "Cita añadida", "cita": nuevo}), 201
    return jsonify(citas)

@app.route("/api/predict", methods=["GET"])
def predict_ia():
    num_citas = len(citas)
    num_medicos = len(medicos)
    num_pacientes = len(pacientes)

    if num_medicos == 0:
        nivel = 0
    else:
        nivel = min(1.0, num_citas / (num_medicos * 5))

    if nivel < 0.4:
        estado, color = "Bajo", "green"
    elif nivel < 0.7:
        estado, color = "Moderado", "orange"
    else:
        estado, color = "Alto", "red"

    return jsonify({
        "nivel": nivel,
        "estado": estado,
        "color": color,
        "num_citas": num_citas,
        "num_medicos": num_medicos,
        "num_pacientes": num_pacientes
    })

@app.route("/api/export/<tipo>")
def exportar(tipo):
    buffer = io.BytesIO()
    df_pacientes = pd.DataFrame(pacientes)
    df_medicos = pd.DataFrame(medicos)
    df_citas = pd.DataFrame(citas)

    if tipo == "excel":
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df_pacientes.to_excel(writer, index=False, sheet_name="Pacientes")
            df_medicos.to_excel(writer, index=False, sheet_name="Medicos")
            df_citas.to_excel(writer, index=False, sheet_name="Citas")
        buffer.seek(0)
        return send_file(buffer, as_attachment=True,
                         download_name="hospital_datos.xlsx",
                         mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    elif tipo == "csv":
        csv_data = io.StringIO()
        csv_data.write("=== PACIENTES ===\n")
        df_pacientes.to_csv(csv_data, index=False)
        csv_data.write("\n=== MÉDICOS ===\n")
        df_medicos.to_csv(csv_data, index=False)
        csv_data.write("\n=== CITAS ===\n")
        df_citas.to_csv(csv_data, index=False)
        csv_data.seek(0)
        return send_file(io.BytesIO(csv_data.getvalue().encode("utf-8")),
                         as_attachment=True, download_name="hospital_datos.csv",
                         mimetype="text/csv")

    else:
        return jsonify({"error": "Formato no válido (usa /excel o /csv)"}), 400


if __name__ == "__main__":
    print("🚀 Servidor corriendo en http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
