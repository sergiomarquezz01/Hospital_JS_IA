// ============================
// VARIABLES GLOBALES
// ============================
let seccionActual = "panel";
let pacientes = [];
let medicos = [];
let citas = [];
let chart = null;

// ============================
// FUNCIONES PRINCIPALES
// ============================

async function cargarDatos() {
  try {
    const [resPac, resMed, resCit] = await Promise.all([
      fetch("/api/pacientes"),
      fetch("/api/medicos"),
      fetch("/api/citas"),
    ]);
    pacientes = await resPac.json();
    medicos = await resMed.json();
    citas = await resCit.json();

    mostrarSeccion(seccionActual);
  } catch (err) {
    console.error("Error cargando datos:", err);
  }
}

// ============================
// MOSTRAR SECCIÓN
// ============================
function mostrarSeccion(seccion) {
  seccionActual = seccion;
  const cont = document.getElementById("contenido");
  cont.innerHTML = "";

  if (seccion === "panel") mostrarPanel(cont);
  if (seccion === "pacientes") mostrarPacientes(cont);
  if (seccion === "medicos") mostrarMedicos(cont);
  if (seccion === "citas") mostrarCitas(cont);
}

// ============================
// PANEL PRINCIPAL
// ============================
async function mostrarPanel(cont) {
  cont.innerHTML = `
    <h2>📊 Panel de Control</h2>
    <div class="stats">
      <div class="card">Pacientes: <strong>${pacientes.length}</strong></div>
      <div class="card">Médicos: <strong>${medicos.length}</strong></div>
      <div class="card">Citas: <strong>${citas.length}</strong></div>
    </div>
    <canvas id="grafico" style="max-width:600px; margin-top:20px;"></canvas>
    <div id="prediccionIA" class="ia-box">🤖 Cargando predicción...</div>
  `;

  renderGrafico();
  await mostrarPrediccionIA();
}

async function mostrarPrediccionIA() {
  try {
    const res = await fetch("/api/predict");
    const data = await res.json();
    document.getElementById("prediccionIA").innerHTML = `
      🤖 <strong>IA:</strong> ${data.prediccion} 
      <br><small>(${data.mensaje})</small>
    `;
  } catch (err) {
    document.getElementById("prediccionIA").innerHTML =
      "⚠️ Error al obtener predicción IA.";
  }
}

// ============================
// TABLA PACIENTES
// ============================
function mostrarPacientes(cont) {
  let html = `
    <h2>👨‍⚕️ Pacientes</h2>
    <table>
      <tr><th>ID</th><th>Nombre</th><th>Edad</th><th>DNI</th></tr>
      ${pacientes
        .map(
          (p) =>
            `<tr><td>${p.id}</td><td>${p.nombre}</td><td>${p.edad}</td><td>${p.dni}</td></tr>`
        )
        .join("")}
    </table>

    <h3>➕ Añadir Paciente</h3>
    <input id="nombrePaciente" placeholder="Nombre" />
    <input id="edadPaciente" placeholder="Edad" type="number" />
    <input id="dniPaciente" placeholder="DNI" />
    <button onclick="guardarPaciente()">Guardar</button>
  `;
  cont.innerHTML = html;
}

async function guardarPaciente() {
  const nuevo = {
    nombre: document.getElementById("nombrePaciente").value,
    edad: document.getElementById("edadPaciente").value,
    dni: document.getElementById("dniPaciente").value,
  };

  const res = await fetch("/api/pacientes", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(nuevo),
  });

  if (res.ok) {
    alert("✅ Paciente añadido correctamente");
    cargarDatos();
  } else alert("⚠️ Error al guardar paciente");
}

// ============================
// TABLA MÉDICOS
// ============================
function mostrarMedicos(cont) {
  let html = `
    <h2>🩺 Médicos</h2>
    <table>
      <tr><th>ID</th><th>Nombre</th><th>Especialidad</th></tr>
      ${medicos
        .map(
          (m) =>
            `<tr><td>${m.id}</td><td>${m.nombre}</td><td>${m.especialidad}</td></tr>`
        )
        .join("")}
    </table>

    <h3>➕ Añadir Médico</h3>
    <input id="nombreMedico" placeholder="Nombre" />
    <input id="espMedico" placeholder="Especialidad" />
    <button onclick="guardarMedico()">Guardar</button>
  `;
  cont.innerHTML = html;
}

async function guardarMedico() {
  const nuevo = {
    nombre: document.getElementById("nombreMedico").value,
    especialidad: document.getElementById("espMedico").value,
  };

  const res = await fetch("/api/medicos", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(nuevo),
  });

  if (res.ok) {
    alert("✅ Médico añadido correctamente");
    cargarDatos();
  } else alert("⚠️ Error al guardar médico");
}

// ============================
// TABLA CITAS
// ============================
function mostrarCitas(cont) {
  let html = `
    <h2>📅 Citas</h2>
    <table>
      <tr><th>ID</th><th>Paciente</th><th>Médico</th><th>Fecha</th><th>Motivo</th></tr>
      ${citas
        .map(
          (c) =>
            `<tr><td>${c.id}</td><td>${c.paciente}</td><td>${c.medico}</td><td>${c.fecha}</td><td>${c.motivo}</td></tr>`
        )
        .join("")}
    </table>

    <h3>➕ Añadir Cita</h3>
    <select id="selPaciente">
      ${pacientes.map((p) => `<option>${p.nombre}</option>`).join("")}
    </select>
    <select id="selMedico">
      ${medicos.map((m) => `<option>${m.nombre}</option>`).join("")}
    </select>
    <input id="fechaCita" type="date" />
    <input id="motivoCita" placeholder="Motivo" />
    <button onclick="guardarCita()">Guardar</button>
  `;
  cont.innerHTML = html;
}

async function guardarCita() {
  const nuevo = {
    paciente: document.getElementById("selPaciente").value,
    medico: document.getElementById("selMedico").value,
    fecha: document.getElementById("fechaCita").value,
    motivo: document.getElementById("motivoCita").value,
  };

  const res = await fetch("/api/citas", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(nuevo),
  });

  if (res.ok) {
    alert("✅ Cita añadida correctamente");
    cargarDatos();
  } else alert("⚠️ Error al guardar cita");
}

// ============================
// GRÁFICO DE ESTADÍSTICAS
// ============================
function renderGrafico() {
  const ctx = document.getElementById("grafico");
  if (chart) chart.destroy();
  chart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["Pacientes", "Médicos", "Citas"],
      datasets: [
        {
          label: "Totales",
          data: [pacientes.length, medicos.length, citas.length],
          backgroundColor: ["#4CAF50", "#2196F3", "#FFC107"],
        },
      ],
    },
  });
}

// ============================
// BUSCADOR Y FILTROS
// ============================
function buscar() {
  const texto = document.getElementById("searchInput").value.toLowerCase();
  if (seccionActual === "pacientes") {
    const filtrados = pacientes.filter((p) =>
      p.nombre.toLowerCase().includes(texto)
    );
    renderTablaFiltrada(filtrados, "pacientes");
  }
}

function renderTablaFiltrada(lista, tipo) {
  const cont = document.getElementById("contenido");
  if (tipo === "pacientes") {
    cont.innerHTML = `
      <h2>Resultados (${lista.length})</h2>
      <table>
        <tr><th>ID</th><th>Nombre</th><th>Edad</th><th>DNI</th></tr>
        ${lista
          .map(
            (p) =>
              `<tr><td>${p.id}</td><td>${p.nombre}</td><td>${p.edad}</td><td>${p.dni}</td></tr>`
          )
          .join("")}
      </table>
    `;
  }
}

// ==================== ESTADÍSTICAS (GRÁFICAS) ==================== //
function mostrarEstadisticas() {
  document.getElementById("contenido").innerHTML = `
    <h2>📈 Estadísticas Hospitalarias</h2>
    <div class="graficos">
      <canvas id="graficoPacientes" width="400" height="200"></canvas>
      <canvas id="graficoCitasPorMedico" width="400" height="200"></canvas>
      <canvas id="graficoMotivos" width="400" height="200"></canvas>
      <canvas id="graficoEdades" width="400" height="200"></canvas>
    </div>
  `;

  Promise.all([
    fetch("/api/pacientes").then(r => r.json()),
    fetch("/api/medicos").then(r => r.json()),
    fetch("/api/citas").then(r => r.json())
  ]).then(([pacientes, medicos, citas]) => {
    // --- Gráfico 1: Edad de pacientes (histograma)
    const edades = pacientes.map(p => p.edad);
    new Chart(document.getElementById("graficoEdades"), {
      type: "bar",
      data: {
        labels: edades.map((_, i) => "Paciente " + (i + 1)),
        datasets: [{
          label: "Edad de los pacientes",
          data: edades,
          borderWidth: 1,
          backgroundColor: "rgba(75, 192, 192, 0.6)"
        }]
      },
      options: { responsive: true }
    });

    // --- Gráfico 2: Citas por médico (barras)
    const conteo = {};
    citas.forEach(c => {
      conteo[c.medico] = (conteo[c.medico] || 0) + 1;
    });
    new Chart(document.getElementById("graficoCitasPorMedico"), {
      type: "bar",
      data: {
        labels: Object.keys(conteo),
        datasets: [{
          label: "Número de citas por médico",
          data: Object.values(conteo),
          backgroundColor: "rgba(255, 159, 64, 0.7)"
        }]
      },
      options: { responsive: true }
    });

    // --- Gráfico 3: Motivos de cita (queso/pie)
    const motivos = {};
    citas.forEach(c => {
      motivos[c.motivo] = (motivos[c.motivo] || 0) + 1;
    });
    new Chart(document.getElementById("graficoMotivos"), {
      type: "pie",
      data: {
        labels: Object.keys(motivos),
        datasets: [{
          data: Object.values(motivos),
          backgroundColor: [
            "#FF6384", "#36A2EB", "#FFCE56", "#8BC34A", "#9C27B0"
          ]
        }]
      },
      options: { responsive: true }
    });

    // --- Gráfico 4: Pacientes por grupo de edad (histograma)
    const grupos = { "0-20": 0, "21-40": 0, "41-60": 0, "61+": 0 };
    pacientes.forEach(p => {
      if (p.edad <= 20) grupos["0-20"]++;
      else if (p.edad <= 40) grupos["21-40"]++;
      else if (p.edad <= 60) grupos["41-60"]++;
      else grupos["61+"]++;
    });
    new Chart(document.getElementById("graficoPacientes"), {
      type: "bar",
      data: {
        labels: Object.keys(grupos),
        datasets: [{
          label: "Pacientes por grupo de edad",
          data: Object.values(grupos),
          backgroundColor: "rgba(153, 102, 255, 0.6)"
        }]
      },
      options: { responsive: true }
    });
  });
}

// ==================== NUEVA SECCIÓN ==================== //
function mostrarSeccion(seccion) {
  if (seccion === "estadisticas") {
    mostrarEstadisticas();
    return;
  }
  // Mantiene el comportamiento anterior
  const main = document.getElementById("contenido");
  if (seccion === "panel") main.innerHTML = `<h2>Panel de Control</h2><p>Bienvenido al Hospital Málaga.</p>`;
  else if (seccion === "pacientes") cargarPacientes();
  else if (seccion === "medicos") cargarMedicos();
  else if (seccion === "citas") cargarCitas();
}

// ============================
// MODO OSCURO
// ============================
function toggleDark() {
  document.body.classList.toggle("dark");
}

// ============================
// INICIO
// ============================
cargarDatos();


