document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('notaForm');
  const nombre = document.getElementById('nombre');
  const descripcion = document.getElementById('descripcion');
  const categoria = document.getElementById('categoria');
  const lista = document.getElementById('listaRegistros');
  const totalRegistros = document.getElementById('totalRegistros');
  const mensajeValidacion = document.getElementById('mensajeValidacion');

  let registros = JSON.parse(localStorage.getItem('notas')) || [];

  function setInvalid(campo, mensaje) {
    campo.classList.add('is-invalid');
    campo.classList.remove('is-valid');
    let feedback = campo.nextElementSibling;
    if(feedback) feedback.textContent = mensaje;
  }

  function setValid(campo) {
    campo.classList.remove('is-invalid');
    campo.classList.add('is-valid');
    let feedback = campo.nextElementSibling;
    if(feedback) feedback.textContent = '';
  }

  const validarNombre = () => {
    const valor = nombre.value.trim();
    if (valor === '') { setInvalid(nombre, 'El nombre es obligatorio.'); return false; }
    if (valor.length < 3) { setInvalid(nombre, 'Mínimo 3 caracteres.'); return false; }
    setValid(nombre); return true;
  }

  const validarDescripcion = () => {
    const valor = descripcion.value.trim();
    if (valor === '') { setInvalid(descripcion, 'La descripción es obligatoria.'); return false; }
    if (valor.length < 10) { setInvalid(descripcion, 'Mínimo 10 caracteres.'); return false; }
    setValid(descripcion); return true;
  }

  const validarCategoria = () => {
    if (categoria.value === '') { setInvalid(categoria, 'Selecciona una categoría.'); return false; }
    setValid(categoria); return true;
  }

  nombre.addEventListener('input', validarNombre);
  descripcion.addEventListener('input', validarDescripcion);
  categoria.addEventListener('change', validarCategoria);

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (validarNombre() && validarDescripcion() && validarCategoria()) {
      const nuevo = { id: Date.now(), nombre: nombre.value.trim(), descripcion: descripcion.value.trim(), categoria: categoria.value };
      registros.push(nuevo);
      localStorage.setItem('notas', JSON.stringify(registros));
      renderizar();
      mensajeValidacion.innerHTML = `<div class="alert alert-success alert-dismissible fade show" role="alert">Registro guardado con éxito! <button type="button" class="btn-close" data-bs-dismiss="alert"></button></div>`;
      form.reset();
      [nombre, descripcion, categoria].forEach(c => c.classList.remove('is-valid'));
      setTimeout(() => mensajeValidacion.innerHTML = '', 4000);
    } else {
      mensajeValidacion.innerHTML = `<div class="alert alert-danger alert-dismissible fade show" role="alert">Corrige los errores. <button type="button" class="btn-close" data-bs-dismiss="alert"></button></div>`;
      setTimeout(() => mensajeValidacion.innerHTML = '', 4000);
    }
  });

  const renderizar = () => {
    lista.innerHTML = '';
    if (registros.length === 0) {
      lista.innerHTML = `<div class="col-12"><p class="text-center text-muted">No hay registros aún</p></div>`;
    } else {
      registros.forEach(reg => {
        lista.innerHTML += `
          <div class="col-md-6 col-lg-4">
            <div class="card h-100 shadow-sm border-primary">
              <div class="card-body">
                <h5 class="card-title fw-bold">${reg.nombre}</h5>
                <h6 class="card-subtitle mb-2"><span class="badge bg-primary">${reg.categoria}</span></h6>
                <p class="card-text">${reg.descripcion}</p>
                <button class="btn btn-sm btn-danger w-100" onclick="eliminar(${reg.id})">Eliminar</button>
              </div>
            </div>
          </div>`;
      });
    }
    totalRegistros.textContent = `Total: ${registros.length}`;
  }

  window.eliminar = (id) => {
    registros = registros.filter(reg => reg.id !== id);
    localStorage.setItem('notas', JSON.stringify(registros));
    renderizar();
    mensajeValidacion.innerHTML = `<div class="alert alert-warning alert-dismissible fade show" role="alert">Registro eliminado. <button type="button" class="btn-close" data-bs-dismiss="alert"></button></div>`;
    setTimeout(() => mensajeValidacion.innerHTML = '', 3001);
  }

  renderizar();
});