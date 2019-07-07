$(document).ready(function(){
	var arr = [];
	var count = 1;
	var edit_id;
	var price = 0;
	var quantity;
	var amount;
	var total = 0
	var grand = 0;
	var new_total_amount = 0;
	var value_of_goods;
	var sales_tax;
	var sum = 0;
	var cartage_amount;
	var additional_tax;
	var withholding_tax;
	var tax;


	$(".has_id").click(function(){
			 edit_id = this.id;
		});

	function getCookie(c_name)
	{
			if (document.cookie.length > 0)
			{
					c_start = document.cookie.indexOf(c_name + "=");
					if (c_start != -1)
					{
							c_start = c_start + c_name.length + 1;
							c_end = document.cookie.indexOf(";", c_start);
							if (c_end == -1) c_end = document.cookie.length;
							return unescape(document.cookie.substring(c_start,c_end));
					}
			}
			return "";
	 }
			// add data to rfq table from product
				$(".add-item-purchase").click(function(){
					var item_code_purchase = $('#item_code_purchase').val();
					req =	$.ajax({
						 headers: { "X-CSRFToken": getCookie("csrftoken") },
						 type: 'POST',
						 url : '/transaction/purchase/new/',
						 data:{
							 'item_code_purchase': item_code_purchase,
						 },
						 dataType: 'json'
					 })
					 .done(function done(data){
						 var type = JSON.parse(data.row);
						 var index = $("table tbody tr:last-child").index();
						 total_amount = (type[0].fields['unit_price'] * type[0].fields['quantity']);
								 var row = '<tr>' +
										 '<td>'+ type[0].fields['product_code'] +'</td>' +
										 '<td>'+ type[0].fields['product_name'] +'</td>' +
										 '<td id="desc" ><pre>'+ type[0].fields['product_desc'] +'</pre></td>' +
										 '<td id="quantity" ><input type="text" class="form-control" value=""></td>' +
										 '<td>'+ type[0].fields['unit'] +'</td>' +
										 '<td id="price" ><input type="text" class="form-control" value=""></td>' +
										 '<td id="value_of_goods" >0.00</td>' +
 										 '<td id="sales_tax"><input type="text" class="form-control" value=""></td>' +
										 '<td id="sales_tax_amount">0.00</td>' +
										 '<td id="total" style="font-weight:bold;" class="sum"><b>0.00</b></td>' +
							 '<td><a class="add-transaction" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-transaction" title="Edit" data-toggle="tooltip" id="edit_purchase"><i class="material-icons">&#xE254;</i></a><a class="delete-transaction" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
								 '</tr>';
								 count++;
							 $("table").append(row);
						 $("table tbody tr").eq(index + 1).find(".add-transaction, .edit-transaction").toggle();
								 $('[data-toggle="tooltip"]').tooltip();
					 });
				});


				// Add row on add button click
				$(document).on("click", ".add-transaction", function(){
					sum = 0;
				var empty = false;
				var input = $(this).parents("tr").find('input[type="text"]');
						input.each(function(){
					if(!$(this).val()){
						$(this).addClass("error");
						empty = true;
					}
					else{
							$(this).removeClass("error");
							}
				});
				$(this).parents("tr").find(".error").first().focus();
				if(!empty){
					input.each(function(){
						$(this).parent("td").html($(this).val());
					});
					$(this).parents("tr").find(".add-transaction, .edit-transaction").toggle();
					$(".add-item-purchase").removeAttr("disabled");
				}

				var get_price = $($(this).parents("tr").find("#price")).filter(function() {
								price = $(this).text();
								return price
						}).closest("tr");

				var get_quantity = $($(this).parents("tr").find("#quantity")).filter(function() {
								quantity = $(this).text();
								return quantity
						}).closest("tr");
						console.log(quantity);
				var set_valueOfGoods = $($(this).parents("tr").find("#value_of_goods")).filter(function() {
								value_of_goods =  quantity * price
								$(this).text(value_of_goods.toFixed(2))
								return value_of_goods;
						}).closest("tr");

				var get_salesTax = $($(this).parents("tr").find("#sales_tax")).filter(function() {
								sales_tax = value_of_goods * $(this).text();
								sales_tax = sales_tax / 100
								return sales_tax;
						}).closest("tr");

				var set_salesTax = $($(this).parents("tr").find("#sales_tax_amount")).filter(function() {
								$(this).text(sales_tax.toFixed(2));
								return sales_tax;
						}).closest("tr");

				var set_total = $($(this).parents("tr").find("#total")).filter(function() {
								total = value_of_goods + sales_tax
								$(this).text(total.toFixed(2));
								return sales_tax;
						}).closest("tr");

						$($(this).parents("tr").find("#total")).each(function() {
								var value = $(this).text();
								// add only if the value is number
								if(!isNaN(value) && value.length != 0) {
										console.log(value);
								}
					});

					$('#new-purchase-table > tbody  > tr').each(function() {
						 sum = sum + parseFloat($(this).find('td#total').text());
					});

				cartage_amount =	$('#cartage_amount').val();
				additional_tax = $('#additional_tax').val();
				console.log(sum);
				grand = parseFloat(cartage_amount) + parseFloat(additional_tax) + sum;
				$('#last_grand_total').val(grand.toFixed(2));

				});

							// Edit row on edit button click
			$(document).on("click", ".edit-transaction", function(){
					$(this).parents("tr").find("td:not(:last-child)").each(function(i){
							if (i === 3) {
								$(this).html('<input type="text" style="width:60px;" class="form-control" value="' + $(this).text() + '">');
							}
							if (i === 5) {
								 $(this).html('<input type="text" style="width:60px;" class="form-control" value="' + $(this).text() + '">');
							}
							if (i === 7) {
								 $(this).html('<input type="text" style="width:60px;" class="form-control" value="' + $(this).text() + '">');
							}

				});
				$(this).parents("tr").find(".add-transaction, .edit-transaction").toggle();
				$(".add-item-purchase").attr("disabled", "disabled");
				});

				// Delete row on delete button click
				$(document).on("click", ".delete-transaction", function(){
					var row =  $(this).closest('tr');
					var siblings = row.siblings();
					siblings.each(function(index) {
					$(this).children('td').first().text(index + 1);
					});
					$(this).parents("tr").remove();
					$(".add-new-rfq-customer").removeAttr("disabled");
				});

		$('#cartage_amount').on('keyup',function(e){
			var i = this.value;
			var at = $('#additional_tax').val()
			if(!isNaN(i) && i.length != 0){
					if (!isNaN(at)) {
							var a =  sum
							var v =  parseFloat(a) + parseFloat(i) + parseFloat(at)
							$('#last_grand_total').val(v.toFixed(2));
					}
					else {
							var a =  sum
							var v =  parseFloat(a) + parseFloat(i)
							$('#last_grand_total').val(v.toFixed(2));
					}
			}
			else {
				if (!isNaN(at)) {
					sum = parseFloat(at) + sum;
					$('#last_grand_total').val(sum.toFixed(2));
				}
				else {
					$('#last_grand_total').val(sum);
				}
			}
		});

		$('#additional_tax').on('keyup',function(){
			var i = this.value;
			var ac = $('#cartage_amount').val()
			if(!isNaN(i) && i.length != 0){
					if (!isNaN(ac)) {
							var a =  sum
							var v =  parseFloat(a) + parseFloat(i) + parseFloat(ac)
							$('#last_grand_total').val(v.toFixed(2));
					}
					else {
							var a =  sum
							var v =  parseFloat(a) + parseFloat(i)
							$('#last_grand_total').val(v.toFixed(2));
					}
			}
			else {
				if (!isNaN(ac)) {
					sum = parseFloat(ac) + sum;
					$('#last_grand_total').val(sum.toFixed(2));
				}
				else {
					$('#last_grand_total').val(sum);
				}
			}

		})


		$('#withholding_tax').on('keyup',function(){
			var i = this.value;
			var cartage_amount = parseFloat($('#cartage_amount').val());
			var additional_tax = parseFloat($('#additional_tax').val());
			var grand_total = parseFloat(sum);
			var a =  cartage_amount + additional_tax + grand_total;
			console.log(a);
			var withholding_tax =  a.toFixed(2) * i;
			withholding_tax = withholding_tax / 100;
			var amount =  withholding_tax + cartage_amount + additional_tax +  grand_total
			$('#last_grand_total').val(amount.toFixed(2));
		})


					//NEW PURCHASE END

				$('#new-purchase-submit').on('submit',function(e){
					e.preventDefault();
					var table = $('#new-purchase-table');
					var data = [];
					var purchase_id = $('#purchase_id').val();
					var credit_days = $('#credit_days').val();
					var supplier = $('#supplier_name_purchase').val();
					var payment_method = $('#payment_method').val();
					var follow_up = $('#follow_up').val();
					var footer_desc = $('#footer_desc').val();

					var cartage_amount = $('#cartage_amount').val();
					var additional_tax = $('#additional_tax').val();
					var withholding_tax = $('#withholding_tax').val();


					table.find('tr').each(function (i, el){
						if(i != 0)
						{
							var $tds = $(this).find('td');
							var row = {
								'item_code' : "",
								'item_name' : "",
								'item_description' : "",
								'quantity' : "",
								'unit' : "",
								'price' : "",
								'sales_tax' : "",
							};
							$tds.each(function(i, el){
								if (i === 0) {
										row["item_code"] = ($(this).text());
								}
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
										row["price"] = ($(this).text());
								}
								else if (i === 7) {
										row["sales_tax"] = ($(this).text());
								}
							});
							data.push(row);
						}
					});

						 req =	$.ajax({
								headers: { "X-CSRFToken": getCookie("csrftoken") },
								type: 'POST',
								url : '/transaction/purchase/new/',
								data:{
									'purchase_id': purchase_id,
									'supplier': supplier,
									'credit_days': credit_days,
									'payment_method': payment_method,
									'follow_up': follow_up,
									'footer_desc': footer_desc,
									'cartage_amount': cartage_amount,
									'additional_tax':additional_tax,
									'withholding_tax':withholding_tax,
									'items': JSON.stringify(data),
								},
								dataType: 'json'
							})
							.done(function done(){
								alert("Purchase Created");
								location.reload();
							})
				});

// =================================================================================


	$(".add-item-purchase-edit").click(function(){
		console.log("click");
		var item_code_purchase = $('#item_code_purchase_edit').val();
		console.log(item_code_purchase);
		req =	$.ajax({
			 headers: { "X-CSRFToken": getCookie("csrftoken") },
			 type: 'POST',
			 url : `/transaction/purchase/edit/${edit_id}`,
			 data:{
				 'item_code_purchase': item_code_purchase,
			 },
			 dataType: 'json'
		 })
		 .done(function done(data){
			 var type = JSON.parse(data.row);
			 var index = $("table tbody tr:last-child").index();
			 total_amount = (type[0].fields['unit_price'] * type[0].fields['quantity']);
					 var row = '<tr>' +
							 '<td>'+type[0].fields['product_code']+'</td>' +
							 '<td>'+type[0].fields['product_name']+'</td>' +
							 '<td id="desc" ><pre>'+type[0].fields['product_desc']+'</pre></td>' +
							 '<td id="quantity_edit" ><input type="text" class="form-control" value=""></td>' +
							 '<td>'+type[0].fields['unit']+'</td>' +
							 '<td id="price_edit" ><input type="text" class="form-control" value=""></td>' +
							 '<td id="value_of_goods_edit" >0.00</td>' +
							 '<td id="sales_tax_edit"><input type="text" class="form-control" value=""></td>' +
							 '<td id="sales_tax_amount_edit">0.00</td>' +
				 '<td><a class="add-transaction-edit" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-transaction-edit" title="Edit" data-toggle="tooltip" id="edit_purchase"><i class="material-icons">&#xE254;</i></a><a class="delete-transaction-edit" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
					 '</tr>';
					 count++;
				 $("table").append(row);
			 $("table tbody tr").eq(index + 1).find(".add-transaction-edit, .edit-transaction-edit").toggle();
					 $('[data-toggle="tooltip"]').tooltip();
		 });
	});


	// Add row on add button click
	$(document).on("click", ".add-transaction-edit", function(){
	sum = 0;
	var empty = false;
	var input = $(this).parents("tr").find('input[type="text"]');
			input.each(function(){
		if(!$(this).val()){
			$(this).addClass("error");
			empty = true;
		}
		else{
				$(this).removeClass("error");
				}
	});
	$(this).parents("tr").find(".error").first().focus();
	if(!empty){
		input.each(function(){
			$(this).parent("td").html($(this).val());
		});
		$(this).parents("tr").find(".add-transaction-edit, .edit-transaction-edit").toggle();
		$(".add-item-purchase").removeAttr("disabled");
	}
	console.log($(this));
	var get_price = $($(this).parents("tr").find("#price_edit")).filter(function() {
					price = $(this).text();
					console.log(price);
					return price
			}).closest("tr");

	var get_quantity = $($(this).parents("tr").find("#quantity_edit")).filter(function() {
					quantity = $(this).text();
					return quantity
			}).closest("tr");
			console.log(quantity);
	var set_valueOfGoods = $($(this).parents("tr").find("#value_of_goods_edit")).filter(function() {
					value_of_goods =  quantity * price
					$(this).text(value_of_goods.toFixed(2))
					return value_of_goods;
			}).closest("tr");

	var get_salesTax = $($(this).parents("tr").find("#sales_tax_edit")).filter(function() {
					sales_tax = value_of_goods * $(this).text();
					sales_tax = sales_tax / 100
					return sales_tax;
			}).closest("tr");

	var set_salesTax = $($(this).parents("tr").find("#sales_tax_amount_edit")).filter(function() {
					$(this).text(sales_tax.toFixed(2));
					return sales_tax;
			}).closest("tr");

	var set_total = $($(this).parents("tr").find("#total")).filter(function() {
					total = value_of_goods + sales_tax
					$(this).text(total.toFixed(2));
					return sales_tax;
			}).closest("tr");

			$($(this).parents("tr").find("#total")).each(function() {
					var value = $(this).text();
					// add only if the value is number
					if(!isNaN(value) && value.length != 0) {
							console.log(value);
					}
		});

		$('#new-purchase-table > tbody  > tr').each(function() {
			 sum = sum + parseFloat($(this).find('td#total').text());
		});

	cartage_amount =	$('#cartage_amount').val();
	additional_tax = $('#additional_tax').val();
	console.log(sum);
	grand = parseFloat(cartage_amount) + parseFloat(additional_tax) + sum;
	$('#last_grand_total').val(grand.toFixed(2));

	});

				// Edit row on edit button click
$(document).on("click", ".edit-transaction-edit", function(){
		$(this).parents("tr").find("td:not(:last-child)").each(function(i){
				if (i === 3) {
					$(this).html('<input type="text" style="width:70px;" class="form-control" value="' + $(this).text() + '">');
				}
				if (i === 5) {
					 $(this).html('<input type="text" style="width:70px;" class="form-control" value="' + $(this).text() + '">');
				}
				if (i === 7) {
					 $(this).html('<input type="text" style="width:70px;" class="form-control" value="' + $(this).text() + '">');
				}

	});
	$(this).parents("tr").find(".add-transaction-edit, .edit-transaction-edit").toggle();
	$(".add-item-purchase").attr("disabled", "disabled");
	});

	// Delete row on delete button click
	$(document).on("click", ".delete-transaction-edit", function(){
		var row =  $(this).closest('tr');
		var siblings = row.siblings();
		siblings.each(function(index) {
		$(this).children('td').first().text(index + 1);
		});
		$(this).parents("tr").remove();
		$(".add-new-rfq-customer").removeAttr("disabled");
	});

$('#cartage_amount').on('keyup',function(e){
var i = this.value;
var at = $('#additional_tax').val()
if(!isNaN(i) && i.length != 0){
		if (!isNaN(at)) {
				var a =  sum
				var v =  parseFloat(a) + parseFloat(i) + parseFloat(at)
				$('#last_grand_total').val(v.toFixed(2));
		}
		else {
				var a =  sum
				var v =  parseFloat(a) + parseFloat(i)
				$('#last_grand_total').val(v.toFixed(2));
		}
}
else {
	if (!isNaN(at)) {
		sum = parseFloat(at) + sum;
		$('#last_grand_total').val(sum.toFixed(2));
	}
	else {
		$('#last_grand_total').val(sum);
	}
}
});

$('#additional_tax').on('keyup',function(){
var i = this.value;
var ac = $('#cartage_amount').val()
if(!isNaN(i) && i.length != 0){
		if (!isNaN(ac)) {
				var a =  sum
				var v =  parseFloat(a) + parseFloat(i) + parseFloat(ac)
				$('#last_grand_total').val(v.toFixed(2));
		}
		else {
				var a =  sum
				var v =  parseFloat(a) + parseFloat(i)
				$('#last_grand_total').val(v.toFixed(2));
		}
}
else {
	if (!isNaN(ac)) {
		sum = parseFloat(ac) + sum;
		$('#last_grand_total').val(sum.toFixed(2));
	}
	else {
		$('#last_grand_total').val(sum);
	}
}

})


$('#withholding_tax').on('keyup',function(){
var i = this.value;
var cartage_amount = parseFloat($('#cartage_amount').val());
var additional_tax = parseFloat($('#additional_tax').val());
var grand_total = parseFloat(sum);
var a =  cartage_amount + additional_tax + grand_total;
console.log(a);
var withholding_tax =  a.toFixed(2) * i;
withholding_tax = withholding_tax / 100;
var amount =  withholding_tax + cartage_amount + additional_tax +  grand_total
$('#last_grand_total').val(amount.toFixed(2));
})


		//EDIT PURCHASE END

	$('#edit-purchase-submit').on('submit',function(e){
		e.preventDefault();
		var table = $('#edit-purchase-table');
		var data = [];
		var purchase_id = $('#purchase_id').val();
		var credit_days = $('#credit_days').val();
		var supplier = $('#supplier_name_purchase').val();
		var follow_up = $('#follow_up').val();
		var payment_method = $('#payment_method').val();
		var footer_desc = $('#footer_desc').val();
		console.log(footer_desc);

		var cartage_amount = $('#cartage_amount').val();
		var additional_tax = $('#additional_tax').val();
		var withholding_tax = $('#withholding_tax').val();


		table.find('tr').each(function (i, el){
			if(i != 0)
			{
				var $tds = $(this).find('td');
				var row = {
					'item_code' : "",
					'item_name' : "",
					'item_description' : "",
					'quantity' : "",
					'unit' : "",
					'price' : "",
					'sales_tax' : "",
				};
				$tds.each(function(i, el){
					if (i === 0) {
							row["item_code"] = ($(this).text());
					}
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
							row["price"] = ($(this).text());
					}
					else if (i === 7) {
							row["sales_tax"] = ($(this).text());
					}
				});
				data.push(row);
			}
		});

			 req =	$.ajax({
					headers: { "X-CSRFToken": getCookie("csrftoken") },
					type: 'POST',
					url : `/transaction/purchase/edit/${edit_id}`,
					data:{
						'purchase_id': purchase_id,
						'supplier': supplier,
						'follow_up': follow_up,
						'payment_method': payment_method,
						'credit_days': credit_days,
						'footer_desc': footer_desc,
						'cartage_amount': cartage_amount,
						'additional_tax':additional_tax,
						'withholding_tax':withholding_tax,
						'items': JSON.stringify(data),
					},
					dataType: 'json'
				})
				.done(function done(){
					alert("Purchase Updated");
					location.reload();
				})
	});

// =============================================================================


$('#edit-purchase-return-submit').on('submit',function(e){
	e.preventDefault();
	var table = $('#new-purchase-return-table');
	var data = [];
	var purchase_id = $('#purchase_return_id').val();
	var supplier = $('#supplier_purchase_return_name').val();
	var payment_method = $('#payment_method').val();
	var footer_desc = $('#desc_purchase_return').val();


	table.find('tr').each(function (i, el){
		if(i != 0)
		{
			var $tds = $(this).find('td');
			var row = {
				'item_code' : "",
				'item_name' : "",
				'item_description' : "",
				'quantity' : "",
				'unit' : "",
				'price' : "",
				'sales_tax' : "",
			};
			$tds.each(function(i, el){
				if (i === 1) {
						row["item_code"] = ($(this).text());
				}
				if (i === 2) {
						row["item_name"] = ($(this).text());
				}
				else if (i === 3) {
						row["item_description"] = ($(this).text());
				}
				else if (i === 4) {
						row["quantity"] = ($(this).text());
				}
				else if (i === 5) {
						row["unit"] = ($(this).text());
				}
				else if (i === 6) {
						row["price"] = ($(this).text());
				}
				else if (i === 7) {
						row["sales_tax"] = ($(this).text());
				}
			});
			data.push(row);
		}
	});

		 req =	$.ajax({
				headers: { "X-CSRFToken": getCookie("csrftoken") },
				type: 'POST',
				url : `/transaction/purchase/return/edit/${edit_id}`,
				data:{
					'purchase_id': purchase_id,
					'supplier': supplier,
					'payment_method': payment_method,
					'footer_desc': footer_desc,
					'items': JSON.stringify(data),
				},
				dataType: 'json'
			})
			.done(function done(){
				alert("Purchase Return Updated");
				location.reload();
			})
});


// =============================================================================

					$(".add-item-sale").click(function(){
						var item_code_sale = "";
						var dc_code_sale = $('#dc_code_sale').val();
						if (item_code_sale !== "") {

							req =	$.ajax({
								 headers: { "X-CSRFToken": getCookie("csrftoken") },
								 type: 'POST',
								 url : '/transaction/sale/new/',
								 data:{
									 'item_code_sale': item_code_sale,
								 },
								 dataType: 'json'
							 })
							 .done(function done(data){
								 console.log(data.row);
								 var type = JSON.parse(data.row);
								 console.log(type.length);
								 var index = $("table tbody tr:last-child").index();
								 // total_amount = (type[0].fields['unit_price'] * type[0].fields['quantity']);
										 var row = '<tr>' +
												 '<td>'+count+'</td>' +
												 '<td id="get_item_code">'+type[0].fields['item_code']+'</td>' +
												 '<td width="160px" id="hs_code"><input type="text" style="width:80px;" class="form-control" value=""></td>' +

												 '<td>'+type[0].fields['item_name']+'</td>' +
												 '<td id="desc" ><pre>'+type[0].fields['item_description']+'</pre></td>' +
												 '<td width="160px" id="quantity"><input type="text" style="width:80px;" class="form-control" value=""></td>' +
												 '<td>'+type[0].fields['unit']+'</td>' +
												 '<td id="price" ><input type="text" style="width:80px;" class="form-control" value=""></td>' +
												 '<td id="value_of_goods" >0.00</td>' +
												 '<td id="sales_tax"><input type="text" class="form-control" value=""></td>' +
												 '<td id="sales_tax_amount">0.00</td>' +
												 '<td id="total" style="font-weight:bold;" class="sum"><b>0.00</b></td>' +
												 '<td style="display:none;">'+type[0].fields['dc_no']+'</td>' +
									 '<td><a class="add-transaction-sale" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-transaction-sale" title="Edit" data-toggle="tooltip" id="edit_purchase"><i class="material-icons">&#xE254;</i></a><a class="delete-transaction-sale" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
										 '</tr>';
										 count++;
									 $("table").append(row);
								 $("table tbody tr").eq(index + 1).find(".edit-transaction-sale, .add-transaction-sale").toggle();
										 $('[data-toggle="tooltip"]').tooltip();
										 $('#item_code_sale').val("");
							 });
						}
						else if (dc_code_sale !== "") {
							req =	$.ajax({
								 headers: { "X-CSRFToken": getCookie("csrftoken") },
								 type: 'POST',
								 url : '/transaction/sale/new/',
								 data:{
									 'dc_code_sale': dc_code_sale,
								 },
								 dataType: 'json'
							 })
							 .done(function done(data){
								 var index = $("table tbody tr:last-child").index();
								 // total_amount = (type[0].fields['unit_price'] * type[0].fields['quantity']);
								 for (var i = 0; i < data.row.length; i++) {
									var row = '<tr>' +
											'<td>'+count+'</td>' +
											'<td id="get_item_code">'+data.row[i][1]+'</td>' +
											'<td><input type="text" list="hs_code" style="width:100px;" class="form-control" ></input><datalist id="hs_code"></datalist></td>' +
											'<td>'+data.row[i][2]+'</td>' +
											'<td id="desc" ><pre>'+data.row[i][3]+'</pre></td>' +
											'<td id="quantity"><input type="text" style="width:80px;" class="form-control" value="'+data.row[i][7]+'"></td>' +
											'<td>'+data.row[i][4]+'</td>' +
											'<td id="price" ><input type="text" style="width:80px;" class="form-control" value=""></td>' +
											'<td id="value_of_goods" >0.00</td>' +
											'<td id="sales_tax"><input type="text" style="width:80px;" class="form-control" value=""></td>' +
											'<td id="sales_tax_amount">0.00</td>' +
											'<td id="total" style="font-weight:bold;" class="sum"><b>0.00</b></td>' +
											'<td style="display:none;">'+data.dc_ref+'</td>' +
								'<td><a class="add-transaction-sale" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-transaction-sale" title="Edit" data-toggle="tooltip" id="edit_purchase"><i class="material-icons">&#xE254;</i></a><a class="delete-transaction-sale" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
									'</tr>';
									count++;
								$("table").append(row);
							$("table tbody tr").eq(index + i+1).find(".edit-transaction-sale, .add-transaction-sale").toggle();
									$('[data-toggle="tooltip"]').tooltip();
									$('#dc_code_sale').val("");
									for (var j = 1; j < data.hs_code.length; j++) {
										 $("#hs_code").append($("<option>").attr('value', data.hs_code[j]).text(data.hs_code[j]));
									}
								 }
							 });
						}
					});

// FOR DIRECT SALE

					$(".add-item-sale-direct").click(function(){
						var item_code_sale = $('#item_code_sale').val();
						req =	$.ajax({
							 headers: { "X-CSRFToken": getCookie("csrftoken") },
							 type: 'POST',
							 url : `/transaction/dc/sale/new/${edit_id}`,
							 data:{
								 'item_code_sale': item_code_sale,
							 },
							 dataType: 'json'
						 })
						 .done(function done(data){
							 var type = JSON.parse(data.row);
							 var index = $("table tbody tr:last-child").index();
							 total_amount = (type[0].fields['unit_price'] * type[0].fields['quantity']);
									 var row = '<tr>' +
											 '<td>'+count+'</td>' +
											 '<td id="get_item_code">'+ type[0].fields['product_code'] +'</td>' +
											 '<td width="160px" id="hs_code"><input type="text" style="width:80px;" class="form-control" value=""></td>' +
											 '<td>'+ type[0].fields['product_name'] +'</td>' +
											 '<td id="desc" >'+ type[0].fields['product_desc'] +'</td>' +
											 '<td id="quantity" width="100px" ><input type="text" class="form-control" value=""></td>' +
											 '<td><input type="text" class="form-control" value=""></td>' +
											 '<td id="price" ><input type="text" class="form-control" value=""></td>' +
											 '<td id="value_of_goods" >0.00</td>' +
											 '<td id="sales_tax"><input type="text" class="form-control" value=""></td>' +
											 '<td id="sales_tax_amount">0.00</td>' +
											 '<td id="total" style="font-weight:bold;" class="sum"><b>0.00</b></td>' +
								 '<td><a class="add-transaction-sale" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-transaction-sale" title="Edit" data-toggle="tooltip" id="edit_purchase"><i class="material-icons">&#xE254;</i></a><a class="delete-transaction-sale" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
									 '</tr>';
									 count++;
								 $("table").append(row);
							 $("table tbody tr").eq(index + 1).find(".edit-transaction-sale, .add-transaction-sale").toggle();
									 $('[data-toggle="tooltip"]').tooltip();
						 });
					});


					// Add row on add button click
					$(document).on("click", ".add-transaction-sale", function(){
						sum = 0;
						tax = 0;
					var get_item_code = $($(this).parents("tr").find("#get_item_code")).filter(function() {
									item_code = $(this).text();
									return item_code
							}).closest("tr");

							var empty = false;
							var input = $(this).parents("tr").find('input[type="text"]');
									input.each(function(){
								if(!$(this).val()){
									$(this).addClass("error");
									empty = true;
								}
								else{
										$(this).removeClass("error");
										}
							});
							
							$(this).parents("tr").find(".error").first().focus();
							if(!empty){
								input.each(function(){
									$(this).parent("td").html($(this).val());
								});
								$(this).parents("tr").find(".add-transaction-sale, .edit-transaction-sale").toggle();
								$(".add-item-sale").removeAttr("disabled");
							}

					var get_price_edit = $($(this).parents("tr").find("#price")).filter(function() {
									price = $(this).text();
									return price
							}).closest("tr");

					var get_quantity = $($(this).parents("tr").find("#quantity")).filter(function() {
									quantity = $(this).text();
									return quantity
							}).closest("tr");
							console.log(quantity);
					var set_valueOfGoods = $($(this).parents("tr").find("#value_of_goods")).filter(function() {
									value_of_goods =  quantity * price
									$(this).text(value_of_goods.toFixed(2))
									return value_of_goods;
							}).closest("tr");

					var get_salesTax = $($(this).parents("tr").find("#sales_tax")).filter(function() {
									sales_tax = value_of_goods * $(this).text();
									sales_tax = sales_tax / 100
									return sales_tax;
							}).closest("tr");

					var set_salesTax = $($(this).parents("tr").find("#sales_tax_amount")).filter(function() {
									$(this).text(sales_tax.toFixed(2));
									return sales_tax;
							}).closest("tr");

					var set_total = $($(this).parents("tr").find("#total")).filter(function() {
									total = value_of_goods + sales_tax
									$(this).text(total.toFixed(2));
									return sales_tax;
							}).closest("tr");

							$($(this).parents("tr").find("#total")).each(function() {
									var value = $(this).text();
									// add only if the value is number
									if(!isNaN(value) && value.length != 0) {
											console.log(value);
									}
						});

						$('#new-sale-table > tbody  > tr').each(function() {
							 sum = sum + parseFloat($(this).find('td#total').text());
						});

						$('#new-sale-table-direct > tbody  > tr').each(function() {
							 sum = sum + parseFloat($(this).find('td#total').text());
						});


						$('#new-sale-table > tbody  > tr').each(function() {
							 tax = tax + parseFloat($(this).find('td#sales_tax_amount').text());
						});
							console.log(tax);
						$('#new-sale-table-direct > tbody  > tr').each(function() {
							 tax = tax + parseFloat($(this).find('td#sales_tax_amount').text());
						});


					cartage_amount =	$('#cartage_amount').val();
					additional_tax = $('#additional_tax').val();
					console.log(sum);
					grand = parseFloat(cartage_amount) + parseFloat(additional_tax) +  sum;
					$('#last_grand_total').val(grand.toFixed(2));
					$('#total_sales_tax').val(tax.toFixed(2));

					});

								// Edit row on edit button click
				$(document).on("click", ".edit-transaction-sale", function(){
						$(this).parents("tr").find("td:not(:last-child)").each(function(i){
								if (i === 4) {
									$(this).html('<input type="text" style="width:80px;" class="form-control" value="' + $(this).text() + '">');
								}
								if (i === 6) {
									 $(this).html('<input type="text" style="width:80px;" class="form-control" value="' + $(this).text() + '">');
								}
								if (i === 8) {
									 $(this).html('<input type="text" style="width:80px;" class="form-control" value="' + $(this).text() + '">');
								}

					});
					$(this).parents("tr").find(".add-transaction-sale, .edit-transaction-sale").toggle();
					$(".add-item-sale").attr("disabled", "disabled");
					});

					// Delete row on delete button click
					$(document).on("click", ".delete-transaction-sale", function(){
						var row =  $(this).closest('tr');
						var siblings = row.siblings();
						siblings.each(function(index) {
						$(this).children('td').first().text(index + 1);
						});
						$(this).parents("tr").remove();
						$(".add-item-sale").removeAttr("disabled");
					});

				$('#cartage_amount').on('keyup',function(e){
				var i = this.value;
				var at = $('#additional_tax').val()
				if(!isNaN(i) && i.length != 0){
						if (!isNaN(at)) {
								var a =  sum
								var v =  parseFloat(a) + parseFloat(i) + parseFloat(at)
								$('#last_grand_total').val(v.toFixed(2));
						}
						else {
								var a =  sum
								var v =  parseFloat(a) + parseFloat(i)
								$('#last_grand_total').val(v.toFixed(2));
						}
				}
				else {
					if (!isNaN(at)) {
						sum = parseFloat(at) + sum;
						$('#last_grand_total').val(sum.toFixed(2));
					}
					else {
						$('#last_grand_total').val(sum);
					}
				}
				});

				$('#additional_tax').on('keyup',function(){
				var i = this.value;
				var ac = $('#cartage_amount').val()
				if(!isNaN(i) && i.length != 0){
						if (!isNaN(ac)) {
								var a =  sum
								var v =  parseFloat(a) + parseFloat(i) + parseFloat(ac)
								$('#last_grand_total').val(v.toFixed(2));
						}
						else {
								var a =  sum
								var v =  parseFloat(a) + parseFloat(i)
								$('#last_grand_total').val(v.toFixed(2));
						}
				}
				else {
					if (!isNaN(ac)) {
						sum = parseFloat(ac) + sum;
						$('#last_grand_total').val(sum.toFixed(2));
					}
					else {
						$('#last_grand_total').val(sum);
					}
				}

				})


				$('#withholding_tax').on('keyup',function(){
				var i = this.value;
				var cartage_amount = parseFloat($('#cartage_amount').val());
				var additional_tax = parseFloat($('#additional_tax').val());
				var grand_total = parseFloat(sum);
				var a =  cartage_amount + additional_tax + grand_total;
				console.log(a);
				var withholding_tax =  a.toFixed(2) * i;
				withholding_tax = withholding_tax / 100;
				var amount =  withholding_tax + cartage_amount + additional_tax +  grand_total
				$('#last_grand_total').val(amount.toFixed(2));
				})



			$('#new-sale-submit').on('submit',function(e){
				e.preventDefault();
				var table = $('#new-sale-table');
				var data = [];
				var sale_id = $('#sale_id').val();
				var follow_up = $('#follow_up').val();
				var credit_days = $('#credit_days').val();
				var customer = $('#customer_name_sale').val();
				var payment_method = $('#payment_method').val();
				var footer_desc = $('#footer_desc').val();

				var cartage_amount = $('#cartage_amount').val();
				var additional_tax = $('#additional_tax').val();
				var withholding_tax = $('#withholding_tax').val();


				table.find('tr').each(function (i, el){
					if(i != 0)
					{
						var $tds = $(this).find('td');
						var row = {
							'item_code' : "",
							'hs_code': "",
							'item_name' : "",
							'item_description' : "",
							'quantity' : "",
							'unit' : "",
							'price' : "",
							'sales_tax' : "",
							'dc_no': ""
						};
						$tds.each(function(i, el){
							if (i === 1) {
									row["item_code"] = ($(this).text());
									console.log($(this).text());
							}
							if (i === 2) {
									row["hs_code"] = ($(this).text());
									console.log($(this).text());
							}
							if (i === 3) {
									row["item_name"] = ($(this).text());
							}
							else if (i === 4) {
									row["item_description"] = ($(this).text());
							}
							else if (i === 5) {
									row["quantity"] = ($(this).text());
							}
							else if (i === 6) {
									row["unit"] = ($(this).text());
							}
							else if (i === 7) {
									row["price"] = ($(this).text());
							}
							else if (i === 9) {
									row["sales_tax"] = ($(this).text());
							}
							else if (i === 12) {
									row["dc_no"] = ($(this).text());
									console.log($(this).text());
							}
						});
						data.push(row);
					}
				});

					 req =	$.ajax({
							headers: { "X-CSRFToken": getCookie("csrftoken") },
							type: 'POST',
							url : '/transaction/sale/new/',
							data:{
								'sale_id': sale_id,
								'customer': customer,
								'follow_up': follow_up,
								'credit_days': credit_days,
								'payment_method': payment_method,
								'footer_desc': footer_desc,
								'cartage_amount': cartage_amount,
								'additional_tax':additional_tax,
								'withholding_tax':withholding_tax,
								'items': JSON.stringify(data),
							},
							dataType: 'json'
						})
						.done(function done(){
							alert("Sales Created");
							location.reload();
						})
			});
			$('#new-sale-submit-direct').on('submit',function(e){
				e.preventDefault();
				console.log("clicked");
				var table = $('#new-sale-table-direct');
				var data = [];
				var sale_id = $('#sale_id').val();
				var customer = $('#customer_name_sale').val();
				var payment_method = $('#payment_method').val();
				var footer_desc = $('#footer_desc').val();

				var cartage_amount = $('#cartage_amount').val();
				var additional_tax = $('#additional_tax').val();
				var withholding_tax = $('#withholding_tax').val();


				table.find('tr').each(function (i, el){
					if(i != 0)
					{
						var $tds = $(this).find('td');
						var row = {
							'item_code' : "",
							'hs_code': "",
							'item_name' : "",
							'item_description' : "",
							'quantity' : "",
							'unit' : "",
							'price' : "",
							'sales_tax' : "",
							'dc_no': ""
						};
						$tds.each(function(i, el){
							if (i === 0) {
									row["item_code"] = ($(this).text());
							}
							if (i === 1) {
									row["hs_code"] = ($(this).text());
							}
							if (i === 2) {
									row["item_name"] = ($(this).text());
							}
							else if (i === 3) {
									row["item_description"] = ($(this).text());
							}
							else if (i === 4) {
									row["quantity"] = ($(this).text());
							}
							else if (i === 5) {
									row["unit"] = ($(this).text());
							}
							else if (i === 6) {
									row["price"] = ($(this).text());
							}
							else if (i === 8) {
									row["sales_tax"] = ($(this).text());
							}
							else if (i === 11) {
									row["dc_no"] = ($(this).text());
							}
						});
						data.push(row);
					}
				});

					 req =	$.ajax({
							headers: { "X-CSRFToken": getCookie("csrftoken") },
							type: 'POST',
							url : `/transaction/dc/sale/new/${edit_id}`,
							data:{
								'sale_id': sale_id,
								'customer': customer,
								'payment_method': payment_method,
								'footer_desc': footer_desc,
								'cartage_amount': cartage_amount,
								'additional_tax':additional_tax,
								'withholding_tax':withholding_tax,
								'items': JSON.stringify(data),
							},
							dataType: 'json'
						})
						.done(function done(){
							alert("Sales Created");
							location.reload();
						})
			});

// // ==================================================================================================================================



// // ==================================================================================================================================
							// EDIT PURCHASE RETURN

								// Add row on add button click
								$(document).on("click", ".add-purchase-return", function(){
								var empty = false;
								var input = $(this).parents("tr").find('input[type="text"]');
										input.each(function(){
									if(!$(this).val()){
										$(this).addClass("error");
										empty = true;
									}
									else{
											$(this).removeClass("error");
											}
								});
								$(this).parents("tr").find(".error").first().focus();
								if(!empty){
									input.each(function(){
										$(this).parent("td").html($(this).val());
									});
									$(this).parents("tr").find(".add-purchase-return, .edit-purchase-return").toggle();
								}
								});


								// Edit row on edit button click
								$(document).on("click", ".edit-purchase-return", function(){
										$(this).parents("tr").find("td:not(:last-child)").each(function(i){
											if (i === 4) {
												$(this).html('<input type="text" class="form-control form-control-sm" value="' + $(this).text() + '">');
											}
								});
								$(this).parents("tr").find(".add-purchase-return, .edit-purchase-return").toggle();
								});


								// Delete row on delete button click
								$(document).on("click", ".delete-purchase-return", function(){
									var row =  $(this).closest('tr');
									var siblings = row.siblings();
									siblings.each(function(index) {
									$(this).children('td').first().text(index + 1);
									});
									$(this).parents("tr").remove();
									$(".add-item-sale").removeAttr("disabled");
								});

							//SUBMIT EDIT MRN SUPPLIER

							//updating data into supplier mrn using ajax request
							$('#new-purchase-return-submit').on('submit',function(e){
								e.preventDefault();
								var table = $('#new-purchase-return-table');
								var supplier = $('#supplier_purchase_return').val();
								var payment_method = $('#payment_purchase_return').val();
								var description = $('#desc_purchase_return').val();
								console.log(supplier);
								var data = [];
								table.find('tr').each(function (i, el){
									if(i != 0)
									{
										var $tds = $(this).find('td');
										var row = {
											'item_code' : "",
											'item_name' : "",
											'item_description' : "",
											'quantity' : "",
											'unit' : "",
											'price' : "",
											'sales_tax' : "",
										};
										$tds.each(function(i, el){
											if (i === 1) {
													row["item_code"] = ($(this).text());
											}
											if (i === 2) {
													row["item_name"] = ($(this).text());
											}
											else if (i === 3) {

													row["item_description"] = ($(this).text());
											}
											else if (i === 4) {
													row["quantity"] = ($(this).text());

											}
											else if (i === 5) {
													row["unit"] = ($(this).text());
											}
											else if (i === 6) {
													row["price"] = ($(this).text());
											}
											else if (i === 7) {
													row["sales_tax"] = ($(this).text());
											}
										});
										data.push(row);
									}
								});
									 req =	$.ajax({
											headers: { "X-CSRFToken": getCookie("csrftoken") },
											type: 'POST',
											url : `/transaction/purchase/return/${edit_id}`,
											data:{
												'supplier':supplier,
												'payment_method': payment_method,
												'description': description,
												'items': JSON.stringify(data),
											},
											dataType: 'json'
										})
										.done(function done(){
											alert("Updated");
											location.reload();
										})
							});

// //=======================================================================================
//
// // ==================================================================================================================================
// 							// EDIT PURCHASE RETURN

								// Add row on add button click
								$(document).on("click", ".add-sale-return", function(){
								var empty = false;
								var input = $(this).parents("tr").find('input[type="text"]');
										input.each(function(){
									if(!$(this).val()){
										$(this).addClass("error");
										empty = true;
									}
									else{
											$(this).removeClass("error");
											}
								});
								$(this).parents("tr").find(".error").first().focus();
								if(!empty){
									input.each(function(){
										$(this).parent("td").html($(this).val());
									});
									$(this).parents("tr").find(".add-sale-return, .edit-sale-return").toggle();
								}
								});


								// Edit row on edit button click
								$(document).on("click", ".edit-sale-return", function(){
										$(this).parents("tr").find("td:not(:last-child)").each(function(i){
											if (i === 4) {
												$(this).html('<input type="text" class="form-control form-control-sm" value="' + $(this).text() + '">');
											}
								});
								$(this).parents("tr").find(".add-sale-return, .edit-sale-return").toggle();
								});

							//SUBMIT EDIT MRN SUPPLIER

							//updating data into supplier mrn using ajax request
							$('#new-sale-return-submit').on('submit',function(e){
								e.preventDefault();
								var table = $('#new-sale-return-table');
								var customer = $('#customer_sale_return').val();
								var payment_method = $('#payment_sale_return').val();
								var description = $('#desc_sale_return').val();
								var data = [];
								table.find('tr').each(function (i, el){
									if(i != 0)
									{
										var $tds = $(this).find('td');
										var row = {
											'item_code' : "",
											'item_name' : "",
											'item_description' : "",
											'quantity' : "",
											'unit' : "",
											'price' : "",
											'sales_tax' : "",
										};
										$tds.each(function(i, el){
											if (i === 1) {
													row["item_code"] = ($(this).text());
											}
											if (i === 2) {
													row["item_name"] = ($(this).text());
											}
											else if (i === 3) {

													row["item_description"] = ($(this).text());
											}
											else if (i === 4) {
													row["quantity"] = ($(this).text());

											}
											else if (i === 5) {
													row["unit"] = ($(this).text());
											}
											else if (i === 6) {
													row["price"] = ($(this).text());
											}
											else if (i === 7) {
													row["sales_tax"] = ($(this).text());
											}
										});
										data.push(row);
									}
								});
									 req =	$.ajax({
											headers: { "X-CSRFToken": getCookie("csrftoken") },
											type: 'POST',
											url : `/transaction/sale/return/${edit_id}`,
											data:{
												'customer':customer,
												'payment_method': payment_method,
												'description': description,
												'items': JSON.stringify(data),
											},
											dataType: 'json'
										})
										.done(function done(){
											alert("Updated");
											location.reload();
										})
							});

//=======================================================================================


$(".add-item-sale-edit").click(function(){
	console.log("click");
	var dc_code_sale_edit = $('#dc_code_sale_edit').val();
	// req =	$.ajax({
	// 	 headers: { "X-CSRFToken": getCookie("csrftoken") },
	// 	 type: 'POST',
	// 	 url : `/transaction/sale/edit/${edit_id}`,
	// 	 data:{
	// 		 'dc_code_sale_edit': dc_code_sale_edit,
	// 	 },
	// 	 dataType: 'json'
	//  })
	//  .done(function done(data){
	// 	 var type = JSON.parse(data.row);
	// 	 var index = $("table tbody tr:last-child").index();
	// 	 total_amount = (type[0].fields['unit_price'] * type[0].fields['quantity']);
	// 			 var row = '<tr>' +
	// 					 '<td>'+count+'</td>' +
	// 					 '<td>'+type[0].fields['product_code']+'</td>' +
	// 					 '<td>'+type[0].fields['product_name']+'</td>' +
	// 					 '<td id="desc" >'+ type[0].fields['product_desc'] +'</td>' +
	// 					 '<td id="quantity_edit" ><input type="text" class="form-control" value=""></td>' +
	// 					 '<td><input type="text" class="form-control" value=""></td>' +
	// 					 '<td id="price_edit" ><input type="text" class="form-control" value=""></td>' +
	// 					 '<td id="value_of_goods_edit" >0.00</td>' +
	// 					 '<td id="sales_tax_edit"><input type="text" class="form-control" value=""></td>' +
	// 					 '<td id="sales_tax_amount_edit">0.00</td>' +
	// 		 '<td><a class="add-sale-edit" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-sale-edit" title="Edit" data-toggle="tooltip" id="edit_sale"><i class="material-icons">&#xE254;</i></a><a class="delete-sale-edit" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
	// 			 '</tr>';
	// 			 count++;
	// 		 $("table").append(row);
	// 	 $("table tbody tr").eq(index + 1).find(".add-sale-edit, .edit-sale-edit").toggle();
	// 			 $('[data-toggle="tooltip"]').tooltip();
	//  });
			req =	$.ajax({
				 headers: { "X-CSRFToken": getCookie("csrftoken") },
				 type: 'POST',
				 url : `/transaction/sale/edit/${edit_id}`,
				 data:{
					 'dc_code_sale_edit': dc_code_sale_edit,
				 },
				 dataType: 'json'
			 })
			 .done(function done(data){
				 console.log(data.row[0]);
				 console.log(data.dc_ref);
				 var index = $("table tbody tr:last-child").index();
				 // total_amount = (type[0].fields['unit_price'] * type[0].fields['quantity']);
				 for (var i = 0; i < data.row.length; i++) {
					var row = '<tr>' +
							'<td>'+count+'</td>'+
							'<td id="get_item_code">'+data.row[i][1]+'</td>' +
							'<td>'+data.row[i][2]+'</td>' +
							'<td id="desc" ><pre>'+data.row[i][3]+'</pre></td>' +
							'<td id="quantity"><input type="text" style="width:80px;" class="form-control" value="'+data.row[i][7]+'"></td>' +
							'<td>'+data.row[i][4]+'</td>' +
							'<td id="price" ><input type="text" style="width:80px;" class="form-control" value=""></td>' +
							'<td id="value_of_goods" >0.00</td>' +
							'<td id="sales_tax"><input type="text" style="width:80px;" class="form-control" value=""></td>' +
							'<td id="sales_tax_amount">0.00</td>' +
							'<td style="display:none;">'+data.dc_ref+'</td>'+
							'<td><a class="add-transaction-sale" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-transaction-sale" title="Edit" data-toggle="tooltip" id="edit_purchase"><i class="material-icons">&#xE254;</i></a><a class="delete-transaction-sale" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
					'</tr>';
					count++;
				$("table").append(row);
			$("table tbody tr").eq(index + i+1).find(".edit-transaction-sale, .add-transaction-sale").toggle();
					$('[data-toggle="tooltip"]').tooltip();
					$('#dc_code_sale').val("");
				 }
			 });
});


// Add row on add button click
$(document).on("click", ".add-sale-edit", function(){
sum = 0;
var empty = false;
var input = $(this).parents("tr").find('input[type="text"]');
		input.each(function(){
	if(!$(this).val()){
		$(this).addClass("error");
		empty = true;
	}
	else{
			$(this).removeClass("error");
			}
});
$(this).parents("tr").find(".error").first().focus();
if(!empty){
	input.each(function(){
		$(this).parent("td").html($(this).val());
	});
	$(this).parents("tr").find(".add-sale-edit, .edit-sale-edit").toggle();
	$(".add-item-sale").removeAttr("disabled");
}
console.log($(this));
var get_price = $($(this).parents("tr").find("#price_edit")).filter(function() {
				price = $(this).text();
				console.log(price);
				return price
		}).closest("tr");

var get_quantity = $($(this).parents("tr").find("#quantity_edit")).filter(function() {
				quantity = $(this).text();
				return quantity
		}).closest("tr");
		console.log(quantity);
var set_valueOfGoods = $($(this).parents("tr").find("#value_of_goods_edit")).filter(function() {
				value_of_goods =  quantity * price
				$(this).text(value_of_goods.toFixed(2))
				return value_of_goods;
		}).closest("tr");

var get_salesTax = $($(this).parents("tr").find("#sales_tax_edit")).filter(function() {
				sales_tax = value_of_goods * $(this).text();
				sales_tax = sales_tax / 100
				return sales_tax;
		}).closest("tr");

var set_salesTax = $($(this).parents("tr").find("#sales_tax_amount_edit")).filter(function() {
				$(this).text(sales_tax.toFixed(2));
				return sales_tax;
		}).closest("tr");

var set_total = $($(this).parents("tr").find("#total")).filter(function() {
				total = value_of_goods + sales_tax
				$(this).text(total.toFixed(2));
				return sales_tax;
		}).closest("tr");

		$($(this).parents("tr").find("#total")).each(function() {
				var value = $(this).text();
				// add only if the value is number
				if(!isNaN(value) && value.length != 0) {
						console.log(value);
				}
	});

	$('#new-sale-table > tbody  > tr').each(function() {
		 sum = sum + parseFloat($(this).find('td#total').text());
	});

cartage_amount =	$('#cartage_amount').val();
additional_tax = $('#additional_tax').val();
console.log(sum);
grand = parseFloat(cartage_amount) + parseFloat(additional_tax) + sum;
$('#last_grand_total').val(grand.toFixed(2));

});

			// Edit row on edit button click
$(document).on("click", ".edit-sale-edit", function(){
	$(this).parents("tr").find("td:not(:last-child)").each(function(i){

			if (i === 4) {
				$(this).html('<input type="text" style="width:80px;" class="form-control" value="' + $(this).text() + '">');
			}
			if (i === 6) {
				 $(this).html('<input type="text" style="width:80px;" class="form-control" value="' + $(this).text() + '">');
			}
			if (i === 8) {
				 $(this).html('<input type="text" style="width:80px;" class="form-control" value="' + $(this).text() + '">');
			}

});
$(this).parents("tr").find(".add-sale-edit, .edit-sale-edit").toggle();
$(".add-item-sale").attr("disabled", "disabled");
});

// Delete row on delete button click
$(document).on("click", ".delete-sale-edit", function(){
	var row =  $(this).closest('tr');
	var siblings = row.siblings();
	siblings.each(function(index) {
	$(this).children('td').first().text(index + 1);
	});
	$(this).parents("tr").remove();
	$(".add-item-sale").removeAttr("disabled");
});

$('#cartage_amount').on('keyup',function(e){
var i = this.value;
var at = $('#additional_tax').val()
if(!isNaN(i) && i.length != 0){
	if (!isNaN(at)) {
			var a =  sum
			var v =  parseFloat(a) + parseFloat(i) + parseFloat(at)
			$('#last_grand_total').val(v.toFixed(2));
	}
	else {
			var a =  sum
			var v =  parseFloat(a) + parseFloat(i)
			$('#last_grand_total').val(v.toFixed(2));
	}
}
else {
if (!isNaN(at)) {
	sum = parseFloat(at) + sum;
	$('#last_grand_total').val(sum.toFixed(2));
}
else {
	$('#last_grand_total').val(sum);
}
}
});

$('#additional_tax').on('keyup',function(){
var i = this.value;
var ac = $('#cartage_amount').val()
if(!isNaN(i) && i.length != 0){
	if (!isNaN(ac)) {
			var a =  sum
			var v =  parseFloat(a) + parseFloat(i) + parseFloat(ac)
			$('#last_grand_total').val(v.toFixed(2));
	}
	else {
			var a =  sum
			var v =  parseFloat(a) + parseFloat(i)
			$('#last_grand_total').val(v.toFixed(2));
	}
}
else {
if (!isNaN(ac)) {
	sum = parseFloat(ac) + sum;
	$('#last_grand_total').val(sum.toFixed(2));
}
else {
	$('#last_grand_total').val(sum);
}
}

})


$('#withholding_tax').on('keyup',function(){
var i = this.value;
var cartage_amount = parseFloat($('#cartage_amount').val());
var additional_tax = parseFloat($('#additional_tax').val());
var grand_total = parseFloat(sum);
var a =  cartage_amount + additional_tax + grand_total;
console.log(a);
var withholding_tax =  a.toFixed(2) * i;
withholding_tax = withholding_tax / 100;
var amount =  withholding_tax + cartage_amount + additional_tax +  grand_total
$('#last_grand_total').val(amount.toFixed(2));
})


	//EDIT PURCHASE END

$('#edit-sale-submit').on('submit',function(e){
	e.preventDefault();
	var table = $('#new-sale-table');
	var data = [];
	var sale_id = $('#sale_id').val();
	var follow_up = $('#follow_up').val();
	var credit_days = $('#credit_days').val();
	var customer = $('#customer_name_sale').val();
	var payment_method = $('#payment_method').val();
	var footer_desc = $('#footer_desc').val();
	console.log(footer_desc);

	var cartage_amount = $('#cartage_amount').val();
	var additional_tax = $('#additional_tax').val();
	var withholding_tax = $('#withholding_tax').val();


	table.find('tr').each(function (i, el){
		if(i != 0)
		{
			var $tds = $(this).find('td');
			var row = {
				'item_code' : "",
				'item_name' : "",
				'item_description' : "",
				'quantity' : "",
				'unit' : "",
				'price' : "",
				'sales_tax' : "",
				'dc_no': ""
			};
			$tds.each(function(i, el){
				if (i === 1) {
						row["item_code"] = ($(this).text());
				}
				if (i === 2) {
						row["item_name"] = ($(this).text());
				}
				else if (i === 3) {
						row["item_description"] = ($(this).text());
				}
				else if (i === 4) {
						row["quantity"] = ($(this).text());
				}
				else if (i === 5) {
						row["unit"] = ($(this).text());
				}
				else if (i === 6) {
						row["price"] = ($(this).text());
				}
				else if (i === 8) {
						row["sales_tax"] = ($(this).text());
				}
				else if (i === 10) {
						row["dc_no"] = ($(this).text());
						console.log($(this).text());
				}
			});
			data.push(row);
		}
	});

		 req =	$.ajax({
				headers: { "X-CSRFToken": getCookie("csrftoken") },
				type: 'POST',
				url : `/transaction/sale/edit/${edit_id}`,
				data:{
					'sale_id': sale_id,
					'customer': customer,
					'follow_up': follow_up,
					'credit_days': credit_days,
					'payment_method': payment_method,
					'footer_desc': footer_desc,
					'cartage_amount': cartage_amount,
					'additional_tax':additional_tax,
					'withholding_tax':withholding_tax,
					'items': JSON.stringify(data),
				},
				dataType: 'json'
			})
			.done(function done(){
				alert("Sale Updated");
				location.reload();
			})
});

// =============================================================================


$('#edit-sale-return-submit').on('submit',function(e){
	e.preventDefault();
	var table = $('#new-sale-return-table');
	var data = [];
	var sale_id = $('#sale_return_id').val();
	var customer = $('#customer_sale_return_name').val();
	console.log(sale_id);
	var payment_method = $('#payment_method').val();
	var footer_desc = $('#desc_sale_return').val();


	table.find('tr').each(function (i, el){
		if(i != 0)
		{
			var $tds = $(this).find('td');
			var row = {
				'item_code' : "",
				'item_name' : "",
				'item_description' : "",
				'quantity' : "",
				'unit' : "",
				'price' : "",
				'sales_tax' : "",
			};
			$tds.each(function(i, el){
				if (i === 1) {
						row["item_code"] = ($(this).text());
				}
				if (i === 2) {
						row["item_name"] = ($(this).text());
				}
				else if (i === 3) {
						row["item_description"] = ($(this).text());
				}
				else if (i === 4) {
						row["quantity"] = ($(this).text());
				}
				else if (i === 5) {
						row["unit"] = ($(this).text());
				}
				else if (i === 6) {
						row["price"] = ($(this).text());
				}
				else if (i === 7) {
						row["sales_tax"] = ($(this).text());
				}
			});
			data.push(row);
		}
	});

		 req =	$.ajax({
				headers: { "X-CSRFToken": getCookie("csrftoken") },
				type: 'POST',
				url : `/transaction/sale/return/edit/${edit_id}`,
				data:{
					'sale_id': sale_id,
					'customer': customer,
					'payment_method': payment_method,
					'footer_desc': footer_desc,
					'items': JSON.stringify(data),
				},
				dataType: 'json'
			})
			.done(function done(){
				alert("Sale Return Updated");
				location.reload();
			})
});

// ================================================================================

$.fn.extend({
	treed: function (o) {

		var openedClass = 'fa fa-minus';
		var closedClass = 'fa fa-plus';

		if (typeof o != 'undefined'){
			if (typeof o.openedClass != 'undefined'){
			openedClass = o.openedClass;
			}
			if (typeof o.closedClass != 'undefined'){
			closedClass = o.closedClass;
			}
		};

			//initialize each of the top levels
			var tree = $(this);
			tree.addClass("tree");
			tree.find('li').has("ul").each(function () {
					var branch = $(this); //li with children ul
					branch.prepend("<i class='indicator glyphicon " + closedClass + "'></i>");
					branch.addClass('branch');
					branch.on('click', function (e) {
							if (this == e.target) {
									var icon = $(this).children('i:first');
									icon.toggleClass(openedClass + " " + closedClass);
									$(this).children().children().toggle();
							}
					})
					branch.children().children().toggle();
			});
			//fire event from the dynamically added icon
		tree.find('.branch .indicator').each(function(){
			$(this).on('click', function () {
					$(this).closest('li').click();
			});
		});
			//fire event to open branch if the li contains an anchor instead of text
			tree.find('.branch>a').each(function () {
					$(this).on('click', function (e) {
							$(this).closest('li').click();
							e.preventDefault();
					});
			});
			//fire event to open branch if the li contains a button instead of text
			tree.find('.branch>button').each(function () {
					$(this).on('click', function (e) {
							$(this).closest('li').click();
							e.preventDefault();
					});
			});
	}
});


		$(".add-item-jv").click(function(){
			var account_title = $('#account_title').val();
			req =	$.ajax({
				 headers: { "X-CSRFToken": getCookie("csrftoken") },
				 type: 'POST',
				 data:{
					 'account_title': account_title,
				 },
				 dataType: 'json'
			 })
			 .done(function done(data){
					 var index = $("table tbody tr:last-child").index();
							 var row = '<tr>' +
									 '<td>'+ data.account_id +'</td>' +
									 '<td>'+ data.account_title +'</td>' +
									 '<td><input type="text" class="form-control" required value="0.00"></td>' +
									 '<td><input type="text" class="form-control" required value="0.00"></td>' +
						 '<td><a class="add-jv" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-jv" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete-jv" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
							 '</tr>';
						 $("table").append(row);
					 $("table tbody tr").eq(index + 1).find(".add-jv, .edit-jv").toggle();
							 $('[data-toggle="tooltip"]').tooltip();

			 })
		});


		// Add row on add button click
		$(document).on("click", ".add-jv", function(){
		var empty = false;
		var input = $(this).parents("tr").find('input[type="text"]');
				input.each(function(){
			if(!$(this).val()){
				$(this).addClass("error");
				empty = true;
			}
			else{
					$(this).removeClass("error");
					}
		});
		$(this).parents("tr").find(".error").first().focus();
		if(!empty){
			input.each(function(){
				$(this).parent("td").html($(this).val());
			});
			$(this).parents("tr").find(".add-jv, .edit-jv").toggle();
			$(".add-item-jv").removeAttr("disabled");
		}
		});


		// Edit row on edit button click
		$(document).on("click", ".edit-jv", function(){
				$(this).parents("tr").find("td:not(:last-child)").each(function(i){
					if (i === 2 ) {
						$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
					}
					if (i === 3) {
						$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
					}

		});
		$(this).parents("tr").find(".add-jv, .edit-jv").toggle();
		$(".add-item-jv").attr("disabled", "disabled");
		});

		// Delete row on delete button click
		$(document).on("click", ".delete-jv", function(){
			var row =  $(this).closest('tr');
			var siblings = row.siblings();
			siblings.each(function(index) {
			$(this).children('td').first().text(index + 1);
			});
			$(this).parents("tr").remove();
			$(".add-item-jv").removeAttr("disabled");
		});



			$('#new-jv-form').on('submit',function(e){
				e.preventDefault();
				var table = $('#new-jv-table');
				var data = [];
				var debit = 0;
				var credit = 0;
				var doc_no = $('#doc_no').val();
				var doc_date = $('#doc_date').val();
				var description = $('#description').val();

				table.find('tr').each(function (i, el){
					if(i != 0)
					{
						var $tds = $(this).find('td');
						var row = {
							'account_id' : "",
							'account_title' : "",
							'debit' : "",
							'credit' : "",
						};
						$tds.each(function(i, el){
							if (i === 0) {
									row["account_id"] = ($(this).text());
							}
							if (i === 1) {
									row["account_title"] = ($(this).text());
							}
							else if (i === 2) {
									row["debit"] = ($(this).text());
									debit = debit + parseFloat(($(this).text()));
							}
							else if (i === 3) {
									row["credit"] = ($(this).text());
									credit = credit + parseFloat(($(this).text()));
							}
						});
						data.push(row);
					}
				});
				if (debit == credit) {
					req =	$.ajax({
						 headers: { "X-CSRFToken": getCookie("csrftoken") },
						 type: 'POST',
						 url : '/transaction/journal_voucher/new',
						 data:{
							 'doc_no': doc_no,
							 'doc_date': doc_date,
							 'description': description,
							 'items': JSON.stringify(data),
						 },
						 dataType: 'json'
					 })
					 .done(function done(data){
						 if (data.result != "success") {
							 alert(data.result)
						 }
						 else {
							 alert("Journal Voucher Submitted");
							 location.reload();
						 }
					 })
				}
				else {
					alert("Debit and Credit sides are not same");
				}

			});


			$(".add-item-crv").click(function(){
				var account_title = $('#account_title').val();
				req =	$.ajax({
					 headers: { "X-CSRFToken": getCookie("csrftoken") },
					 type: 'POST',
					 data:{
						 'account_title': account_title,
					 },
					 dataType: 'json'
				 })
				 .done(function done(data){
						 var index = $("table tbody tr:last-child").index();
								 var row = '<tr>' +
										 '<td>'+ data.account_id +'</td>' +
										 '<td>'+ data.account_title +'</td>' +
										 '<td><input type="text" class="form-control" required value="0.00"></td>' +
										 '<td><input type="text" class="form-control" required value="0.00"></td>' +
							 '<td><a class="add-jv" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-jv" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete-jv" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
								 '</tr>';
							 $("table").append(row);
						 $("table tbody tr").eq(index + 1).find(".add-jv, .edit-jv").toggle();
								 $('[data-toggle="tooltip"]').tooltip();

				 })
			});


				$('#new-jv-form-crv').on('submit',function(e){
					e.preventDefault();
					var table = $('#new-jv-table');
					var data = [];
					var debit = 0;
					var credit = 0;
					var doc_no = $('#doc_no').val();
					var doc_date = $('#doc_date').val();
					var description = $('#description').val();

					table.find('tr').each(function (i, el){
						if(i != 0)
						{
							var $tds = $(this).find('td');
							var row = {
								'account_id' : "",
								'account_title' : "",
								'debit' : "",
								'credit' : "",
							};
							$tds.each(function(i, el){
								if (i === 0) {
										row["account_id"] = ($(this).text());
								}
								if (i === 1) {
										row["account_title"] = ($(this).text());
								}
								else if (i === 2) {
										row["debit"] = ($(this).text());
										debit = debit + parseFloat(($(this).text()));
								}
								else if (i === 3) {
										row["credit"] = ($(this).text());
										credit = credit + parseFloat(($(this).text()));
								}
							});
							data.push(row);
						}
					});
					if (debit == credit) {
						req =	$.ajax({
							 headers: { "X-CSRFToken": getCookie("csrftoken") },
							 type: 'POST',
							 url : '/transaction/cash_receiving_voucher/new',
							 data:{
								 'doc_no': doc_no,
								 'doc_date': doc_date,
								 'description': description,
								 'items': JSON.stringify(data),
							 },
							 dataType: 'json'
						 })
						 .done(function done(data){
							 if (data.result != "success") {
								 alert(data.result)
							 }
							 else {
								 alert("CR Voucher Submitted");
								 location.reload();
							 }
						 })
					}
					else {
						alert("Debit and Credit sides are not same");
					}

				});


				$(".add-item-cpv").click(function(){
					var account_title = $('#account_title').val();
					req =	$.ajax({
						 headers: { "X-CSRFToken": getCookie("csrftoken") },
						 type: 'POST',
						 data:{
							 'account_title': account_title,
						 },
						 dataType: 'json'
					 })
					 .done(function done(data){
							 var index = $("table tbody tr:last-child").index();
									 var row = '<tr>' +
											 '<td>'+ data.account_id +'</td>' +
											 '<td>'+ data.account_title +'</td>' +
											 '<td><input type="text" class="form-control" required value="0.00"></td>' +
											 '<td><input type="text" class="form-control" required value="0.00"></td>' +
								 '<td><a class="add-jv" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-jv" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete-jv" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
									 '</tr>';
								 $("table").append(row);
							 $("table tbody tr").eq(index + 1).find(".add-jv, .edit-jv").toggle();
									 $('[data-toggle="tooltip"]').tooltip();

					 })
				});


					$('#new-jv-form-cpv').on('submit',function(e){
						e.preventDefault();
						var table = $('#new-jv-table');
						var data = [];
						var debit = 0;
						var credit = 0;
						var doc_no = $('#doc_no').val();
						var doc_date = $('#doc_date').val();
						var description = $('#description').val();

						table.find('tr').each(function (i, el){
							if(i != 0)
							{
								var $tds = $(this).find('td');
								var row = {
									'account_id' : "",
									'account_title' : "",
									'debit' : "",
									'credit' : "",
								};
								$tds.each(function(i, el){
									if (i === 0) {
											row["account_id"] = ($(this).text());
									}
									if (i === 1) {
											row["account_title"] = ($(this).text());
									}
									else if (i === 2) {
											row["debit"] = ($(this).text());
											debit = debit + parseFloat(($(this).text()));
									}
									else if (i === 3) {
											row["credit"] = ($(this).text());
											credit = credit + parseFloat(($(this).text()));
									}
								});
								data.push(row);
							}
						});
						if (debit == credit) {
							req =	$.ajax({
								 headers: { "X-CSRFToken": getCookie("csrftoken") },
								 type: 'POST',
								 url : '/transaction/cash_payment_voucher/new',
								 data:{
									 'doc_no': doc_no,
									 'doc_date': doc_date,
									 'description': description,
									 'items': JSON.stringify(data),
								 },
								 dataType: 'json'
							 })
							 .done(function done(data){
								 if (data.result != "success") {
									 alert(data.result)
								 }
								 else {
									 alert("CP Voucher Submitted");
									 location.reload();
								 }
							 })
						}
						else {
							alert("Debit and Credit sides are not same");
						}

					});

					$(".add-item-brv").click(function(){
						var account_title = $('#account_title').val();
						req =	$.ajax({
							 headers: { "X-CSRFToken": getCookie("csrftoken") },
							 type: 'POST',
							 data:{
								 'account_title': account_title,
							 },
							 dataType: 'json'
						 })
						 .done(function done(data){
								 var index = $("table tbody tr:last-child").index();
										 var row = '<tr>' +
												 '<td>'+ data.account_id +'</td>' +
												 '<td>'+ data.account_title +'</td>' +
												 '<td><input type="text" class="form-control" required value="0.00"></td>' +
												 '<td><input type="text" class="form-control" required value="0.00"></td>' +
									 '<td><a class="add-jv" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-jv" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete-jv" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
										 '</tr>';
									 $("table").append(row);
								 $("table tbody tr").eq(index + 1).find(".add-jv, .edit-jv").toggle();
										 $('[data-toggle="tooltip"]').tooltip();

						 })
					});


						$('#new-jv-form-brv').on('submit',function(e){
							e.preventDefault();
							var table = $('#new-jv-table');
							var data = [];
							var debit = 0;
							var credit = 0;

							var doc_no = $('#doc_no').val();
							var doc_date = $('#doc_date').val();
							var description = $('#description').val();
							var cheque_no = $('#cheque_no').val();
							var cheque_date = $('#cheque_date').val();

							table.find('tr').each(function (i, el){
								if(i != 0)
								{
									var $tds = $(this).find('td');
									var row = {
										'account_id' : "",
										'account_title' : "",
										'debit' : "",
										'credit' : "",
									};
									$tds.each(function(i, el){
										if (i === 0) {
												row["account_id"] = ($(this).text());
										}
										if (i === 1) {
												row["account_title"] = ($(this).text());
										}
										else if (i === 2) {
												row["debit"] = ($(this).text());
												debit = debit + parseFloat(($(this).text()));
										}
										else if (i === 3) {
												row["credit"] = ($(this).text());
												credit = credit + parseFloat(($(this).text()));
										}
									});
									data.push(row);
								}
							});
							if (debit == credit) {
								req =	$.ajax({
									 headers: { "X-CSRFToken": getCookie("csrftoken") },
									 type: 'POST',
									 url : '/transaction/bank_receiving_voucher/new',
									 data:{
										 'doc_no': doc_no,
										 'doc_date': doc_date,
										 'description': description,
										 'cheque_no': cheque_no,
										 'cheque_date': cheque_date,
										 'items': JSON.stringify(data),
									 },
									 dataType: 'json'
								 })
								 .done(function done(data){
									 if (data.result != "success") {
										 alert(data.result)
									 }
									 else {
										 alert("BR Voucher Submitted");
										 location.reload();
									 }
								 })
							}
							else {
								alert("Debit and Credit sides are not same");
							}

						});


						$(".add-item-bpv").click(function(){
							var account_title = $('#account_title').val();
							req =	$.ajax({
								 headers: { "X-CSRFToken": getCookie("csrftoken") },
								 type: 'POST',
								 data:{
									 'account_title': account_title,
								 },
								 dataType: 'json'
							 })
							 .done(function done(data){
									 var index = $("table tbody tr:last-child").index();
											 var row = '<tr>' +
													 '<td>'+ data.account_id +'</td>' +
													 '<td>'+ data.account_title +'</td>' +
													 '<td><input type="text" class="form-control" required value="0.00"></td>' +
													 '<td><input type="text" class="form-control" required value="0.00"></td>' +
										 '<td><a class="add-jv" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-jv" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete-jv" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
											 '</tr>';
										 $("table").append(row);
									 $("table tbody tr").eq(index + 1).find(".add-jv, .edit-jv").toggle();
											 $('[data-toggle="tooltip"]').tooltip();

							 })
						});


							$('#new-jv-form-bpv').on('submit',function(e){
								e.preventDefault();
								var table = $('#new-jv-table');
								var data = [];
								var debit = 0;
								var credit = 0;

								var doc_no = $('#doc_no').val();
								var doc_date = $('#doc_date').val();
								var description = $('#description').val();
								var cheque_no = $('#cheque_no').val();
								var cheque_date = $('#cheque_date').val();

								table.find('tr').each(function (i, el){
									if(i != 0)
									{
										var $tds = $(this).find('td');
										var row = {
											'account_id' : "",
											'account_title' : "",
											'debit' : "",
											'credit' : "",
										};
										$tds.each(function(i, el){
											if (i === 0) {
													row["account_id"] = ($(this).text());
											}
											if (i === 1) {
													row["account_title"] = ($(this).text());
											}
											else if (i === 2) {
													row["debit"] = ($(this).text());
													debit = debit + parseFloat(($(this).text()));
											}
											else if (i === 3) {
													row["credit"] = ($(this).text());
													credit = credit + parseFloat(($(this).text()));
											}
										});
										data.push(row);
									}
								});
								if (debit == credit) {
									req =	$.ajax({
										 headers: { "X-CSRFToken": getCookie("csrftoken") },
										 type: 'POST',
										 url : '/transaction/bank_payment_voucher/new',
										 data:{
											 'doc_no': doc_no,
											 'doc_date': doc_date,
											 'description': description,
											 'cheque_no': cheque_no,
											 'cheque_date': cheque_date,
											 'items': JSON.stringify(data),
										 },
										 dataType: 'json'
									 })
									 .done(function done(data){
										 if (data.result != "success") {
											 alert(data.result)
										 }
										 else {
											 alert("BP Voucher Submitted");
											 location.reload();
										 }
									 })
								}
								else {
									alert("Debit and Credit sides are not same");
								}

							});



//Initialization of treeviews

		$('#tree1').treed();

		$('#sales_tax_invoice').on('click', function(){
			var win = window.open(`/transaction/sales_tax_invoice/pdf/${edit_id}`, '_blank');
				if (win) {
				    //Browser has allowed it to be opened
				    win.focus();
				} else {
				    //Browser has blocked it
				    alert('Please allow popups for this website');
				}
		})

		$('#commercial_invoice').on('click', function(){
			var win = window.open(`/transaction/commercial_invoice/pdf/${edit_id}`, '_blank');
				if (win) {
						//Browser has allowed it to be opened
						win.focus();
				} else {
						//Browser has blocked it
						alert('Please allow popups for this website');
				}
		})

	$('#payment_method').change(function(){
		  var data= $(this).val();
		  if (data === 'Cash') {
				$('#credit_days').attr('readonly', true)
		  }
			else{
				$('#credit_days').attr('readonly', false)
			}
		});

});
