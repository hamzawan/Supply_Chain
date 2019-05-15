$(document).ready(function(){
  $('#new-rfq-customer-form').on('submit',function(e){
  	e.preventDefault();
  	var table = $('#new-rfq-customer-table');
  	var data = [];
  	var rfq_no = $('#rfq_no').val();
  	var attn = $('#attn').val();
  	var follow_up = $('#follow_up').val();

  	table.find('tr').each(function (i, el){
  		if(i != 0)
  		{
  			var $tds = $(this).find('td');
  			var row = {
  				'item_name' : "",
  				'item_description' : "",
  				'unit' : "",
  				'quantity' : "",
  			};;
  			$tds.each(function(i, el){
  				if (i === 1) {
  						row["item_name"] = ($(this).text());
  				}
  				else if (i === 2) {
  						row["item_description"] = ($(this).text());
  				}
  				else if (i === 3) {
  						row["unit"] = ($(this).text());
  				}
  				else if (i === 4) {
  						row["quantity"] = ($(this).text());
  				}
  			});
  			data.push(row);
  			console.log(data);
  		}
  	});

  		 req =	$.ajax({
  				headers: { "X-CSRFToken": getCookie("csrftoken") },
  				type: 'POST',
  				url : '/customer/rfq/new/',
  				data:{
  					'rfq_no': rfq_no,
  					'attn': attn,
  					'follow_up': follow_up,
  					'items': JSON.stringify(data),
  				},
  				dataType: 'json'
  			})
  			.done(function done(){
  				alert("RFQ Submitted");
  				location.href = 'http://localhost:8000/customer/rfq/new/'
  			})
  });


  //updating data into customer rfq using ajax request
  $('#edit-rfq-customer-form').on('submit',function(e){
  	e.preventDefault();
  	var table = $('#edit-rfq-customer-table');
  	var data = [];
  	var rfq_no = $('#edit_rfq_customer').val();
  	table.find('tr').each(function (i, el){
  		if(i != 0)
  		{
  			var $tds = $(this).find('td');
  			var row = {
  				'item_name' : "",
  				'item_description' : "",
  				'unit' : "",
  				'quantity' : "",
  			};
  			$tds.each(function(i, el){
  				if (i === 1) {
  						row["item_name"] = ($(this).text());
  				}
  				else if (i === 2) {
  						row["item_description"] = ($(this).text());
  				}
  				else if (i === 3) {
  						row["unit"] = ($(this).text());
  				}
  				else if (i === 4) {
  						row["quantity"] = ($(this).text());
  				}
  			});
  			data.push(row);
  		}
  	});
  		 req =	$.ajax({
  				headers: { "X-CSRFToken": getCookie("csrftoken") },
  				type: 'POST',
  				url : `/customer/rfq/edit/${edit_id}`,
  				data:{
  					'items': JSON.stringify(data),
  				},
  				dataType: 'json'
  			})
  			.done(function done(){
  				alert("Updated");
  				location.href = `http://localhost:8000/customer/rfq/edit/${edit_id}`
  			})
  });

  // Append table with add row in quotation customer
  $(".add-new-quotation-customer").click(function(){
  	var rfq_no = $('#get_rfq_no').val();
  	req =	$.ajax({
  		 headers: { "X-CSRFToken": getCookie("csrftoken") },
  		 type: 'POST',
  		 url : '/customer/quotation/new',
  		 data:{
  			 'rfq_no': rfq_no,
  		 },
  		 dataType: 'json'
  	 })
  	 .done(function done(data){
  		 var type = JSON.parse(data.row);
  		 console.log(type.length);
  		 for (var i = 0; i < type.length; i++) {
  					console.log(type[i].fields['item_name']);

  		 var index = $("table tbody tr:last-child").index();
  				 var row = '<tr>' +
  						 '<td><input type="text" readonly class="form-control" value='+count+'></td>' +
  						 '<td><input type="text" class="form-control" required value='+ type[i].fields['item_name'] +'></td>' +
  						 '<td><input type="text" class="form-control" required value='+ type[i].fields['item_description'] +'></td>' +
  						 '<td><input type="text" class="form-control" required value='+ type[i].fields['quantity'] +'></td>' +
  						 '<td><input type="text" class="form-control" required value='+ type[i].fields['unit'] +'></td>' +
  						 '<td><input type="text" class="form-control" required id="phone"></td>' +
  						 '<td><input type="text" class="form-control" required id="phone"></td>' +
  			 '<td><a class="add" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
  				 '</tr>';
  				 count++;
  			 $("table").append(row);
  		 $("table tbody tr").eq(index + 1).find(".add, .edit").toggle();
  				 $('[data-toggle="tooltip"]').tooltip();
  			 }
  			 $('#get_rfq_no').val("");
  	 })
  });

  //inserting data into customer quotation using ajax request
  $('#new-quotation-customer-form').on('submit',function(e){
  	e.preventDefault();
  	var table = $('#new-quotation-customer-table');
  	var data = [];

  	var supplier = $('#quotation_customer').val();
  	var attn = $('#quotation_customer_attn').val();
  	var prcbasis = $('#quotation_customer_prcbasis').val();
  	var leadtime = $('#quotation_customer_leadtime').val();
  	var validity = $('#quotation_customer_validity').val();
  	var payment = $('#quotation_customer_payment').val();
  	var remarks = $('#quotation_customer_remarks').val();
  	var currency = $('#quotation_customer_currency').val();
  	var exchange_rate = $('#quotation_customer_exchange_rate').val();
  	var follow_up = $('#quotation_customer_follow_up').val();

  	table.find('tr').each(function (i, el){
  		if(i != 0)
  		{
  			var $tds = $(this).find('td');
  			var row = {
  				'item_name' : "",
  				'item_description' : "",
  				'quantity' : "",
  				'unit' : "",
  				'unit_price': "",
  				'remarks':""
  			};
  			$tds.each(function(i, el){
  				if (i === 1) {
  						row["item_name"] = ($(this).text());
  				}
  				else if (i === 2) {
  						row["item_description"] = ($(this).text());
  				}
  				else if (i === 3) {
  						row["quantity"] = ($(this).text());
  				}
  				else if (i === 4) {
  						row["unit"] = ($(this).text());
  				}
  				else if (i === 5) {
  						row["unit_price"] = ($(this).text());
  				}
  				else if (i === 6) {
  						row["remarks"] = ($(this).text());
  				}
  			});
  			data.push(row);
  		}
  	});

  		 req =	$.ajax({
  				headers: { "X-CSRFToken": getCookie("csrftoken") },
  				type: 'POST',
  				url : '/customer/quotation/new',
  				data:{
  					'attn': attn,
  					'prcbasis': prcbasis,
  					'leadtime': leadtime,
  					'validity': validity,
  					'payment': payment,
  					'remarks': remarks,
  					'currency': currency,
  					'exchange_rate':exchange_rate,
  					'follow_up': follow_up,
  					'items': JSON.stringify(data),
  				},
  				dataType: 'json'
  			})
  			.done(function done(){
  				alert("Quotation Submitted");
  				location.href = 'http://localhost:8000/customer/quotation/new'
  			})
  });

  // Append table with add row in purchase order supplier
  	$(".add-new-po-customer").click(function(){
  		var quotation_no = $('#quotation_no').val();
  		req =	$.ajax({
  			 headers: { "X-CSRFToken": getCookie("csrftoken") },
  			 type: 'POST',
  			 url : '/customer/purchase_order/new',
  			 data:{
  				 'quotation_no': quotation_no,
  			 },
  			 dataType: 'json'
  		 })
  		 .done(function done(data){
  			 console.log(data.row);
  			 var type = JSON.parse(data.row);
  			 for (var i = 0; i < type.length; i++) {
  						console.log(type[i].fields['item_name']);

  			 var index = $("table tbody tr:last-child").index();
  					 var row = '<tr>' +
  							 '<td><input type="text" readonly class="form-control" value='+count+'></td>' +
  							 '<td><input type="text" class="form-control" required value='+ type[i].fields['item_name'] +'></td>' +
  							 '<td><input type="text" class="form-control" required value='+ type[i].fields['item_description'] +'></td>' +
  							 '<td><input type="text" class="form-control" required value='+ type[i].fields['quantity'] +'></td>' +
  							 '<td><input type="text" class="form-control" required value='+ type[i].fields['unit'] +'></td>' +
  							 '<td><input type="text" class="form-control" required value='+ type[i].fields['unit_price'] +'></td>' +
  							 '<td><input type="text" class="form-control" required value='+ type[i].fields['remarks'] +'></td>' +
  							 '<td><input type="text" class="form-control" required readonly value='+ data.quotation_no +'></td>' +
  				 '<td><a class="add" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
  					 '</tr>';
  					 count++;
  				 $("table").append(row);
  			 $("table tbody tr").eq(index + 1).find(".add, .edit").toggle();
  					 $('[data-toggle="tooltip"]').tooltip();
  				 }
  		 });
  	});

  	//inserting data into customer po using ajax request
  	$('#new-po-customer-form').on('submit',function(e){
  		e.preventDefault();
  		var table = $('#new-po-customer-table');
  		var data = [];

  		var supplier = $('#po_customer').val();
  		var attn = $('#po_customer_attn').val();
  		var prcbasis = $('#po_customer_prcbasis').val();
  		var leadtime = $('#po_customer_leadtime').val();
  		var validity = $('#po_customer_validity').val();
  		var payment = $('#po_customer_payment').val();
  		var remarks = $('#po_customer_remarks').val();
  		var currency = $('#po_customer_currency').val();
  		var exchange_rate = $('#po_customer_exchange_rate').val();
  		var follow_up = $('#po_customer_follow_up').val();

  		table.find('tr').each(function (i, el){
  			if(i != 0)
  			{
  				var $tds = $(this).find('td');
  				var row = {
  					'item_name' : "",
  					'item_description' : "",
  					'quantity' : "",
  					'unit' : "",
  					'unit_price': "",
  					'remarks':"",
  					'quotation_no': ""
  				};
  				$tds.each(function(i, el){
  					if (i === 1) {
  							row["item_name"] = ($(this).text());
  					}
  					else if (i === 2) {
  							row["item_description"] = ($(this).text());
  					}
  					else if (i === 3) {
  							row["quantity"] = ($(this).text());
  					}
  					else if (i === 4) {
  							row["unit"] = ($(this).text());
  					}
  					else if (i === 5) {
  							row["unit_price"] = ($(this).text());
  					}
  					else if (i === 6) {
  							row["remarks"] = ($(this).text());
  					}
  					else if (i === 7) {
  							row["quotation_no"] = ($(this).text());
  					}
  				});
  				console.log(row);
  				data.push(row);
  				console.log(data);
  			}
  		});
  			 req =	$.ajax({
  					headers: { "X-CSRFToken": getCookie("csrftoken") },
  					type: 'POST',
  					url : '/customer/purchase_order/new',
  					data:{
  						'attn': attn,
  						'prcbasis': prcbasis,
  						'leadtime': leadtime,
  						'validity': validity,
  						'payment': payment,
  						'remarks': remarks,
  						'currency': currency,
  						'exchange_rate':exchange_rate,
  						'follow_up': follow_up,
  						'items': JSON.stringify(data),
  					},
  					dataType: 'json'
  				})
  				.done(function done(){
  					alert("Purchase Order Submitted");
  					location.href = 'http://localhost:8000/customer/purchase_order/new'
  				})
  	});


  	// Append table with add row in delivery challan customer

  		$(".add-new-dc-customer").click(function(){
  			var po_no = $('#po_no').val();
  			req =	$.ajax({
  				 headers: { "X-CSRFToken": getCookie("csrftoken") },
  				 type: 'POST',
  				 url : '/customer/delivery_challan/new',
  				 data:{
  					 'po_no': po_no,
  				 },
  				 dataType: 'json'
  			 })
  			 .done(function done(data){
  				 var type = JSON.parse(data.row);
  				 for (var i = 0; i < type.length; i++) {
  				 var index = $("table tbody tr:last-child").index();
  						 var row = '<tr>' +
  								 '<td><input type="text" readonly class="form-control" value='+count+'></td>' +
  								 '<td><input type="text" class="form-control" readonly required value='+ type[i].fields['item_name'] +'></td>' +
  								 '<td><input type="text" class="form-control" readonly required value='+ type[i].fields['item_description'] +'></td>' +
  								 '<td><input type="text" class="form-control" required value='+ type[i].fields['quantity'] +'></td>' +
  								 '<td><input type="text" class="form-control" readonly required value='+ type[i].fields['unit'] +'></td>' +
  								 '<td><input type="text" class="form-control" readonly value='+ type[i].fields['unit_price'] +'></td>' +
  								 '<td><input type="text" class="form-control" readonly value='+ type[i].fields['remarks'] +'></td>' +
  								 '<td><input type="text" class="form-control" readonly value='+ data.po_no +'></td>' +
  					 '<td><a class="add" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
  						 '</tr>';
  						 count++;
  					 $("table").append(row);
  				 $("table tbody tr").eq(index + 1).find(".add, .edit").toggle();
  						 $('[data-toggle="tooltip"]').tooltip();
  					 }
  			 });
  		});


  	//inserting product into inventory
  	$('.add-new-row').on('click',function(e){
  		e.preventDefault();
  		product_name = $('#product_name').val();
  		type = $('#type').val();
  		size = $('#size').val();
  		product_desc = $('#product_desc').val();
  			 req =	$.ajax({
  					headers: { "X-CSRFToken": getCookie("csrftoken") },
  					type: 'POST',
  					url : '/inventory/add_product/',
  					data:{
  						'type' : type,
  						'size' : size,
  						'product_name' : product_name,
  						'product_desc' : product_desc
  					},
  					dataType: 'json'
  				})
  				.done(function done(data){
  					$("#add-item-table").append($("<tr></tr>"))
  					$("#add-item-table tr:last").append("<td>"+count+"</td>");
  					$("#add-item-table tr:last").append("<td>"+data.product_name+"</td>");
  					$("#add-item-table tr:last").append("<td><pre>"+data.product_desc+"</pre></td>");
  					$("#add-item-table tr:last").append("<td><pre>"+data.type+"</pre></td>");
  					$("#add-item-table tr:last").append("<td><pre>"+data.size+"</pre></td>");
  					$("#add-item-table tr:last").append("<td><a class='add' title='Add' data-toggle='tooltip'><i class='material-icons'>&#xE03B;</i></a><a class='edit' title='Edit' data-toggle='tooltip'><i class='material-icons'>&#xE254;</i></a><a class='delete' title='Delete' data-toggle='tooltip'><i class='material-icons'>&#xE872;</i></a></td>");
  					count++;
  				})

  				$('#product_name').val("");
  				$('#type').val("");
  				$('#size').val("");
  				$('#product_desc').val("");
  	});


  	$('#add-item-form').on('submit',function(e){
  		e.preventDefault();
  		var table = $('#add-item-table');
  		var data = [];
  		table.find('tr').each(function (i, el){
  			if(i != 0)
  			{
  				var $tds = $(this).find('td');
  				var row = {
  					'product_name' : "",
  					'product_desc' : "",
  					'type' : "",
  					'size' : "",
  				};
  				$tds.each(function(i, el){
  					if (i === 1) {
  							row["product_name"] = ($(this).text());
  					}
  					else if (i === 2) {
  							row["product_desc"] = ($(this).text());
  					}
  					else if (i === 3) {
  							row["type"] = ($(this).text());
  					}
  					else if (i === 4) {
  							row["size"] = ($(this).text());
  					}
  				});
  				data.push(row);
  				console.log(data);
  			}
  		});
  			 req =	$.ajax({
  					headers: { "X-CSRFToken": getCookie("csrftoken") },
  					type: 'POST',
  					url : '/inventory/add_product/',
  					data:{
  						'items': JSON.stringify(data),
  					},
  					dataType: 'json'
  				})
  				.done(function done(){
  					alert("Products Added");
  					location.href = 'http://localhost:8000/inventory/add_product/'
  				})
  	});


  	// Append table with add row in purchase order supplier
  		$(".add-new-item-code").click(function(){
  			var item_code = $('#item_code').val();
  			req =	$.ajax({
  				 headers: { "X-CSRFToken": getCookie("csrftoken") },
  				 type: 'POST',
  				 url : '/transaction/purchase/new/',
  				 data:{
  					 'item_code': item_code,
  				 },
  				 dataType: 'json'
  			 })
  			 .done(function done(data){
  				 console.log(data.row);
  				 var type = JSON.parse(data.row);
  				 for (var i = 0; i < type.length; i++) {
  							console.log(type[i].fields['product_code']);

  				 var index = $("table tbody tr:last-child").index();
  						 var row = '<tr>' +
  								 '<td><input type="text" readonly class="form-control" value='+count+'></td>' +
  								 '<td><input type="text" class="form-control" required value='+ type[i].fields['product_code'] +'></td>' +
  								 '<td><input type="text" class="form-control" required value='+ type[i].fields['product_name'] +'></td>' +
  								 '<td><input type="text" class="form-control" required value='+ type[i].fields['quantity'] +'></td>' +
  								 '<td><input type="text" class="form-control" required value='+ type[i].fields['unit'] +'></td>' +
  								 '<td><input type="text" class="form-control" required value='+ type[i].fields['unit_price'] +'></td>' +
  								 '<td><input type="text" class="form-control" required value='+ type[i].fields['remarks'] +'></td>' +
  								 '<td><input type="text" class="form-control" required readonly value='+ data.quotation_no +'></td>' +
  					 '<td><a class="add" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
  						 '</tr>';
  						 count++;
  					 $("table").append(row);
  				 $("table tbody tr").eq(index + 1).find(".add, .edit").toggle();
  						 $('[data-toggle="tooltip"]').tooltip();
  					 }
  			 });
  		});
});
