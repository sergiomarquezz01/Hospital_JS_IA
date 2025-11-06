from flask import Flask, jsonify, request, send_from_directory
from faker import Faker
import random
import csv
import os

app = Flask(__name__, static_folder="static", static_url_path="/static")

# ======================================================
# DATOS SIMULADOS REALISTAS DE UN HOSPITAL
# ======================================================
fake = Faker("es_ES")

especialidades = [
    "Cardiología", "Pediatría", "Neurología", "Traumatología",
    "Dermatología", "Psiquiatría", "Oncología", "Ginecología",
    "Urología", "Oftalmología", "Endocrinología", "Neumología"
]

# Médicos simulados
medicos = [
    {
        "id": i + 1,
        "nombre": fake.name(),
        "especialidad": random.choice(especialidades)
    }
    for i in range(350)
]

# Pacientes simulados
pacientes = [
    {
        "id": i + 1,
        "nombre": fake.name(),
        "edad": random.randint(0, 95),
        "dni": fake.random_number(digits=8, fix_len=True)
    }
    for i in range(1500)
]

# Citas simuladas
citas = [
    {
        "id": i + 1,
        "paciente": random.choice(pacientes)["nombre"],
        "medico": random.choice(medicos)["nombre"],
        "fecha": str(fake.date_this_year()),
        "motivo": random.choice([
            "Revisión general", "Dolor de cabeza", "Consulta anual",
            "Chequeo de presión", "Vacunación", "Dolor abdominal"
        ])
    }
    for i in range(2000)
]

print(f"✅ Datos simulados generados: {len(medicos)} médicos, {len(pacientes)} pacientes y {len(citas)} citas.")


# ======================================================
# ENDPOINTS DE LA API
# ======================================================

@app.route("/api/pacientes", methods=["GET", "POST"])
def api_pacientes():
    if request.method == "POST":
        data = request.json
        nuevo = {
            "id": len(pacientes) + 1,
            "nombre": data.get("nombre"),
            "edad": data.get("edad"),
            "dni": data.get("dni")
        }
        pacientes.append(nuevo)
        return jsonify({"message": "✅ Paciente añadido", "paciente": nuevo})
    return jsonify(pacientes)


@app.route("/api/medicos", methods=["GET", "POST"])
def api_medicos():
    if request.method == "POST":
        data = request.json
        nuevo = {
            "id": len(medicos) + 1,
            "nombre": data.get("nombre"),
            "especialidad": data.get("especialidad")
        }
        medicos.append(nuevo)
        return jsonify({"message": "✅ Médico añadido", "medico": nuevo})
    return jsonify(medicos)


@app.route("/api/citas", methods=["GET", "POST"])
def api_citas():
    if request.method == "POST":
        data = request.json
        nuevo = {
            "id": len(citas) + 1,
            "paciente": data.get("paciente"),
            "medico": data.get("medico"),
            "fecha": data.get("fecha"),
            "motivo": data.get("motivo")
        }
        citas.append(nuevo)
        return jsonify({"message": "✅ Cita añadida", "cita": nuevo})
    return jsonify(citas)


# ======================================================
# EXPORTACIÓN A CSV
# ======================================================

@app.route("/api/exportar/<string:tipo>")
def exportar_csv(tipo):
    filename = f"export_{tipo}.csv"
    ruta = os.path.join(os.getcwd(), filename)

    if tipo == "pacientes":
        campos = ["id", "nombre", "edad", "dni"]
        datos = pacientes
    elif tipo == "medicos":
        campos = ["id", "nombre", "especialidad"]
        datos = medicos
    elif tipo == "citas":
        campos = ["id", "paciente", "medico", "fecha", "motivo"]
        datos = citas
    else:
        return jsonify({"error": "Tipo no válido"}), 400

    with open(ruta, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(datos)

    return send_from_directory(os.getcwd(), filename, as_attachment=True)


# ======================================================
# RUTA PRINCIPAL (Frontend)
# ======================================================
@app.route("/")
def home():
    return app.send_static_file("index.html")


# ======================================================
# EJECUCIÓN
# ======================================================
if __name__ == "__main__":
    app.run(debug=True, port=5000)
