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

    // Spinner Bootstrap
    const spinner = document.getElementById("spinnerCarga");

    // Modal Bootstrap
    const elementoModal = document.getElementById("modalEliminar");

    const modalEliminar = elementoModal
        ? new bootstrap.Modal(elementoModal)
        : null;

    const btnConfirmarEliminar =
        document.getElementById("btnConfirmarEliminar");

    let idEliminar = null;


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

        // Si la página no tiene la sección de servicios,
        // no hacemos nada.

        if (!listaServicios) {
            return;
        }

        listaServicios.innerHTML = "";

        servicios.forEach(servicio => {

            listaServicios.innerHTML += `

                <div class="col-md-6 col-lg-3">

                    <div class="card h-100 shadow">

                        <div class="card-body text-center">

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

        if (!campo) {
            return;
        }

        campo.classList.remove("is-valid");
        campo.classList.add("is-invalid");

        const feedback = campo.nextElementSibling;

        if (feedback) {
            feedback.textContent = mensaje;
        }

    }


    function setValid(campo) {

        if (!campo) {
            return;
        }

        campo.classList.remove("is-invalid");
        campo.classList.add("is-valid");

        const feedback = campo.nextElementSibling;

        if (feedback) {
            feedback.textContent = "";
        }

    }


    function validarNombre() {

        if (!nombre) {
            return false;
        }

        const valor = nombre.value.trim();

        if (valor === "") {

            setInvalid(
                nombre,
                "Ingrese un nombre."
            );

            return false;

        }

        if (valor.length < 3) {

            setInvalid(
                nombre,
                "Debe tener mínimo 3 caracteres."
            );

            return false;

        }

        setValid(nombre);

        return true;

    }


    function validarDescripcion() {

        if (!descripcion) {
            return false;
        }

        const valor = descripcion.value.trim();

        if (valor === "") {

            setInvalid(
                descripcion,
                "Ingrese una descripción."
            );

            return false;

        }

        if (valor.length < 10) {

            setInvalid(
                descripcion,
                "Debe contener mínimo 10 caracteres."
            );

            return false;

        }

        setValid(descripcion);

        return true;

    }


    function validarCategoria() {

        if (!categoria) {
            return false;
        }

        if (categoria.value === "") {

            setInvalid(
                categoria,
                "Seleccione una categoría."
            );

            return false;

        }

        setValid(categoria);

        return true;

    }


    // ===========================
    // EVENTOS DE VALIDACIÓN
    // ===========================

    if (nombre) {

        nombre.addEventListener(
            "input",
            validarNombre
        );

    }


    if (descripcion) {

        descripcion.addEventListener(
            "input",
            validarDescripcion
        );

    }


    if (categoria) {

        categoria.addEventListener(
            "change",
            validarCategoria
        );

    }


    // ===========================
    // REGISTRO CON SPINNER
    // ===========================

    if (form) {

        form.addEventListener("submit", (e) => {

            e.preventDefault();


            if (
                validarNombre() &&
                validarDescripcion() &&
                validarCategoria()
            ) {

                // Mostrar spinner

                if (spinner) {
                    spinner.classList.remove("d-none");
                }


                setTimeout(() => {

                    // Ocultar spinner

                    if (spinner) {
                        spinner.classList.add("d-none");
                    }


                    // Crear nuevo registro

                    const nuevo = {

                        id: Date.now(),

                        nombre: nombre.value.trim(),

                        descripcion:
                            descripcion.value.trim(),

                        categoria:
                            categoria.value,

                        fecha:
                            new Date().toLocaleDateString()

                    };


                    // Guardar registro

                    registros.push(nuevo);


                    localStorage.setItem(
                        "notas",
                        JSON.stringify(registros)
                    );


                    // Actualizar pantalla

                    renderizar();


                    // Mostrar mensaje

                    if (mensajeValidacion) {

                        mensajeValidacion.innerHTML = `

                            <div
                                class="alert alert-success alert-dismissible fade show"
                                role="alert">

                                <strong>¡Éxito!</strong>
                                Registro guardado correctamente.

                                <button
                                    type="button"
                                    class="btn-close"
                                    data-bs-dismiss="alert">
                                </button>

                            </div>

                        `;


                        setTimeout(() => {

                            mensajeValidacion.innerHTML = "";

                        }, 3000);

                    }


                    // Limpiar formulario

                    form.reset();


                    nombre.classList.remove(
                        "is-valid"
                    );

                    descripcion.classList.remove(
                        "is-valid"
                    );

                    categoria.classList.remove(
                        "is-valid"
                    );


                }, 1500);

            }

            else {

                if (mensajeValidacion) {

                    mensajeValidacion.innerHTML = `

                        <div
                            class="alert alert-danger alert-dismissible fade show"
                            role="alert">

                            <strong>Error.</strong>
                            Corrija los errores del formulario.

                            <button
                                type="button"
                                class="btn-close"
                                data-bs-dismiss="alert">
                            </button>

                        </div>

                    `;


                    setTimeout(() => {

                        mensajeValidacion.innerHTML = "";

                    }, 3000);

                }

            }

        });

    }


    // ===========================
    // RENDERIZAR REGISTROS
    // ===========================

    function renderizar() {

        // Si estamos en otra página,
        // no intentamos renderizar registros.

        if (!lista) {
            return;
        }


        lista.innerHTML = "";


        // Contador general

        if (contadorGeneral) {

            contadorGeneral.textContent =
                "Registros almacenados: "
                + registros.length;

        }


        // Total de registros

        if (totalRegistros) {

            totalRegistros.textContent =
                "Total: "
                + registros.length;

        }


        // No existen registros

        if (registros.length === 0) {

            lista.innerHTML = `

                <div class="col-12">

                    <div class="alert alert-warning text-center">

                        No existen registros.

                    </div>

                </div>

            `;

        }

        else {

            // Mostrar registros

            registros.forEach(reg => {

                lista.innerHTML += `

                    <div class="col-md-6 col-lg-4">

                        <div
                            class="card h-100 border-primary shadow">

                            <div class="card-body">

                                <h5 class="fw-bold">
                                    ${reg.nombre}
                                </h5>

                                <span
                                    class="badge bg-primary">

                                    ${reg.categoria}

                                </span>

                                <hr>

                                <p>
                                    ${reg.descripcion}
                                </p>

                                <small class="text-muted">

                                    Fecha: ${reg.fecha}

                                </small>

                                <br>
                                <br>

                                <button
                                    class="btn btn-danger w-100"
                                    onclick="abrirModal(${reg.id})">

                                    Eliminar

                                </button>

                            </div>

                        </div>

                    </div>

                `;

            });

        }


        // Mensaje cuando hay muchos registros

        if (registros.length >= 5) {

            if (mensajeValidacion) {

                mensajeValidacion.innerHTML = `

                    <div
                        class="alert alert-info alert-dismissible fade show"
                        role="alert">

                        Ya existen varios registros almacenados.

                        <button
                            type="button"
                            class="btn-close"
                            data-bs-dismiss="alert">
                        </button>

                    </div>

                `;

            }

        }

    }


    // ===========================
    // MODAL ELIMINAR
    // ===========================

    window.abrirModal = function(id) {

        idEliminar = id;


        if (modalEliminar) {

            modalEliminar.show();

        }

    };


    // ===========================
    // CONFIRMAR ELIMINACIÓN
    // ===========================

    if (
        btnConfirmarEliminar &&
        modalEliminar
    ) {

        btnConfirmarEliminar.addEventListener(
            "click",
            () => {

                registros = registros.filter(
                    reg => reg.id !== idEliminar
                );


                localStorage.setItem(
                    "notas",
                    JSON.stringify(registros)
                );


                modalEliminar.hide();


                renderizar();


                if (mensajeValidacion) {

                    mensajeValidacion.innerHTML = `

                        <div
                            class="alert alert-success alert-dismissible fade show"
                            role="alert">

                            Registro eliminado correctamente.

                            <button
                                type="button"
                                class="btn-close"
                                data-bs-dismiss="alert">
                            </button>

                        </div>

                    `;


                    setTimeout(() => {

                        mensajeValidacion.innerHTML = "";

                    }, 3000);

                }

            }
        );

    }


    // ===========================
    // INICIALIZAR
    // ===========================

    renderizar();

});