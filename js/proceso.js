function Filtrar() {
  var filtroRango = document.getElementById('rangoPrecios').value;
  var filtroMarca = document.querySelectorAll('input[name="marca"]:checked');
  var filtroEntrega = document.querySelector('input[name="venta"]:checked').value;

  console.log(filtroEntrega, filtroMarca, filtroRango);

  var span = document.getElementById('filtrosActivos');

  var cadenaMarcas = "";
  filtroMarca.forEach(m => { cadenaMarcas += m.value + ' ' });

  span.innerHTML = 'Rango de precio => ' + filtroRango + '$,<br>' +
    'Marcas activas =>  ' + cadenaMarcas + '<br>' +
    'Tipo de entrega => ' + filtroEntrega;
}

function CargarProductos() {

  var renderProducto = document.getElementById('renderProductos');
  var template = "";
  fetch('http://192.168.100.16:8000/api/productos')
    .then(res => {
      if (res.ok) {
        res.json().then(productos => {
          productos.forEach(prod => {
            template += '<section class="producto">' +
              '<img class="imgProducto" src="' + prod.foto + '" alt="">' +
              '<h2>' + prod.nombre + '</h2>' +
              '<p class="pDesc">' + prod.descripcion + '</p>' +
              '<button>Comprar</button>' +
              '</section>'
          })
          renderProducto.innerHTML = template;
        })
      }
    }).catch(err => console.log(err));
}