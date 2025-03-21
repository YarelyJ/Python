document.addEventListener("DOMContentLoaded", () => {
    console.log("Script cargado correctamente.");
    cargarTareas();
    document.getElementById("formTarea").addEventListener("submit", agregarTarea);
});

function obtenerTareas() {
    return JSON.parse(localStorage.getItem("tareas")) || [];
}

function guardarTareas(tareas) {
    localStorage.setItem("tareas", JSON.stringify(tareas));
}

function cargarTareas() {
    const lista = document.getElementById("listaTareas");
    lista.innerHTML = ""; // Limpiar la lista antes de cargar las tareas
    const tareas = obtenerTareas();
    
    console.log("Cargando tareas:", tareas);

    tareas.forEach((tarea, index) => {
        mostrarTarea(tarea, index);
    });
}

// Función para calcular el color de la tarea según la fecha
function calcularColor(fecha) {
    const fechaActual = new Date();
    const fechaTarea = new Date(fecha);

    // Calcular la diferencia de días entre la fecha actual y la fecha de la tarea
    const diferenciaTiempo = fechaTarea - fechaActual;
    const diferenciaDias = diferenciaTiempo / (1000 * 3600 * 24);

    console.log(`Diferencia de días para la tarea con fecha ${fecha}:`, diferenciaDias); // Ver la diferencia de días

    // Si la tarea está vencida
    if (diferenciaDias < 0) {
        return 'rojo';
    }
    // Si la tarea vence en los próximos 3 días
    else if (diferenciaDias <= 3) {
        return 'naranja';
    }
    // Si la tarea está a tiempo
    else {
        return 'verde';
    }
}

function mostrarTarea(tarea, index) {
    const div = document.createElement("div");
    div.classList.add("tarea");

    // Calcular el color para la tarea
    const color = calcularColor(tarea.fecha);

    // Crear el punto de color
    const puntoColor = document.createElement("span");
    puntoColor.classList.add("punto", color); // Asignar la clase del color

    // Crear el contenido de la tarea
    div.innerHTML = `
        <span>${tarea.nombre} - ${tarea.fecha}</span>
        <button onclick="editarTarea(${index})">✏️</button>
        <button onclick="eliminarTarea(${index})">❌</button>
    `;
    
    // Agregar el punto de color antes de la tarea
    div.prepend(puntoColor);

    document.getElementById("listaTareas").appendChild(div);
}

function agregarTarea(e) {
    e.preventDefault();
    const nombre = document.getElementById("nombre").value.trim();
    const fecha = document.getElementById("fecha").value;

    if (!nombre || !fecha) {
        alert("Por favor, completa todos los campos.");
        return;
    }

    const tareas = obtenerTareas();
    tareas.push({ nombre, fecha });
    guardarTareas(tareas);
    cargarTareas();
    document.getElementById("formTarea").reset();
}

function eliminarTarea(index) {
    const tareas = obtenerTareas();
    tareas.splice(index, 1);
    guardarTareas(tareas);
    cargarTareas();
}

function editarTarea(index) {
    const tareas = obtenerTareas();
    const nuevoNombre = prompt("Editar tarea", tareas[index].nombre);
    const nuevaFecha = prompt("Editar fecha (YYYY-MM-DD)", tareas[index].fecha);
    
    if (nuevoNombre && nuevaFecha) {
        tareas[index] = { nombre: nuevoNombre, fecha: nuevaFecha };
        guardarTareas(tareas);
        cargarTareas();
    }
}

