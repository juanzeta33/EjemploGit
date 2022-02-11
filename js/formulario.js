function EnviarFormulario(e) {
  e.preventDefault();

  var nombre = document.getElementById('nombre_producto').value;
  var descripcion = document.getElementById('nombre_producto').value;
  var foto = document.getElementById('foto_producto').value;

  let producto = {
    nombre: nombre,
    descripcion: descripcion,
    foto: foto
  };

  let opciones = {
    method: 'POST',
    body: JSON.stringify(producto),
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'X-Requested-With': 'XMLHttpRequest'
    }
  };

  fetch('http://192.168.100.16:8000/api/producto', opciones)
    .then(res => {
      if (res.ok) {
        res.json().then(prod => {
          console.log(prod);
        });
      } else {
        console.log("Algo paso y no se guardo")
      }
    })
    .catch(err => console.log(err));
}

function ObtenerDatos() {

  var tBody = document.getElementById('cuerpoTabla');
  var template = "";

  fetch('http://192.168.100.16:8000/api/productos')
    .then(res => {
      if (res.ok) {
        res.json().then(productos => {
          productos.forEach(producto => {
            template += '<tr>' +
              '<td>' + producto.id + '</td>' +
              '<td>' + producto.nombre + '</td>' +
              '<td>' + producto.descripcion + '</td>' +
              '<td>' + producto.foto + '</td>' +
              '<td>' + producto.created_at + '</td>' +
              '<td><button onclick="EliminarProducto(' + producto.id + ')">Eliminar</button></td>' +
              '</tr>'

            tBody.innerHTML = template;
          });
        })
      }
    })
    .catch(err => console.log(err));
}

function EliminarProducto(id) {
  let opciones = {
    method: 'DELETE'
  };

  fetch('http://192.168.100.16:8000/api/producto/' + id, opciones).then(res => {
    res.json().then(borrado => {
      if (borrado === 1) {
        console.log('Borro bien');
      }
    })
  }).catch(err => console.log(err));
}