document.addEventListener("DOMContentLoaded", () => {

    // ===========================
    // ELEMENTOS DEL DOM
    // ===========================

    const form = document.getElementById("notaForm");
    const nombre = document.getElementById("nombre");
    const descripcion = document.getElementById("descripcion");
    const categoria = document.getElementById("categoria");

    const lista = document.getElementById("listaRegistros");
    const totalRegistros = document.getElementById("totalRegistros");
    const mensajeValidacion = document.getElementById("mensajeValidacion");
    const contadorGeneral = document.getElementById("contadorGeneral");
    const listaServicios = document.getElementById("listaServicios");

    // ===========================
    // SERVICIOS DINÁMICOS
    // ===========================

    const servicios = [

        {
            titulo: "Registro de Notas",
            descripcion: "Registro de calificaciones por asignatura y parcial."
        },

        {
            titulo: "Consulta Estudiantil",
            descripcion: "Consulta inmediata de notas y promedios."
        },

        {
            titulo: "Reportes PDF",
            descripcion: "Generación automática de reportes académicos."
        },

        {
            titulo: "Cálculo Automático",
            descripcion: "Promedios calculados automáticamente."
        }

    ];

    function renderizarServicios() {

        listaServicios.innerHTML = "";

        servicios.forEach(servicio => {

            listaServicios.innerHTML += `

            <div class="col-md-6 col-lg-3">

                <div class="card h-100 text-center p-3">

                    <div class="card-body">

                        <h5 class="card-title">
                            ${servicio.titulo}
                        </h5>

                        <p class="card-text">
                            ${servicio.descripcion}
                        </p>

                    </div>

                </div>

            </div>

            `;

        });

    }

    renderizarServicios();

    // ===========================
    // LOCAL STORAGE
    // ===========================

    let registros =
        JSON.parse(localStorage.getItem("notas")) || [];

    // ===========================
    // VALIDACIONES
    // ===========================

    function setInvalid(campo, mensaje) {

        campo.classList.remove("is-valid");
        campo.classList.add("is-invalid");

        const feedback = campo.nextElementSibling;

        if (feedback) {

            feedback.textContent = mensaje;

        }

    }

    function setValid(campo) {

        campo.classList.remove("is-invalid");
        campo.classList.add("is-valid");

        const feedback = campo.nextElementSibling;

        if (feedback) {

            feedback.textContent = "";

        }

    }

    function validarNombre() {

        const valor = nombre.value.trim();

        if (valor === "") {

            setInvalid(nombre, "Ingrese un nombre.");
            return false;

        }

        if (valor.length < 3) {

            setInvalid(nombre, "Debe tener mínimo 3 caracteres.");
            return false;

        }

        setValid(nombre);

        return true;

    }

    function validarDescripcion() {

        const valor = descripcion.value.trim();

        if (valor === "") {

            setInvalid(descripcion, "Ingrese una descripción.");
            return false;

        }

        if (valor.length < 10) {

            setInvalid(descripcion, "Debe contener mínimo 10 caracteres.");
            return false;

        }

        setValid(descripcion);

        return true;

    }

    function validarCategoria() {

        if (categoria.value === "") {

            setInvalid(categoria, "Seleccione una categoría.");
            return false;

        }

        setValid(categoria);

        return true;

    }

    nombre.addEventListener("input", validarNombre);
    descripcion.addEventListener("input", validarDescripcion);
    categoria.addEventListener("change", validarCategoria);

    // ===========================
    // REGISTRAR
    // ===========================

    form.addEventListener("submit", (e) => {

        e.preventDefault();

        if (
            validarNombre() &&
            validarDescripcion() &&
            validarCategoria()
        ) {

            const nuevo = {

                id: Date.now(),

                nombre: nombre.value.trim(),

                descripcion: descripcion.value.trim(),

                categoria: categoria.value,

                fecha: new Date().toLocaleDateString()

            };

            registros.push(nuevo);

            localStorage.setItem(
                "notas",
                JSON.stringify(registros)
            );

            renderizar();

            mensajeValidacion.innerHTML =

                `<div class="alert alert-success">

                    Registro guardado correctamente.

                </div>`;

            form.reset();

            nombre.classList.remove("is-valid");
            descripcion.classList.remove("is-valid");
            categoria.classList.remove("is-valid");

        }

        else {

            mensajeValidacion.innerHTML =

                `<div class="alert alert-danger">

                    Corrija los errores del formulario.

                </div>`;

        }

    });

    // ===========================
    // RENDERIZAR REGISTROS
    // ===========================

    function renderizar() {

        lista.innerHTML = "";

        contadorGeneral.textContent =
            "Registros almacenados: " + registros.length;

        totalRegistros.textContent =
            "Total: " + registros.length;

        if (registros.length === 0) {

            lista.innerHTML =

                `<div class="col-12">

                    <div class="alert alert-warning text-center">

                        No existen registros.

                    </div>

                </div>`;

        }

        else {

            registros.forEach(reg => {

                lista.innerHTML += `

                <div class="col-md-6 col-lg-4">

                    <div class="card h-100 border-primary">

                        <div class="card-body">

                            <h5 class="fw-bold">

                                ${reg.nombre}

                            </h5>

                            <span class="badge bg-primary">

                                ${reg.categoria}

                            </span>

                            <hr>

                            <p>

                                ${reg.descripcion}

                            </p>

                            <small class="text-muted">

                                Fecha: ${reg.fecha}

                            </small>

                            <br><br>

                            <button
                                class="btn btn-danger w-100"
                                onclick="eliminar(${reg.id})">

                                Eliminar

                            </button>

                        </div>

                    </div>

                </div>

                `;

            });

        }

        if (registros.length >= 5) {

            mensajeValidacion.innerHTML =

                `<div class="alert alert-info">

                    Ya existen varios registros almacenados.

                </div>`;

        }

    }

    // ===========================
    // ELIMINAR
    // ===========================

    window.eliminar = function(id) {

        registros =
            registros.filter(reg => reg.id !== id);

        localStorage.setItem(
            "notas",
            JSON.stringify(registros)
        );

        renderizar();

    };

    renderizar();

});