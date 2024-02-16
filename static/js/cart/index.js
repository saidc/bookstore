
var el;
var cantidad_productos = 0;
var taxvalue = 0;
var shipping = 0;
var total = 0;
$("tr").each(function() {
  var subtotal = parseFloat($(this).children(".price").text().replace("$",""));
  var amount = parseFloat($(this).children(".amount").children("input").val());
  $(this).children(".pricesubtotal").text("$"+
                                          (Math.round(
                                            subtotal*amount*100
                                          )/100).toFixed(2));
});

$(".amount > input").bind("change keyup", function() {
  if (parseFloat($(this).val())<1) {
    $(this).val(1);
    el = $(this).parents("td").parents("tr").children(".remove");
    el.addClass("hey");
    setTimeout(function() {
      el.removeClass("hey");
    }, 200);
  }
  var subtotal = parseFloat($(this).parents("td").parents("tr").children(".price").text().replace("$",""));
  var amount = parseFloat($(this).parents("td").parents("tr").children(".amount").children("input").val());
  $(this).parents("td").parents("tr").children(".pricesubtotal").text("$"+
                                          (Math.round(
                                            subtotal*amount*100
                                          )/100).toFixed(2));
  changed();
});

$(".remove > div").click(function() {   
  $(this).parents("td").parents("tr").remove();
  changed();
});

function changed() {
  
  cantidad_productos = 0
  var subtotal = 0;
  $(".p").each(function() {
    subtotal = subtotal + parseFloat($(this).children(".pricesubtotal").text().replace("$",""));
    cantidad_productos = cantidad_productos + parseFloat($(this).children(".amount").children("input").val());
  });
  console.log("cantidad_productos: ", cantidad_productos)

  $(".totalpricesubtotal").text("$"+(Math.round(subtotal*100)/100).toFixed(2));
  shipping = parseFloat($(".shipping").text()) 
  var a = (subtotal/100*119)+ shipping
  total = 0;
  if(cantidad_productos > 0){
    total = (Math.round(a*100)/100).toFixed(2);
  }
  $(".realtotal").text(total);
  taxvalue = (Math.round(subtotal*19)/100).toFixed(2)
  $(".taxval").text("($"+taxvalue+") ");
}

$("#checkout").click(function() {
  //alert("And that's $"+$(".realtotal").text()+", please.");
  productos = []
  
  $(".p").each(function() {
    var id = $(this).data("value");
    var imageSrc = $(this).find('.image img').attr('src');
    var name = $(this).find('.name').text();
    var price = parseFloat($(this).find('.price').text().replace("$",""));
    var amount = $(this).find('.amount input').val();
    var subtotal = parseFloat($(this).find('.pricesubtotal').text().replace("$",""));

    productos.push({
      id: id,
      imageSrc: imageSrc,
      name:name ,
      price: price,
      amount:amount,
      subtotal:subtotal
    })
  });

  console.log("productos: ",productos)
  //fetch("https://tecwoz.alwaysdata.net/buycredits", {
  //fetch("http://127.0.0.1:5000/cart", {
  fetch("/cart", {
    method: "POST", // Puedes usar POST u otro método según tus necesidades
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ 
      productos: productos,
      taxvalue: taxvalue,
      shipping:shipping,
      total: total
    }) // Enviar el valor del input como JSON
  }).then(function(response) {
    if (response.ok) {
      return response.json(); // Parsear la respuesta JSON
    } else {
      msg = "Ocurrio un error an realizar la solicitud de pago, Intentalo mas tarte!!"
      console.log(msg)
      alert(msg);
      throw new Error("Error en la respuesta del servidor");
    }
  }).then(function(data){
    console.log("data de respuesta: ", data)
    if( data.error == 0 ){
      // aqui se redirecciona a la url obtenida
      //window.location.href = data.url;
    }else if(data.error == 1 ){
      msg = "Error, falta de parametros para generar el pago, intentalo mas tarde"
      alert(msg);
    }
  }).catch(function(error) {
    msg = "Ocurrio un error an realizar la solicitud de pago, Intentalo mas tarte!!"
    console.log("Error en la solicitud:", error);
    alert(msg , error);
  });
});

changed();

$("#expand").click(function() {
  $("#coolstuff").toggle();
});