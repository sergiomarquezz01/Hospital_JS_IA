# init_db.py
import sqlite3
from datetime import date, timedelta
import os

DB = "hospital.db"
if os.path.exists(DB):
    print("El archivo hospital.db ya existe. Si quieres regenerarlo, bórralo antes.")
    # Uncomment to recreate:
    # os.remove(DB)

conn = sqlite3.connect(DB)
c = conn.cursor()

# Crear tablas
c.executescript("""
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS pacientes (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    edad INTEGER,
    dni TEXT
);

CREATE TABLE IF NOT EXISTS medicos (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    especialidad TEXT,
    telefono TEXT
);

CREATE TABLE IF NOT EXISTS citas (
    id INTEGER PRIMARY KEY,
    paciente_id INTEGER NOT NULL,
    medico_id INTEGER NOT NULL,
    fecha TEXT NOT NULL,
    hora TEXT,
    motivo TEXT,
    FOREIGN KEY(paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE,
    FOREIGN KEY(medico_id) REFERENCES medicos(id) ON DELETE CASCADE
);
""")

# Datos ejemplo: 20 pacientes
pacientes = [
    ("Ana López",34,"12345678A"),("Carlos Ramírez",45,"23456789B"),("María Pérez",29,"34567890C"),
    ("José Martínez",51,"45678901D"),("Lucía Fernández",38,"56789012E"),("Antonio García",47,"67890123F"),
    ("Laura Ruiz",26,"78901234G"),("Pedro Jiménez",60,"89012345H"),("Marta Castillo",31,"90123456I"),
    ("David Torres",41,"01234567J"),("Rosa Morales",33,"11223344L"),("Raúl Díaz",55,"22334455M"),
    ("Elena Navarro",29,"33445566N"),("Andrés Vega",48,"44556677P"),("Sofía Romero",36,"55667788Q"),
    ("Miguel Flores",44,"66778899R"),("Patricia León",28,"77889900S"),("Francisco Ortega",63,"88990011T"),
    ("Isabel Herrera",40,"99001122V"),("Javier Molina",50,"10111213W")
]

c.executemany("INSERT INTO pacientes (nombre, edad, dni) VALUES (?, ?, ?);", pacientes)

# 10 médicos
medicos = [
    ("Dr. Juan Pérez","Cardiología","951123001"),
    ("Dra. Marta López","Pediatría","951123002"),
    ("Dr. Antonio Ruiz","Neurología","951123003"),
    ("Dra. Carmen Díaz","Traumatología","951123004"),
    ("Dr. Javier Torres","Medicina Interna","951123005"),
    ("Dra. Isabel García","Ginecología","951123006"),
    ("Dr. Luis Romero","Oncología","951123007"),
    ("Dra. Patricia Ramos","Psiquiatría","951123008"),
    ("Dr. Manuel Castro","Dermatología","951123009"),
    ("Dra. Ana Navarro","Oftalmología","951123010")
]
c.executemany("INSERT INTO medicos (nombre, especialidad, telefono) VALUES (?, ?, ?);", medicos)

# Crear 20 citas distribuidas en los próximos días
# Obtener ids actuales
conn.commit()
c.execute("SELECT id FROM pacientes;")
pac_ids = [row[0] for row in c.fetchall()]
c.execute("SELECT id FROM medicos;")
med_ids = [row[0] for row in c.fetchall()]

start = date.today()
citas = []
hora_base = ["09:00","09:30","10:00","10:30","11:00","11:30","12:00","12:30","15:00","15:30"]
for i in range(20):
    paciente_id = pac_ids[i % len(pac_ids)]
    medico_id = med_ids[i % len(med_ids)]
    fecha = (start + timedelta(days=(i % 14))).isoformat()
    hora = hora_base[i % len(hora_base)]
    motivo = ["Revisión","Control","Dolor","Seguimiento","Consulta"][i % 5] + f" #{i+1}"
    citas.append((paciente_id, medico_id, fecha, hora, motivo))

c.executemany("INSERT INTO citas (paciente_id, medico_id, fecha, hora, motivo) VALUES (?, ?, ?, ?, ?);", citas)

conn.commit()
conn.close()
print("Base de datos hospital.db creada y población inicial insertada.")
