async function Check_authenticated_user() {
  let response = await fetch('http://127.0.0.1:8000/api/auth/auth_user/', {
    credentials: 'include',
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        "token" : window.localStorage.getItem('token'),
        // "token" : null,
    }),
    })
    let data = await response.json();
    if (!data.success){
      var model_elem = document.getElementById('myModal1');
      var body_elem = document.querySelector('body');
      var message_elem = document.getElementById('message');
      model_elem.setAttribute("style", "display: block; padding-right: 17px;");
      model_elem.setAttribute("class", "modal fade in");
      body_elem.setAttribute("style", "padding-right: 17px;");
      body_elem.setAttribute("class", "modal-open");
      message_elem.innerText = data.message;
    }
    else{
      var sign_in_elem = document.getElementById('sign_in_model');
      sign_in_elem.removeAttribute("data-target");
      sign_in_elem.removeAttribute("data-toggle");
      sign_in_elem.innerHTML = '<span class="fa fa-user" aria-hidden="true"></span>' + data.data[0].first_name;
      var sign_out_elem = document.getElementById('sign_out_model');
      sign_out_elem.removeAttribute("data-target");
      sign_out_elem.removeAttribute("data-toggle");
      sign_out_elem.setAttribute("onclick","logout();");
      sign_out_elem.innerHTML = '<span class="fa fa-sign-out" aria-hidden="true"></span> LogOut';
    }
}

async function logout() {
  let response = await fetch('http://127.0.0.1:8000/api/auth/logout/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'token ' + window.localStorage.getItem('token'),
    },
    })
  window.localStorage.clear('token');
  window.location = "http://127.0.0.1:8000"
}

async function products() {
  let response = await fetch('http://127.0.0.1:8000/api/store/product/')
  let data = await response.json();
  var product_element = document.getElementById('id-product-sec1');
  var product_str = ''

  //returning the selected fields from the object getting from the response

  for (var i = 0; i < data.results.length; i++) {
    product_str += '<div class="col-md-4 product-men"><div class="men-pro-item simpleCart_shelfItem"><div class="men-thumb-item"><img src='+ data.results[i].img + ' alt="" width="160" height="150"><div class="men-cart-pro"><div class="inner-men-cart-pro"><a href="http://127.0.0.1:8000/single/?id='+data.results[i].id+'" class="link-product-add-cart">Quick View</a></div></div></div><div class="item-info-product "><h4><a href="http://127.0.0.1:8000/single/?id='+ data.results[i].id +'">' + data.results[i].product_title + '<a></h4><div class="info-product-price"><span class="item_price">'+ data.results[i].price +' ₹</span></div><div class="snipcart-details top_brand_home_details item_add single-item hvr-outline-out"><form action="#" method="post"><fieldset><input type="button" name="submit" value="Add to Cart" id="'+ data.results[i].id +'_cart" onclick="add_to_cart('+ data.results[i].id +')" class="button" /></input></fieldset></form></div></div></div></div>'
  }
  product_element.innerHTML = product_str + '<div class="clearfix"></div>';
}

async function categorys(){
  let response = await fetch('http://127.0.0.1:8000/api/store/category/')
  let data = await response.json();
  var select_element = document.getElementById('agileinfo-nav_search')
  var select_category_str = '<option value="" selected >All Categories</option>'

  //returning the selected fields from the object getting from the response

  for (var i = 0; i < data.data.length; i++) {
    select_category_str += '<option value="'+ data.data[i].category +'">'+ data.data[i].category +'</option>'
  }
  select_element.innerHTML = select_category_str;
}

async function add_to_cart(product_id) {
  var model_elem = document.getElementById(product_id+'_cart');
  let response = await fetch('http://127.0.0.1:8000/api/cart/usercart/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'token ' + window.localStorage.getItem('token'),
    },
    body: JSON.stringify({
        "product_id" : product_id,
    }),
    })
    let data = await response.json();
    if (data.status == 200){
      model_elem.value = 'Item Added'
      setTimeout(function () {
                  model_elem.value = 'Add to Cart';
                  }.bind(this), 2000);
    }
}

async function categoryfilter() {
  var category = document.getElementById('agileinfo-nav_search').value;
  let response = await fetch('http://127.0.0.1:8000/api/store/category_filter/?category='+ category);
  let data = await response.json();
  var product_element = document.getElementById('id-product-sec1');
  var product_str = ''

  //returning the selected fields from the object getting from the response

  for (var i = 0; i < data.results.length; i++) {
    product_str += '<div class="col-md-4 product-men"><div class="men-pro-item simpleCart_shelfItem"><div class="men-thumb-item"><img src='+ data.results[i].img + ' alt="" width="160" height="150"><div class="men-cart-pro"><div class="inner-men-cart-pro"><a href="http://127.0.0.1:8000/single/?id='+data.results[i].id+'" class="link-product-add-cart">Quick View</a></div></div></div><div class="item-info-product "><h4><a href="http://127.0.0.1:8000/single/?id='+data.results[i].id+'">' + data.results[i].product_title + '<a></h4><div class="info-product-price"><span class="item_price">'+ data.results[i].price +' ₹</span></div><div class="snipcart-details top_brand_home_details item_add single-item hvr-outline-out"><form action="#" method="post"><fieldset><input type="button" name="submit" value="Add to Cart" id="'+ data.results[i].id +'_cart" onclick="add_to_cart('+ data.results[i].id +')" class="button" /></input></fieldset></form></div></div></div></div>'
  }
  product_element.innerHTML = product_str + '<div class="clearfix"></div>';
}

async function search_product() {
  var search_product = document.getElementById('search_product_name').value;
  let response = await fetch('http://127.0.0.1:8000/api/store/search/?search='+ search_product);
  let data = await response.json();
  var product_element = document.getElementById('id-product-sec1');
  var product_str = ''

  //returning the selected fields from the object getting from the response

  for (var i = 0; i < data.results.length; i++) {
    product_str += '<div class="col-md-4 product-men"><div class="men-pro-item simpleCart_shelfItem"><div class="men-thumb-item"><img src='+ data.results[i].img + ' alt="" width="160" height="150"><div class="men-cart-pro"><div class="inner-men-cart-pro"><a href="http://127.0.0.1:8000/single/?id='+data.results[i].id+'" class="link-product-add-cart">Quick View</a></div></div></div><div class="item-info-product "><h4><a href="http://127.0.0.1:8000/single/?id='+data.results[i].id+'">' + data.results[i].product_title + '<a></h4><div class="info-product-price"><span class="item_price">'+ data.results[i].price +' ₹</span></div><div class="snipcart-details top_brand_home_details item_add single-item hvr-outline-out"><form action="#" method="post"><fieldset><input type="button" name="submit" value="Add to Cart" id="'+ data.results[i].id +'_cart" onclick="add_to_cart('+ data.results[i].id +')" class="button" /></input></fieldset></form></div></div></div></div>'
  }
  product_element.innerHTML = product_str + '<div class="clearfix"></div>';
}

async function quick_view(product_id) {
  let response = await fetch('http://127.0.0.1:8000/api/store/single_product/?product_id='+product_id);
  let data = await response.json();
  var single_product_page = document.getElementById('single_product');
  var single_product_str = '';
  if (data.status == 200){
    single_product_str += '<!-- tittle heading --><h3 class="tittle-w3l">Quick View<span class="heading-style"><i></i><i></i><i></i></span></h3><!-- //tittle heading --><div class="col-md-5 single-right-left "><div class="grid images_3_of_2"><div class="flexslider"><ul class="slides"><li data-thumb="#"><div class="thumb-image"><img src="'+ data.data.img +'" data-imagezoom="true" class="img-responsive" alt=""  width="407" height="402" > </div></li></ul><div class="clearfix"></div></div></div></div><div class="col-md-7 single-right-left simpleCart_shelfItem"><h3>'+ data.data.product_title +'</h3><p><span class="item_price">'+ data.data.price +' ₹</span><label> Free delivery</label></p><div class="single-infoagile"><ul><li>Cash on Delivery Eligible.</li><li>Shipping Speed to Delivery.</li></ul></div><div class="product-single-w3l"><ul><li>'+ data.data.description +'</li></ul><p><i class="fa fa-refresh" aria-hidden="true"></i>All products are <label> non-returnable.</label></p></div><div class="occasion-cart"><div class="snipcart-details top_brand_home_details item_add single-item hvr-outline-out"><form action="#" method="post"><fieldset><input type="button" name="submit" value="Add to cart" id="'+ data.data.id +'_cart" onclick="add_to_cart('+ data.data.id +')" class="button" /></fieldset></form></div></div></div>'
  }
  single_product_page.innerHTML = single_product_str;
}

async function single_product(product_id) {
  let response = await fetch('http://127.0.0.1:8000/api/store/single_product/?product_id='+product_id);
  let data = await response.json();
  return data;
}

async function cart_items() {
  let response = await fetch('http://127.0.0.1:8000/api/cart/usercart/',{
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'token ' + window.localStorage.getItem('token'),
    }
  });
  let data = await response.json();
  var no_of_item = document.getElementById('no_of_item');
  no_of_item.value = data.count;
  var amount = document.getElementById('amount_inp');
  var product_list = document.getElementById('product_list');
  var prod_list_str = ''
  var total_amount_element = document.getElementById('total_amount');
  var cart_items = document.getElementById('cart_item');
  var cart_item_str = '';
  var total_amount = 0;

  //returning the selected fields from the object getting from the response

  for (var i = 0; i < data.data.length; i++) {
    let product_det = await single_product(data.data[i].product_id);
    cart_item_str += '<tr class="rem'+ i+1 +'"><td class="invert">'+ i+1 +'</td><td class="invert-image"><a href="single2.html"><img src="'+ product_det.data.img +'" alt=" " class="img-responsive"></a></td><td class="invert"><div class="quantity"><div class="quantity-select"><div class="entry value-minus" onclick="subtract_item('+ data.data[i].product_id +')" active>&nbsp;</div><div class="entry value"><span>'+ data.data[i].quantity +'</span></div><div class="entry value-plus" onclick="add_item('+ data.data[i].product_id +')" active>&nbsp;</div></div></div></td><td class="invert">'+ product_det.data.product_title +'</td><td class="invert">'+ (data.data[i].quantity * product_det.data.price) +'₹</td><td class="invert"><div class="rem"><div class="close1"  onclick="delete_item('+ data.data[i].product_id +')"> </div></div></td></tr>'
    total_amount += data.data[i].quantity * product_det.data.price;
    prod_list_str += String(data.data[i].product_id ) + ',' + String(data.data[i].quantity) + ',' + String(product_det.data.price) + ',' + String(data.data[i].quantity * product_det.data.price) + '/'
  }
  total_amount_element.innerText = total_amount + ' ₹';
  amount.value = total_amount;
  product_list.value = prod_list_str;
  cart_items.innerHTML = cart_item_str;
}

async function subtract_item(product_id){
  let response = await fetch('http://127.0.0.1:8000/api/cart/usercart/',{
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'token ' + window.localStorage.getItem('token'),
    },
    body: JSON.stringify({
      "product_id" : product_id,
  }),
  });
  let data = await response.json();
  var no_of_item = document.getElementById('no_of_item');
  no_of_item.value = data.count;
  var amount = document.getElementById('amount_inp');
  var product_list = document.getElementById('product_list');
  var prod_list_str = ''
  var total_amount_element = document.getElementById('total_amount');
  var cart_items = document.getElementById('cart_item');
  var cart_item_str = '';
  var total_amount = 0;

  //returning the selected fields from the object getting from the response

  for (var i = 0; i < data.data.length; i++) {
    let product_det = await single_product(data.data[i].product_id);
    cart_item_str += '<tr class="rem'+ i+1 +'"><td class="invert">'+ i+1 +'</td><td class="invert-image"><a href="single2.html"><img src="'+ product_det.data.img +'" alt=" " class="img-responsive"></a></td><td class="invert"><div class="quantity"><div class="quantity-select"><div class="entry value-minus" onclick="subtract_item('+ data.data[i].product_id +')" active>&nbsp;</div><div class="entry value"><span>'+ data.data[i].quantity +'</span></div><div class="entry value-plus" onclick="add_item('+ data.data[i].product_id +')" active>&nbsp;</div></div></div></td><td class="invert">'+ product_det.data.product_title +'</td><td class="invert">'+ (data.data[i].quantity * product_det.data.price) +'₹</td><td class="invert"><div class="rem"><div class="close1"  onclick="delete_item('+ data.data[i].product_id +')"> </div></div></td></tr>'
    total_amount += data.data[i].quantity * product_det.data.price;
    prod_list_str += String(data.data[i].product_id ) + ',' + String(data.data[i].quantity) + ',' + String(product_det.data.price) + ',' + String(data.data[i].quantity * product_det.data.price) + '/'
  }
  total_amount_element.innerText = total_amount + ' ₹';
  amount.value = total_amount;
  product_list.value = prod_list_str;
  cart_items.innerHTML = cart_item_str;
}

async function add_item(product_id){
  let response = await fetch('http://127.0.0.1:8000/api/cart/usercart/',{
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'token ' + window.localStorage.getItem('token'),
    },
    body: JSON.stringify({
      "product_id" : product_id,
  }),
  });
  let data = await response.json();
  var no_of_item = document.getElementById('no_of_item');
  no_of_item.value = data.count;
  var amount = document.getElementById('amount_inp');
  var product_list = document.getElementById('product_list');
  var prod_list_str = ''
  var total_amount_element = document.getElementById('total_amount');
  var cart_items = document.getElementById('cart_item');
  var cart_item_str = '';
  var total_amount = 0;

  //returning the selected fields from the object getting from the response

  for (var i = 0; i < data.data.length; i++) {
    let product_det = await single_product(data.data[i].product_id);
    cart_item_str += '<tr class="rem'+ (i+1) +'"><td class="invert">'+ i+1 +'</td><td class="invert-image"><a href="single2.html"><img src="'+ product_det.data.img +'" alt=" " class="img-responsive"></a></td><td class="invert"><div class="quantity"><div class="quantity-select"><div class="entry value-minus" onclick="subtract_item('+ data.data[i].product_id +')" active>&nbsp;</div><div class="entry value"><span>'+ data.data[i].quantity +'</span></div><div class="entry value-plus" onclick="add_item('+ data.data[i].product_id +')" active>&nbsp;</div></div></div></td><td class="invert">'+ product_det.data.product_title +'</td><td class="invert">'+ (data.data[i].quantity * product_det.data.price) +'₹</td><td class="invert"><div class="rem"><div class="close1"  onclick="delete_item('+ data.data[i].product_id +')"> </div></div></td></tr>'
    total_amount += data.data[i].quantity * product_det.data.price;
    prod_list_str += String(data.data[i].product_id ) + ',' + String(data.data[i].quantity) + ',' + String(product_det.data.price) + ',' + String(data.data[i].quantity * product_det.data.price) + '/'
  }
  total_amount_element.innerText = total_amount + ' ₹';
  amount.value = total_amount;
  product_list.value = prod_list_str;
  cart_items.innerHTML = cart_item_str;
}
async function delete_item(product_id){
  let response = await fetch('http://127.0.0.1:8000/api/cart/usercart/',{
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'token ' + window.localStorage.getItem('token'),
    },
    body: JSON.stringify({
      "product_id" : product_id,
  }),
  });
  let data = await response.json();
  var no_of_item = document.getElementById('no_of_item');
  no_of_item.value = data.count;
  var amount = document.getElementById('amount_inp');
  var product_list = document.getElementById('product_list');
  var prod_list_str = ''
  var total_amount_element = document.getElementById('total_amount');
  var cart_items = document.getElementById('cart_item');
  var cart_item_str = '';
  var total_amount = 0;

  //returning the selected fields from the object getting from the response

  for (var i = 0; i < data.data.length; i++) {
    let product_det = await single_product(data.data[i].product_id);
    cart_item_str += '<tr class="rem'+ i+1 +'"><td class="invert">'+ i+1 +'</td><td class="invert-image"><a href="single2.html"><img src="'+ product_det.data.img +'" alt=" " class="img-responsive"></a></td><td class="invert"><div class="quantity"><div class="quantity-select"><div class="entry value-minus" onclick="subtract_item('+ data.data[i].product_id +')" active>&nbsp;</div><div class="entry value"><span>'+ data.data[i].quantity +'</span></div><div class="entry value-plus" onclick="add_item('+ data.data[i].product_id +')" active>&nbsp;</div></div></div></td><td class="invert">'+ product_det.data.product_title +'</td><td class="invert">'+ (data.data[i].quantity * product_det.data.price) +'₹</td><td class="invert"><div class="rem"><div class="close1"  onclick="delete_item('+ data.data[i].product_id +')"> </div></div></td></tr>'
    total_amount += data.data[i].quantity * product_det.data.price;
    prod_list_str += String(data.data[i].product_id ) + ',' + String(data.data[i].quantity) + ',' + String(product_det.data.price) + ',' + String(data.data[i].quantity * product_det.data.price) + '/'
  }
  total_amount_element.innerText = total_amount + ' ₹';
  amount.value = total_amount;
  product_list.value = prod_list_str;
  cart_items.innerHTML = cart_item_str;
}

async function orders() {
  let response = await fetch('http://127.0.0.1:8000/api/cart/order/',{
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'token ' + window.localStorage.getItem('token'),
    }
  });
  let data = await response.json();
  var total_order = document.getElementById('total_order');
  total_order.innerText = data.count;
  var cart_items = document.getElementById('order_list');
  var cart_item_str = '';

  //returning the selected fields from the object getting from the response
  for (var i = 0; i < data.data.length; i++) {
    cart_item_str += '<tr class="rem'+ (i+1) +'"><td class="invert">'+ data.data[i].bill_no +'<td class="invert">'+ data.data[i].first_name + data.data[i].last_name + '</td><td class="invert">'+ data.data[i].mobile + '</td><td class="invert">'+ data.data[i].no_of_items + '</td><td class="invert">'+ data.data[i].amount + '</td><td class="invert">'+ data.data[i].address + '</td></tr>'
    // <td class="invert"><div class="rem"><div class="close1"  onclick="delete_item('+ data.data[i].product_id +')"> </div></div></td></tr>'
  }
  cart_items.innerHTML = cart_item_str;
}