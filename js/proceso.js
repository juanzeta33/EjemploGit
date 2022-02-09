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