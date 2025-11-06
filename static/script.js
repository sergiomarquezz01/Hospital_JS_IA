let pacientes = [];
let medicos = [];
let citas = [];

let graficaPacientes;
let graficaCitas;


window.onload = async () => {
  await cargarDatos();
  initGraficas();
  actualizarGraficas();

  
  setInterval(async () => {
    await cargarDatos();
    actualizarGraficas();
  }, 10000);
};


async function cargarDatos() {
  try {
    const [resPacientes, resMedicos, resCitas] = await Promise.all([
      fetch("/api/pacientes"),
      fetch("/api/medicos"),
      fetch("/api/citas")
    ]);

    pacientes = await resPacientes.json();
    medicos = await resMedicos.json();
    citas = await resCitas.json();

    renderPacientes();
    renderMedicos();
    renderCitas();
  } catch (error) {
    console.error("❌ Error cargando datos:", error);
  }
}


function renderPacientes() {
  const cont = document.getElementById("tabla-pacientes");
  if (!cont) return;
  cont.innerHTML = pacientes.map(p => `
    <tr>
      <td>${p.id}</td>
      <td>${p.nombre}</td>
      <td>${p.edad}</td>
      <td>${p.dni}</td>
    </tr>`).join("");
}

function renderMedicos() {
  const cont = document.getElementById("tabla-medicos");
  if (!cont) return;
  cont.innerHTML = medicos.map(m => `
    <tr>
      <td>${m.id}</td>
      <td>${m.nombre}</td>
      <td>${m.especialidad}</td>
    </tr>`).join("");
}

function renderCitas() {
  const cont = document.getElementById("tabla-citas");
  if (!cont) return;
  cont.innerHTML = citas.map(c => `
    <tr>
      <td>${c.id}</td>
      <td>${c.paciente}</td>
      <td>${c.medico}</td>
      <td>${c.fecha}</td>
      <td>${c.motivo}</td>
    </tr>`).join("");
}


async function agregarPaciente() {
  const nombre = document.getElementById("nombrePaciente").value;
  const edad = parseInt(document.getElementById("edadPaciente").value);
  const dni = document.getElementById("dniPaciente").value;

  if (!nombre || !edad || !dni) return alert("Rellena todos los campos");

  const res = await fetch("/api/pacientes", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ nombre, edad, dni })
  });

  const data = await res.json();
  pacientes.push(data.paciente);

  renderPacientes();
  actualizarGraficas();
  limpiarCampos("paciente");
}


async function agregarMedico() {
  const nombre = document.getElementById("nombreMedico").value;
  const especialidad = document.getElementById("especialidadMedico").value;

  if (!nombre || !especialidad) return alert("Rellena todos los campos");

  const res = await fetch("/api/medicos", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ nombre, especialidad })
  });

  const data = await res.json();
  medicos.push(data.medico);

  renderMedicos();
  actualizarGraficas();
  limpiarCampos("medico");
}


async function agregarCita() {
  const paciente = document.getElementById("pacienteCita").value;
  const medico = document.getElementById("medicoCita").value;
  const fecha = document.getElementById("fechaCita").value;
  const motivo = document.getElementById("motivoCita").value;

  if (!paciente || !medico || !fecha || !motivo)
    return alert("Completa todos los campos");

  const res = await fetch("/api/citas", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ paciente, medico, fecha, motivo })
  });

  const data = await res.json();
  citas.push(data.cita);

  renderCitas();
  actualizarGraficas();
  limpiarCampos("cita");
}


function initGraficas() {
  const ctx1 = document.getElementById('graficaPacientes');
  const ctx2 = document.getElementById('graficaCitas');

  graficaPacientes = new Chart(ctx1, {
    type: 'bar',
    data: {
      labels: ['0-18', '19-40', '41-65', '65+'],
      datasets: [{
        label: 'Pacientes por edad',
        data: [0, 0, 0, 0],
        backgroundColor: '#00a99d'
      }]
    },
    options: { responsive: true }
  });

  graficaCitas = new Chart(ctx2, {
    type: 'pie',
    data: {
      labels: [],
      datasets: [{
        label: 'Citas por médico',
        data: [],
        backgroundColor: ['#00a99d', '#007b7f', '#55c2b8', '#b6ebe6']
      }]
    },
    options: { responsive: true }
  });
}

function actualizarGraficas() {
 
  const edades = [0, 0, 0, 0];
  pacientes.forEach(p => {
    if (p.edad <= 18) edades[0]++;
    else if (p.edad <= 40) edades[1]++;
    else if (p.edad <= 65) edades[2]++;
    else edades[3]++;
  });
  graficaPacientes.data.datasets[0].data = edades;
  graficaPacientes.update();

  
  const conteo = {};
  citas.forEach(c => {
    conteo[c.medico] = (conteo[c.medico] || 0) + 1;
  });
  graficaCitas.data.labels = Object.keys(conteo);
  graficaCitas.data.datasets[0].data = Object.values(conteo);
  graficaCitas.update();
}


function limpiarCampos(tipo) {
  if (tipo === "paciente") {
    document.getElementById("nombrePaciente").value = "";
    document.getElementById("edadPaciente").value = "";
    document.getElementById("dniPaciente").value = "";
  } else if (tipo === "medico") {
    document.getElementById("nombreMedico").value = "";
    document.getElementById("especialidadMedico").value = "";
  } else if (tipo === "cita") {
    document.getElementById("pacienteCita").value = "";
    document.getElementById("medicoCita").value = "";
    document.getElementById("fechaCita").value = "";
    document.getElementById("motivoCita").value = "";
  }
}
