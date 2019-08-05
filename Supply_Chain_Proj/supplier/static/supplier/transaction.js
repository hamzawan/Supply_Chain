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
	var sum_st = 0;
	var sum_add = 0;
	var cartage_amount;
	var additional_tax;
	var withholding_tax;
	var tax;
	var total_amount_row = 0;

			$('#new-sale-return-table tbody tr').each(function() {
				var tdObject = $(this).find('td:eq(10)');
				var total = tdObject.text()
				console.log(total);
				if (!isNaN(total) && total.length !== 0) {
						sum += parseFloat(total);
				}
				additional_tax = $('#additional_tax').val();
				cartage_amount = $('#cartage_amount').val();
				$('#last_grand_total').val((sum + parseFloat(additional_tax) + parseFloat(cartage_amount)).toFixed(2));
		});

		$('#new-sale-return-table tbody tr').each(function() {
			var sales_tax_td = $(this).find('td:eq(9)');
			var total_sales_tax = sales_tax_td.text()
			if (!isNaN(total_sales_tax) && total_sales_tax.length !== 0) {
					sum_st += parseFloat(total_sales_tax);
			}
			$('#total_sales_tax').val(sum_st.toFixed(2));
	});

	$(".has_id").click(function(){
			 edit_id = this.id;
			 console.log("HERE",edit_id);
			 $.get("chart_of_account/edit/"+ edit_id, function(data, status){
				alert("Data: " + data + "\nStatus: " + status);
			});
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
										 '<td style="display:none;">'+type[0]['pk']+'</td>' +
										 '<td>'+type[0].fields['product_code'] +'</td>' +
										 '<td>'+type[0].fields['product_name'] +'</td>' +
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
							if (i === 4) {
								$(this).html('<input type="text" style="width:60px;" class="form-control" value="' + $(this).text() + '">');
							}
							if (i === 6) {
								 $(this).html('<input type="text" style="width:60px;" class="form-control" value="' + $(this).text() + '">');
							}
							if (i === 8) {
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
								'id' : "",
								'quantity' : "",
								'price' : "",
								'sales_tax' : "",
							};
							$tds.each(function(i, el){
								if (i === 0) {
										row["id"] = ($(this).text());
								}
								else if (i === 4) {
										row["quantity"] = ($(this).text());
								}
								else if (i === 6) {
										row["price"] = ($(this).text());
								}
								else if (i === 8) {
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

			$('#edit-purchase-table tbody tr').each(function() {
				var tdObject = $(this).find('td:eq(10)');
				var total = tdObject.text()
				if (!isNaN(total) && total.length !== 0) {
						sum_add += parseFloat(total);
				}
				additional_tax = $('#additional_tax_edit').val();
				cartage_amount = $('#cartage_amount_edit').val();
				$('#last_grand_total').val((sum_add + parseFloat(additional_tax) + parseFloat(cartage_amount)).toFixed(2));
			});

			$('#edit-purchase-table tbody tr').each(function() {
			var sales_tax = $(this).find('td:eq(9)');
			var total_sales_tax = sales_tax.text()
			if (!isNaN(total_sales_tax) && total_sales_tax.length !== 0) {
					sum_st += parseFloat(total_sales_tax);
			}
			$('#total_sales_tax').val(sum_st.toFixed(2));
			});

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
					 		 '<td style="display:none;">'+type[0]['pk']+'</td>' +
							 '<td>'+type[0].fields['product_code']+'</td>' +
							 '<td>'+type[0].fields['product_name']+'</td>' +
							 '<td id="desc" ><pre>'+type[0].fields['product_desc']+'</pre></td>' +
							 '<td id="quantity_edit" ><input type="text" class="form-control" value=""></td>' +
							 '<td>'+type[0].fields['unit']+'</td>' +
							 '<td id="price_edit" ><input type="text" class="form-control" value=""></td>' +
							 '<td id="value_of_goods_edit" >0.00</td>' +
							 '<td id="sales_tax_edit"><input type="text" class="form-control" value=""></td>' +
							 '<td id="sales_tax_amount_edit">0.00</td>' +
							 '<td id="total_amount">0.00</td>' +
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

			var total_amount = $($(this).parents("tr").find("#total_amount")).filter(function() {
							total = value_of_goods + sales_tax
							$(this).text(total.toFixed(2));
							return total_amount;
					}).closest("tr");
			sum_add = 0;
			sum_st = 0;
			$('#edit-purchase-table tbody tr').each(function() {
				var tdObject = $(this).find('td:eq(10)');
				var total = tdObject.text()
				if (!isNaN(total) && total.length !== 0) {
						sum_add += parseFloat(total);
				}
				additional_tax = $('#additional_tax_edit').val();
				cartage_amount = $('#cartage_amount_edit').val();
				$('#last_grand_total').val((sum_add + parseFloat(additional_tax) + parseFloat(cartage_amount)).toFixed(2));
			});

			$('#edit-purchase-table tbody tr').each(function() {
			var sales_tax = $(this).find('td:eq(9)');
			var total_sales_tax = sales_tax.text()
			if (!isNaN(total_sales_tax) && total_sales_tax.length !== 0) {
					sum_st += parseFloat(total_sales_tax);
			}
			$('#total_sales_tax').val(sum_st.toFixed(2));
			});

	});

				// Edit row on edit button click
$(document).on("click", ".edit-transaction-edit", function(){
		$(this).parents("tr").find("td:not(:last-child)").each(function(i){
				if (i === 4) {
					$(this).html('<input type="text" style="width:70px;" class="form-control" value="' + $(this).text() + '">');
				}
				if (i === 6) {
					 $(this).html('<input type="text" style="width:70px;" class="form-control" value="' + $(this).text() + '">');
				}
				if (i === 8) {
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

		var cartage_amount = $('#cartage_amount_edit').val();
		var additional_tax = $('#additional_tax_edit').val();
		var withholding_tax = $('#withholding_tax').val();


		table.find('tr').each(function (i, el){
			if(i != 0)
			{
				var $tds = $(this).find('td');
				var row = {
					'id' : "",
					'quantity' : "",
					'unit' : "",
					'price' : "",
					'sales_tax' : "",
				};
				$tds.each(function(i, el){
					if (i === 0) {
							row["id"] = ($(this).text());
					}
					else if (i === 4) {
							row["quantity"] = ($(this).text());
					}
					else if (i === 6) {
							row["price"] = ($(this).text());
					}
					else if (i === 8) {
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
//
//
// $('#edit-purchase-return-submit').on('submit',function(e){
// 	e.preventDefault();
// 	var table = $('#new-purchase-return-table');
// 	var data = [];
// 	var purchase_id = $('#purchase_return_id').val();
// 	var supplier = $('#supplier_purchase_return_name').val();
// 	var payment_method = $('#payment_method').val();
// 	var footer_desc = $('#desc_purchase_return').val();
//
//
// 	table.find('tr').each(function (i, el){
// 		if(i != 0)
// 		{
// 			var $tds = $(this).find('td');
// 			var row = {
// 				'id': "",
// 				'quantity' : "",
// 				'price' : "",
// 				'sales_tax' : "",
// 			};
// 			$tds.each(function(i, el){
// 				if (i === 0) {
// 						row["id"] = ($(this).text());
// 				}
// 				else if (i === 4) {
// 						row["quantity"] = ($(this).text());
// 				}
// 				else if (i === 6) {
// 						row["price"] = ($(this).text());
// 				}
// 				else if (i === 7) {
// 						row["sales_tax"] = ($(this).text());
// 				}
// 			});
// 			data.push(row);
// 		}
// 	});
//
// 		 req =	$.ajax({
// 				headers: { "X-CSRFToken": getCookie("csrftoken") },
// 				type: 'POST',
// 				url : `/transaction/purchase/return/edit/${edit_id}`,
// 				data:{
// 					'purchase_id': purchase_id,
// 					'supplier': supplier,
// 					'payment_method': payment_method,
// 					'footer_desc': footer_desc,
// 					'items': JSON.stringify(data),
// 				},
// 				dataType: 'json'
// 			})
// 			.done(function done(){
// 				alert("Purchase Return Updated");
// 				location.reload();
// 			})
// });


// =============================================================================

					var all_dc = 'all_dc';
					req =	$.ajax({
						 headers: { "X-CSRFToken": getCookie("csrftoken") },
						 type: 'POST',
						 url : '/transaction/sale/new/',
						 data:{
							 'all_dc': all_dc,
						 },
						 dataType: 'json'
					 })
					 .done(function fun(data){
						 $('#dc').html('');
							 for (var j = 0; j < data.all_dc.length; j++) {
								 console.log(data.all_dc[j][1]);
									$("#dc").append($("<option>").attr('value',data.all_dc[j][1]).text(data.all_dc[j][1]));
							 }
					 });

					$('#customer_name_sale').on('focusout', function(){
						var customer_name_sale = $('#customer_name_sale').val();
						if (customer_name_sale) {
							req =	$.ajax({
								 headers: { "X-CSRFToken": getCookie("csrftoken") },
								 type: 'POST',
								 url : '/transaction/sale/new/',
								 data:{
									 'customer_name_sale': customer_name_sale,
								 },
								 dataType: 'json'
							 })
							 .done(function fun(data){
								 $('#dc').html('');
								 if (data.customer_dc === 'False') {
									 alert("No Account found");
								 }
								 else {
									 console.log(data.customer_dc);
									 for (var j = 0; j < data.customer_dc.length; j++) {
											$("#dc").append($("<option>").attr('value',data.customer_dc[j][1]).text(data.customer_dc[j][1]));
									 }
								 }
							 });
						}
						else{
							var all_dc = 'all_dc';
							req =	$.ajax({
								 headers: { "X-CSRFToken": getCookie("csrftoken") },
								 type: 'POST',
								 url : '/transaction/sale/new/',
								 data:{
									 'all_dc': all_dc,
								 },
								 dataType: 'json'
							 })
							 .done(function fun(data){
								 $('#dc').html('');
									 for (var j = 0; j < data.all_dc.length; j++) {
										 console.log(data.all_dc[j][1]);
											$("#dc").append($("<option>").attr('value',data.all_dc[j][1]).text(data.all_dc[j][1]));
									 }
							 });
						}
					})


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
											'<td >'+count+'</td>'+
											'<td style="display:none;">'+data.row[i][1]+'</td>'+
											'<td id="get_item_code">'+data.row[i][2]+'</td>' +
											'<td><input type="text" list="hs_code" style="width:100px;" class="form-control" ></input><datalist id="hs_code"></datalist></td>' +
											'<td>'+data.row[i][3]+'</td>' +
											'<td id="desc" ><pre>'+data.row[i][4]+'</pre></td>' +
											'<td id="quantity"><input type="text" style="width:80px;" class="form-control" value="'+data.row[i][8]+'"></td>' +
											'<td>'+data.row[i][5]+'</td>' +
											'<td id="price" ><input type="text" style="width:80px;" class="form-control" value=""></td>' +
											'<td id="value_of_goods" >0.00</td>' +
											'<td id="sales_tax"><input type="text" style="width:80px;" class="form-control" value="17"></td>' +
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
											 '<td style="display:none;">'+type[0]['pk']+'</td>' +
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
								if (i === 6) {
									$(this).html('<input type="text" style="width:80px;" class="form-control" value="' + $(this).text() + '">');
								}
								if (i === 8) {
									 $(this).html('<input type="text" style="width:80px;" class="form-control" value="' + $(this).text() + '">');
								}
								if (i === 10) {
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
							'id' : "",
							'hs_code': "",
							'quantity' : "",
							'price' : "",
							'sales_tax' : "",
							'dc_no': ""
						};
						$tds.each(function(i, el){
							if (i === 1) {
									row["id"] = ($(this).text());
									console.log($(this).text());
							}
							if (i === 3) {
									row["hs_code"] = ($(this).text());
									console.log($(this).text());
							}
							else if (i === 6) {
									row["quantity"] = ($(this).text());
							}
							else if (i === 8) {
									row["price"] = ($(this).text());
							}
							else if (i === 10) {
									row["sales_tax"] = ($(this).text());
							}
							else if (i === 13) {
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
							'id' : "",
							'hs_code': "",
							'quantity' : "",
							'price' : "",
							'sales_tax' : "",
							'dc_no': ""
						};
						$tds.each(function(i, el){
							if (i === 1) {
									row["id"] = ($(this).text());
							}
							if (i === 3) {
									row["hs_code"] = ($(this).text());
							}
							else if (i === 6) {
									row["quantity"] = ($(this).text());
							}
							else if (i === 8) {
									row["price"] = ($(this).text());
							}
							else if (i === 10) {
									row["sales_tax"] = ($(this).text());
							}
							else if (i === 13) {
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
							sum_add = 0;
							sum_st = 0;
							$('#new-purchase-return-table tbody tr').each(function() {

								var tdObject_add = $(this).find('td:eq(10)');
								var total_add = tdObject_add.text()
								if (!isNaN(total_add) && total_add.length !== 0) {
										sum_add += parseFloat(total_add);
								}
								additional_tax = $('#additional_tax').val();
								cartage_amount = $('#cartage_amount').val();
								$('#last_grand_total').val((sum_add + parseFloat(additional_tax) + parseFloat(cartage_amount)).toFixed(2));
								console.log(sum_add);
						});

						$('#new-purchase-return-table tbody tr').each(function() {
							var sales_tax_td = $(this).find('td:eq(9)');
							var total_sales_tax = sales_tax_td.text()
							if (!isNaN(total_sales_tax) && total_sales_tax.length !== 0) {
									sum_st += parseFloat(total_sales_tax);
							}
							console.log(sum_st);
							$('#total_sales_tax').val(sum_st.toFixed(2));
						});
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

								var get_quantity = $($(this).parents("tr").find("#quantity")).filter(function() {
												quantity = $(this).text();
												return quantity
										}).closest("tr");
								var get_price = $($(this).parents("tr").find("#price")).filter(function() {
												price = $(this).text();
												return price
										}).closest("tr");
								var get_sales_tax_amount = $($(this).parents("tr").find("#sales_tax")).filter(function() {
												sales_tax_amount = $(this).text();
												return sales_tax_amount
										}).closest("tr");
								st_total_amount_row = (parseFloat(quantity) * parseFloat(price) * parseFloat(sales_tax_amount) / 100)
								var sales_tax_amount_row = $($(this).parents("tr").find("#sales_tax_amount")).filter(function() {
												sales_tax_amount_row = $(this).text(st_total_amount_row);
												return sales_tax_amount_row
										}).closest("tr");
								total_amount_row = (parseFloat(quantity) * parseFloat(price) + parseFloat(st_total_amount_row))
								console.log(total_amount_row);
								var total = $($(this).parents("tr").find("#total")).filter(function() {
												total = $(this).text(total_amount_row.toFixed(2));
												return total
										}).closest("tr");

								var total = $($(this).parents("tr").find("#total")).filter(function() {
												total = $(this).text(total_amount_row.toFixed(2));
												return total
										}).closest("tr");

								sum_add = 0;
								sum_st = 0;
								$('#new-purchase-return-table tbody tr').each(function() {

									var tdObject_add = $(this).find('td:eq(10)');
									var total_add = tdObject_add.text()
									if (!isNaN(total_add) && total_add.length !== 0) {
											sum_add += parseFloat(total_add);
									}
									additional_tax = $('#additional_tax').val();
									cartage_amount = $('#cartage_amount').val();
									$('#last_grand_total').val((sum_add + parseFloat(additional_tax) + parseFloat(cartage_amount)).toFixed(2));
									console.log(sum_add);
							});

							$('#new-purchase-return-table tbody tr').each(function() {
								var sales_tax_td = $(this).find('td:eq(9)');
								var total_sales_tax = sales_tax_td.text()
								if (!isNaN(total_sales_tax) && total_sales_tax.length !== 0) {
										sum_st += parseFloat(total_sales_tax);
								}
								console.log(sum_st);
								$('#total_sales_tax').val(sum_st.toFixed(2));
							});
								});


								// Edit row on edit button click
								$(document).on("click", ".edit-purchase-return", function(){
										$(this).parents("tr").find("td:not(:last-child)").each(function(i){
											if (i === 5) {
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
								});

							//SUBMIT EDIT MRN SUPPLIER

							//updating data into supplier mrn using ajax request
							$('#new-purchase-return-submit').on('submit',function(e){
								e.preventDefault();
								console.log("clickde");
								var table = $('#new-purchase-return-table');
								var supplier = $('#supplier').val();
								var payment_method = $('#payment_method').val();
								var credit_days = $('#credit_days').val();
								var cartage_amount = $('#cartage_amount').val();
								var additional_tax = $('#additional_tax').val();
								var description = $('#footer_desc').val();
								console.log(supplier);
								var data = [];
								table.find('tr').each(function (i, el){
									if(i != 0)
									{
										var $tds = $(this).find('td');
										var row = {
											'id' : "",
											'quantity' : "",
											'price' : "",
											'sales_tax' : "",
										};
										$tds.each(function(i, el){
											if (i === 1) {
													row["id"] = ($(this).text());
											}
											else if (i === 5) {
													row["quantity"] = ($(this).text());

											}
											else if (i === 7) {
													row["price"] = ($(this).text());
											}
											else if (i === 8) {
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
												'description': description,
												'credit_days' : credit_days,
												'cartage_amount': cartage_amount,
												'additional_tax': additional_tax,
												'payment_method': payment_method,
												'items': JSON.stringify(data),
											},
											dataType: 'json'
										})
										.done(function done(){
											alert("Purchase Return Submit");
											location.reload();
										})
							});
							// // ==================================================================================================================================
							// EDIT PURCHASE RETURN
							sum_add = 0;
							sum_st = 0;
							$('#edit-purchase-return-table tbody tr').each(function() {

								var tdObject_add = $(this).find('td:eq(10)');
								var total_add = tdObject_add.text()
								if (!isNaN(total_add) && total_add.length !== 0) {
										sum_add += parseFloat(total_add);
								}
								additional_tax = $('#additional_tax_edit').val();
								cartage_amount = $('#cartage_amount_edit').val();
								$('#last_grand_total').val((sum_add + parseFloat(additional_tax) + parseFloat(cartage_amount)).toFixed(2));
								console.log(sum_add);
						});

						$('#edit-purchase-return-table tbody tr').each(function() {
							var sales_tax_td = $(this).find('td:eq(9)');
							var total_sales_tax = sales_tax_td.text()
							if (!isNaN(total_sales_tax) && total_sales_tax.length !== 0) {
									sum_st += parseFloat(total_sales_tax);
							}
							console.log(sum_st);
							$('#total_sales_tax').val(sum_st.toFixed(2));
						});
								// Add row on add button click
								$(document).on("click", ".add-purchase-return-edit", function(){
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
									$(this).parents("tr").find(".add-purchase-return-edit, .edit-purchase-return-edit").toggle();
								}

								var get_quantity = $($(this).parents("tr").find("#quantity")).filter(function() {
												quantity = $(this).text();
												return quantity
										}).closest("tr");
								var get_price = $($(this).parents("tr").find("#price")).filter(function() {
												price = $(this).text();
												return price
										}).closest("tr");
								var get_sales_tax_amount = $($(this).parents("tr").find("#sales_tax")).filter(function() {
												sales_tax_amount = $(this).text();
												return sales_tax_amount
										}).closest("tr");
								st_total_amount_row = (parseFloat(quantity) * parseFloat(price) * parseFloat(sales_tax_amount) / 100)
								var sales_tax_amount_row = $($(this).parents("tr").find("#sales_tax_amount")).filter(function() {
												sales_tax_amount_row = $(this).text(st_total_amount_row);
												return sales_tax_amount_row
										}).closest("tr");
								total_amount_row = (parseFloat(quantity) * parseFloat(price) + parseFloat(st_total_amount_row))
								console.log(total_amount_row);
								var total = $($(this).parents("tr").find("#total")).filter(function() {
												total = $(this).text(total_amount_row.toFixed(2));
												return total
										}).closest("tr");

								var total = $($(this).parents("tr").find("#total")).filter(function() {
												total = $(this).text(total_amount_row.toFixed(2));
												return total
										}).closest("tr");

								sum_add = 0;
								sum_st = 0;
								$('#new-purchase-return-table tbody tr').each(function() {

									var tdObject_add = $(this).find('td:eq(10)');
									var total_add = tdObject_add.text()
									if (!isNaN(total_add) && total_add.length !== 0) {
											sum_add += parseFloat(total_add);
									}
									additional_tax = $('#additional_tax').val();
									cartage_amount = $('#cartage_amount').val();
									$('#last_grand_total').val((sum_add + parseFloat(additional_tax) + parseFloat(cartage_amount)).toFixed(2));
									console.log(sum_add);
							});

							$('#new-purchase-return-table tbody tr').each(function() {
								var sales_tax_td = $(this).find('td:eq(9)');
								var total_sales_tax = sales_tax_td.text()
								if (!isNaN(total_sales_tax) && total_sales_tax.length !== 0) {
										sum_st += parseFloat(total_sales_tax);
								}
								console.log(sum_st);
								$('#total_sales_tax').val(sum_st.toFixed(2));
							});
								});


								// Edit row on edit button click
								$(document).on("click", ".edit-purchase-return-edit", function(){
										$(this).parents("tr").find("td:not(:last-child)").each(function(i){
											if (i === 5) {
												$(this).html('<input type="text" class="form-control form-control-sm" style="width:100px;" value="' + $(this).text() + '">');
											}
								});
								$(this).parents("tr").find(".add-purchase-return-edit, .edit-purchase-return-edit").toggle();
								});


								// Delete row on delete button click
								$(document).on("click", ".delete-purchase-return-edit", function(){
									var row =  $(this).closest('tr');
									var siblings = row.siblings();
									siblings.each(function(index) {
									$(this).children('td').first().text(index + 1);
									});
									$(this).parents("tr").remove();
								});

							//SUBMIT EDIT MRN SUPPLIER

							//updating data into supplier mrn using ajax request
							$('#edit-purchase-return-submit').on('submit',function(e){
								e.preventDefault();
								var table = $('#edit-purchase-return-table');
								var supplier = $('#supplier').val();
								var cartage_amount = $('#cartage_amount_edit').val();
								var additional_tax = $('#additional_tax_edit').val();
								var description = $('#footer_desc').val();
								var data = [];
								table.find('tr').each(function (i, el){
									if(i != 0)
									{
										var $tds = $(this).find('td');
										var row = {
											'id' : "",
											'quantity' : "",
											'price' : "",
											'sales_tax' : "",
										};
										$tds.each(function(i, el){
											if (i === 1) {
													row["id"] = ($(this).text());
											}
											else if (i === 5) {
													row["quantity"] = ($(this).text());

											}
											else if (i === 7) {
													row["price"] = ($(this).text());
											}
											else if (i === 8) {
													row["sales_tax"] = ($(this).text());
											}
										});
										console.log(data);
										data.push(row);
									}
								});
									 req =	$.ajax({
											headers: { "X-CSRFToken": getCookie("csrftoken") },
											type: 'POST',
											url : `/transaction/purchase/return/edit/${edit_id}/`,
											data:{
												'supplier':supplier,
												'description': description,
												'cartage_amount': cartage_amount,
												'additional_tax': additional_tax,
												'items': JSON.stringify(data),
											},
											dataType: 'json'
										})
										.done(function done(){
											alert("Purchase Return Updated");
											location.reload();
										})
							});

// ================================================================================================

							// EDIT PURCHASE RETURN
							sum_add = 0;
							sum_st = 0;
							$('#edit-sale-return-table tbody tr').each(function() {

								var tdObject_add = $(this).find('td:eq(10)');
								var total_add = tdObject_add.text()
								if (!isNaN(total_add) && total_add.length !== 0) {
										sum_add += parseFloat(total_add);
								}
								additional_tax = $('#additional_tax_edit').val();
								cartage_amount = $('#cartage_amount_edit').val();
								$('#last_grand_total').val((sum_add + parseFloat(additional_tax) + parseFloat(cartage_amount)).toFixed(2));
								console.log(sum_add);
						});

						$('#edit-sale-return-table tbody tr').each(function() {
							var sales_tax_td = $(this).find('td:eq(9)');
							var total_sales_tax = sales_tax_td.text()
							if (!isNaN(total_sales_tax) && total_sales_tax.length !== 0) {
									sum_st += parseFloat(total_sales_tax);
							}
							console.log(sum_st);
							$('#total_sales_tax').val(sum_st.toFixed(2));
						});
								// Add row on add button click
								$(document).on("click", ".add-sale-return-edit", function(){
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
									$(this).parents("tr").find(".add-sale-return-edit, .edit-sale-return-edit").toggle();
								}

								var get_quantity = $($(this).parents("tr").find("#quantity")).filter(function() {
												quantity = $(this).text();
												return quantity
										}).closest("tr");
								var get_price = $($(this).parents("tr").find("#price")).filter(function() {
												price = $(this).text();
												return price
										}).closest("tr");
								var get_sales_tax_amount = $($(this).parents("tr").find("#sales_tax")).filter(function() {
												sales_tax_amount = $(this).text();
												return sales_tax_amount
										}).closest("tr");
								st_total_amount_row = (parseFloat(quantity) * parseFloat(price) * parseFloat(sales_tax_amount) / 100)
								var sales_tax_amount_row = $($(this).parents("tr").find("#sales_tax_amount")).filter(function() {
												sales_tax_amount_row = $(this).text(st_total_amount_row);
												return sales_tax_amount_row
										}).closest("tr");
								total_amount_row = (parseFloat(quantity) * parseFloat(price) + parseFloat(st_total_amount_row))
								console.log(total_amount_row);
								var total = $($(this).parents("tr").find("#total")).filter(function() {
												total = $(this).text(total_amount_row.toFixed(2));
												return total
										}).closest("tr");

								var total = $($(this).parents("tr").find("#total")).filter(function() {
												total = $(this).text(total_amount_row.toFixed(2));
												return total
										}).closest("tr");

								sum_add = 0;
								sum_st = 0;
								$('#edit-sale-return-table tbody tr').each(function() {

									var tdObject_add = $(this).find('td:eq(10)');
									var total_add = tdObject_add.text()
									if (!isNaN(total_add) && total_add.length !== 0) {
											sum_add += parseFloat(total_add);
									}
									additional_tax = $('#additional_tax_edit').val();
									cartage_amount = $('#cartage_amount_edit').val();
									$('#last_grand_total').val((sum_add + parseFloat(additional_tax) + parseFloat(cartage_amount)).toFixed(2));
									console.log(sum_add);
							});

							$('#edit-sale-return-table tbody tr').each(function() {
								var sales_tax_td = $(this).find('td:eq(9)');
								var total_sales_tax = sales_tax_td.text()
								if (!isNaN(total_sales_tax) && total_sales_tax.length !== 0) {
										sum_st += parseFloat(total_sales_tax);
								}
								console.log(sum_st);
								$('#total_sales_tax').val(sum_st.toFixed(2));
							});
								});


								// Edit row on edit button click
								$(document).on("click", ".edit-sale-return-edit", function(){
										$(this).parents("tr").find("td:not(:last-child)").each(function(i){
											if (i === 5) {
												$(this).html('<input type="text" class="form-control form-control-sm" style="width:100px;" value="' + $(this).text() + '">');
											}
								});
								$(this).parents("tr").find(".add-sale-return-edit, .edit-sale-return-edit").toggle();
								});


								// Delete row on delete button click
								$(document).on("click", ".delete-sale-return-edit", function(){
									var row =  $(this).closest('tr');
									var siblings = row.siblings();
									siblings.each(function(index) {
									$(this).children('td').first().text(index + 1);
									});
									$(this).parents("tr").remove();
								});


							//updating data into supplier mrn using ajax request
							$('#edit-sale-return-submit').on('submit',function(e){
								e.preventDefault();
								var table = $('#edit-sale-return-table');
								var customer = $('#customer').val();
								var cartage_amount = $('#cartage_amount_edit').val();
								var additional_tax = $('#additional_tax_edit').val();
								var description = $('#footer_desc').val();
								var data = [];
								table.find('tr').each(function (i, el){
									if(i != 0)
									{
										var $tds = $(this).find('td');
										var row = {
											'id' : "",
											'quantity' : "",
											'price' : "",
											'sales_tax' : "",
										};
										$tds.each(function(i, el){
											if (i === 1) {
													row["id"] = ($(this).text());
											}
											else if (i === 5) {
													row["quantity"] = ($(this).text());

											}
											else if (i === 7) {
													row["price"] = ($(this).text());
											}
											else if (i === 8) {
													row["sales_tax"] = ($(this).text());
											}
										});
										console.log(data);
										data.push(row);
									}
								});
									 req =	$.ajax({
											headers: { "X-CSRFToken": getCookie("csrftoken") },
											type: 'POST',
											url : `/transaction/sale/return/edit/${edit_id}`,
											data:{
												'customer':customer,
												'description': description,
												'cartage_amount': cartage_amount,
												'additional_tax': additional_tax,
												'items': JSON.stringify(data),
											},
											dataType: 'json'
										})
										.done(function done(){
											alert("Sale Return Updated");
											location.reload();
										})
							});

// // ==================================================================================================================================

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

								var get_quantity = $($(this).parents("tr").find("#quantity")).filter(function() {
												quantity = $(this).text();
												return quantity
										}).closest("tr");
								var get_price = $($(this).parents("tr").find("#price")).filter(function() {
												price = $(this).text();
												return price
										}).closest("tr");
								var get_sales_tax_amount = $($(this).parents("tr").find("#sales_tax")).filter(function() {
												sales_tax_amount = $(this).text();
												return sales_tax_amount
										}).closest("tr");
								st_total_amount_row = (parseFloat(quantity) * parseFloat(price) * parseFloat(sales_tax_amount) / 100)
								var sales_tax_amount_row = $($(this).parents("tr").find("#sales_tax_amount")).filter(function() {
												sales_tax_amount_row = $(this).text(st_total_amount_row);
												return sales_tax_amount_row
										}).closest("tr");
								total_amount_row = (parseFloat(quantity) * parseFloat(price) + parseFloat(st_total_amount_row))
								console.log(total_amount_row);
								var total = $($(this).parents("tr").find("#total")).filter(function() {
												total = $(this).text(total_amount_row.toFixed(2));
												return total
										}).closest("tr");

								var total = $($(this).parents("tr").find("#total")).filter(function() {
												total = $(this).text(total_amount_row.toFixed(2));
												return total
										}).closest("tr");

								sum_add = 0;
								sum_st = 0;
								$('#new-sale-return-table tbody tr').each(function() {

									var tdObject_add = $(this).find('td:eq(10)');
									var total_add = tdObject_add.text()
									if (!isNaN(total_add) && total_add.length !== 0) {
											sum_add += parseFloat(total_add);
									}
									additional_tax = $('#additional_tax').val();
									cartage_amount = $('#cartage_amount').val();
									$('#last_grand_total').val((sum_add + parseFloat(additional_tax) + parseFloat(cartage_amount)).toFixed(2));
							});

							$('#new-sale-return-table tbody tr').each(function() {
								var sales_tax_td = $(this).find('td:eq(9)');
								var total_sales_tax = sales_tax_td.text()
								if (!isNaN(total_sales_tax) && total_sales_tax.length !== 0) {
										sum_st += parseFloat(total_sales_tax);
								}
								$('#total_sales_tax').val(sum_st.toFixed(2));
						});
								});

								// Edit row on edit button click
								$(document).on("click", ".edit-sale-return", function(){
										$(this).parents("tr").find("td:not(:last-child)").each(function(i){
											if (i === 5) {
												$(this).html('<input type="text" class="form-control form-control-sm" value="' + $(this).text() + '">');
											}
								});
								$(this).parents("tr").find(".add-sale-return, .edit-sale-return").toggle();
								});


								// Delete row on delete button click
								$(document).on("click", ".delete-sale-return", function(){
									var row =  $(this).closest('tr');
									var siblings = row.siblings();
									siblings.each(function(index) {
									$(this).children('td').first().text(index + 1);
									});
									$(this).parents("tr").remove();
								});


							//updating data into supplier mrn using ajax request
							$('#new-sale-return-submit').on('submit',function(e){
								e.preventDefault();
								var table = $('#new-sale-return-table');
								var customer = $('#customer_sale_return').val();
								var payment_method = $('#payment_sale_return').val();
								var description = $('#desc_sale_return').val();
								var cartage_amount = $('#cartage_amount').val();
								var additional_tax = $('#additional_tax').val();
								var data = [];
								table.find('tr').each(function (i, el){
									if(i != 0)
									{
										var $tds = $(this).find('td');
										var row = {
											'item_id' : "",
											'quantity' : "",
											'price' : "",
											'sales_tax' : "",
										};
										$tds.each(function(i, el){
											if (i === 1) {
													row["item_id"] = ($(this).text());
											}
											else if (i === 5) {
													row["quantity"] = ($(this).text());
											}
											else if (i === 7) {
													row["price"] = ($(this).text());
											}
											else if (i === 8) {
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
											alert("Sale Return Submit");
											location.reload();
										})
							});

//=======================================================================================

		$('#edit-sale-table tbody tr').each(function() {
			var tdObject = $(this).find('td:eq(11)');
			var total = tdObject.text()
			console.log(total);
			if (!isNaN(total) && total.length !== 0) {
					sum_add += parseFloat(total);
			}
			additional_tax = $('#additional_tax_edit').val();
			cartage_amount = $('#cartage_amount_edit').val();
			$('#last_grand_total').val((sum_add + parseFloat(additional_tax) + parseFloat(cartage_amount)).toFixed(2));
		});

		$('#edit-sale-table tbody tr').each(function() {
		var sales_tax = $(this).find('td:eq(10)');
		var total_sales_tax = sales_tax.text()
		if (!isNaN(total_sales_tax) && total_sales_tax.length !== 0) {
				sum_st += parseFloat(total_sales_tax);
		}
		$('#total_sales_tax').val(sum_st.toFixed(2));
		});

		$(".add-item-sale-edit").click(function(){
			var item_code_sale = "";
			var dc_code_sale = $('#dc_code_sale').val();

			if (item_code_sale !== "") {
				//
				// req =	$.ajax({
				// 	 headers: { "X-CSRFToken": getCookie("csrftoken") },
				// 	 type: 'POST',
				// 	 url : '/transaction/sale/new/',
				// 	 data:{
				// 		 'item_code_sale': item_code_sale,
				// 	 },
				// 	 dataType: 'json'
				//  })
				//  .done(function done(data){
				// 	 console.log(data.row);
				// 	 var type = JSON.parse(data.row);
				// 	 console.log(type.length);
				// 	 var index = $("table tbody tr:last-child").index();
				// 	 // total_amount = (type[0].fields['unit_price'] * type[0].fields['quantity']);
				// 			 var row = '<tr>' +
				// 					 '<td>'+count+'</td>' +
				// 					 '<td id="get_item_code">'+type[0].fields['item_code']+'</td>' +
				// 					 '<td width="160px" id="hs_code"><input type="text" style="width:80px;" class="form-control" value=""></td>' +
				//
				// 					 '<td>'+type[0].fields['item_name']+'</td>' +
				// 					 '<td id="desc" ><pre>'+type[0].fields['item_description']+'</pre></td>' +
				// 					 '<td width="160px" id="quantity"><input type="text" style="width:80px;" class="form-control" value=""></td>' +
				// 					 '<td>'+type[0].fields['unit']+'</td>' +
				// 					 '<td id="price" ><input type="text" style="width:80px;" class="form-control" value=""></td>' +
				// 					 '<td id="value_of_goods" >0.00</td>' +
				// 					 '<td id="sales_tax"><input type="text" class="form-control" value=""></td>' +
				// 					 '<td id="sales_tax_amount">0.00</td>' +
				// 					 '<td id="total" style="font-weight:bold;" class="sum"><b>0.00</b></td>' +
				// 					 '<td style="display:none;">'+type[0].fields['dc_no']+'</td>' +
				// 		 '<td><a class="add-transaction-sale" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-transaction-sale" title="Edit" data-toggle="tooltip" id="edit_purchase"><i class="material-icons">&#xE254;</i></a><a class="delete-transaction-sale" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
				// 			 '</tr>';
				// 			 count++;
				// 		 $("table").append(row);
				// 	 $("table tbody tr").eq(index + 1).find(".edit-transaction-sale, .add-transaction-sale").toggle();
				// 			 $('[data-toggle="tooltip"]').tooltip();
				// 			 $('#item_code_sale').val("");
				//  });
			}
			else if (dc_code_sale !== "") {
				req =	$.ajax({
					 headers: { "X-CSRFToken": getCookie("csrftoken") },
					 type: 'POST',
					 url : `/transaction/sale/edit/${edit_id}`,
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
								'<td style="display:none;">'+data.row[i][1]+'</td>'+
								'<td id="get_item_code">'+data.row[i][2]+'</td>' +
								'<td><input type="text" list="hs_code" style="width:100px;" class="form-control" ></input><datalist id="hs_code"></datalist></td>' +
								'<td>'+data.row[i][3]+'</td>' +
								'<td id="desc" ><pre>'+data.row[i][4]+'</pre></td>' +
								'<td id="quantity_edit"><input type="text" style="width:80px;" class="form-control" value="'+data.row[i][8]+'"></td>' +
								'<td>'+data.row[i][5]+'</td>' +
								'<td id="price_edit" ><input type="text" style="width:80px;" class="form-control" value=""></td>' +
								'<td id="value_of_goods_edit" >0.00</td>' +
								'<td id="sales_tax_edit"><input type="text" style="width:80px;" class="form-control" value="17"></td>' +
								'<td id="sales_tax_amount_edit">0.00</td>' +
								'<td id="total_amount" style="font-weight:bold;" class="sum"><b>0.00</b></td>' +
								'<td style="display:none;">'+data.dc_ref+'</td>' +
					'<td><a class="add-sale-edit" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-sale-edit" title="Edit" data-toggle="tooltip" id="edit_purchase"><i class="material-icons">&#xE254;</i></a><a class="delete-sale-edit" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
						'</tr>';
						count++;
					$("table").append(row);
					$("table tbody tr").eq(index + i+1).find(".add-sale-edit, .edit-sale-edit").toggle();
						$('[data-toggle="tooltip"]').tooltip();
						$('#dc_code_sale').val("");
						for (var j = 1; j < data.hs_code.length; j++) {
							 $("#hs_code").append($("<option>").attr('value', data.hs_code[j]).text(data.hs_code[j]));
						}
					 }
				 });
			}
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

				var get_price = $($(this).parents("tr").find("#price_edit")).filter(function() {
								price = $(this).text();
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

						var total_amount = $($(this).parents("tr").find("#total_amount")).filter(function() {
										total = value_of_goods + sales_tax
										$(this).text(total.toFixed(2));
										return total_amount;
								}).closest("tr");


						sum_add = 0;
						sum_st = 0;
						$('#edit-sale-table tbody tr').each(function() {
							var tdObject = $(this).find('td:eq(11)');
							var total = tdObject.text()
							if (!isNaN(total) && total.length !== 0) {
									sum_add += parseFloat(total);
							}
							additional_tax = $('#additional_tax_edit').val();
							cartage_amount = $('#cartage_amount_edit').val();
							$('#last_grand_total').val((sum_add + parseFloat(additional_tax) + parseFloat(cartage_amount)).toFixed(2));
						});

						$('#edit-sale-table tbody tr').each(function() {
						var sales_tax = $(this).find('td:eq(10)');
						var total_sales_tax = sales_tax.text()
						if (!isNaN(total_sales_tax) && total_sales_tax.length !== 0) {
								sum_st += parseFloat(total_sales_tax);
						}
						$('#total_sales_tax').val(sum_st.toFixed(2));
						});


});

			// Edit row on edit button click
$(document).on("click", ".edit-sale-edit", function(){
	$(this).parents("tr").find("td:not(:last-child)").each(function(i){
			if (i === 5) {
				$(this).html('<input type="text" style="width:80px;" class="form-control" value="' + $(this).text() + '">');
			}
			if (i === 7) {
				$(this).html('<input type="text" style="width:80px;" class="form-control" value="' + $(this).text() + '">');
			}
			if (i === 9) {
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
	var table = $('#edit-sale-table');
	var data = [];
	var sale_id = $('#sale_id').val();
	var follow_up = $('#follow_up').val();
	var credit_days = $('#credit_days').val();
	var customer = $('#customer_name_sale').val();
	var payment_method = $('#payment_method').val();
	var footer_desc = $('#footer_desc').val();
	console.log(footer_desc);

	var cartage_amount = $('#cartage_amount_edit').val();
	var additional_tax = $('#additional_tax_edit').val();
	var withholding_tax = $('#withholding_tax').val();


	table.find('tr').each(function (i, el){
		if(i != 0)
		{
			var $tds = $(this).find('td');
			var row = {
				'id' : "",
				'quantity' : "",
				'hs_code': "",
				'price' : "",
				'sales_tax' : "",
				'dc_no': ""
			};
			$tds.each(function(i, el){
				if (i === 0) {
						row["id"] = ($(this).text());
				}
				if (i === 2) {
						row["hs_code"] = ($(this).text());
				}
				else if (i === 5) {
						row["quantity"] = ($(this).text());
				}
				else if (i === 7) {
						row["price"] = ($(this).text());
				}
				else if (i === 9) {
						row["sales_tax"] = ($(this).text());
				}
				else if (i === 12) {
						row["dc_no"] = ($(this).text());
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


			$('#edit-jv-form').on('submit',function(e){
				e.preventDefault();
				var table = $('#edit-jv-table');
				var data = [];
				var debit = 0;
				var credit = 0;
				var tran_id = $('#tran_id').val();
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
							if (i === 1) {
									row["account_id"] = ($(this).text());
							}
							if (i === 2) {
									row["account_title"] = ($(this).text());
							}
							else if (i === 3) {
									row["debit"] = ($(this).text());
									debit = debit + parseFloat(($(this).text()));
							}
							else if (i === 4) {
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
						 url : `/transaction/journal_voucher/edit/${edit_id}`,
						 data:{
							 'tran_id':tran_id,
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


			$(".edit-item-jv").click(function(){
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
							 			 '<td>'+ count +'</td>' +
										 '<td>'+ data.account_id +'</td>' +
										 '<td>'+ data.account_title +'</td>' +
										 '<td><input type="text" class="form-control" required value="0.00"></td>' +
										 '<td><input type="text" class="form-control" required value="0.00"></td>' +
							 '<td><a class="add-jv-edit" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-jv-edit" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete-jv-edit" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
								 '</tr>';
							 $("table").append(row);
						 $("table tbody tr").eq(index + 1).find(".add-jv-edit, .edit-jv-edit").toggle();
								 $('[data-toggle="tooltip"]').tooltip();

				 })
			});


			// Add row on add button click
			$(document).on("click", ".add-jv-edit", function(){
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
				$(this).parents("tr").find(".add-jv-edit, .edit-jv-edit").toggle();
				$(".edit-item-jv").removeAttr("disabled");
			}
			});


			// Edit row on edit button click
			$(document).on("click", ".edit-jv-edit", function(){
					$(this).parents("tr").find("td:not(:last-child)").each(function(i){
						if (i === 3 ) {
							$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
						}
						if (i === 4) {
							$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
						}

			});
			$(this).parents("tr").find(".add-jv-edit, .edit-jv-edit").toggle();
			$(".edit-item-jv").attr("disabled", "disabled");
			});

			// Delete row on delete button click
			$(document).on("click", ".delete-jv-edit", function(){
				var row =  $(this).closest('tr');
				var siblings = row.siblings();
				siblings.each(function(index) {
				$(this).children('td').first().text(index + 1);
				});
				$(this).parents("tr").remove();
				$(".edit-item-jv").removeAttr("disabled");
			});


			$(".load-invoices").click(function(){
				var invoice_no = $('#invoice_no').val()
				console.log(invoice_no);
				if($('#box').prop("checked") == true){
						var check = 1;
				}
				else{
						check = 0
				}
				var account_title = $('#account_title').find(":selected").text();

				req =	$.ajax({
					 headers: { "X-CSRFToken": getCookie("csrftoken") },
					 type: 'POST',
					 data:{
						 'check':check,
						 'invoice_no': invoice_no,
						 'account_title': account_title,
					 },
					 dataType: 'json'
				 })
				 .done(function done(data){
					 var balance_amount = 0;
					 var parent_amount = $('#amount').val();
					 console.log(data.pi);
						 var index = $("table tbody tr:last-child").index();
						 for (var i = 0; i < data.pi.length; i++) {
							 console.log(data.pi[i][3]);
							 b_amount = parseFloat(data.pi[i][3]) - parseFloat(data.pi[i][4])
							 if (parent_amount > 0) {
								 is_abs = parent_amount - parseFloat(b_amount)
									if (parent_amount > parseFloat(b_amount)){
										balance_amount = 0.00 ;
									}
									else{
										parent_amount = parent_amount - parseFloat(b_amount)
										balance_amount = Math.abs(parent_amount)
									}
								 var row = '<tr>' +
										 '<td>6</td>' +
										 '<td>Cash</td>' +
										 '<td>'+data.pi[i][5]+'</td>' +
										 '<td>'+b_amount.toFixed(2)+'</td>' +
										 '<td>0.00</td>' +
										 '<td>'+balance_amount.toFixed(2)+'</td>' +
							 // '<td><a class="add-jv" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-jv" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete-jv" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
								 '</tr>';
							 $("table").append(row);
						 $("table tbody tr").eq(index + 1).find(".add-jv, .edit-jv").toggle();
								 $('[data-toggle="tooltip"]').tooltip();
									parent_amount = parent_amount - parseFloat(b_amount)
							 }
						 }
				 })
			});


				$('#new-jv-form-crv').on('submit',function(e){
						e.preventDefault();
						var account_id = 0
						var table = $('#new-crv-table');
						var data = [];
						var debit = 0;
						var credit = 0;
						var invoice_no = $('#invoice_no').val();
						var doc_date = $('#doc_date').val();
						var cheque_no = $('#cheque_no').val();
						var cheque_date = $('#cheque_date').val();
						var date = $('#date').val();
						var customer = $('#account_title').find(":selected").text();
						var description = $('#description').val();

						table.find('tr').each(function (i, el){
							if(i != 0)
							{
								var $tds = $(this).find('td');
								var row = {
									'account_id' : "",
									'account_title' : "",
									'invoice_no' : "",
									'debit' : "",
									'credit' : "",
									'balance' : "",
								};
								$tds.each(function(i, el){
									if (i === 0) {
											row["account_id"] = ($(this).text());
									}
									if (i === 1) {
											row["account_title"] = ($(this).text());
									}
									else if (i === 2) {
											row["invoice_no"] = ($(this).text());
											debit = debit + parseFloat(($(this).text()));
									}
									else if (i === 3) {
											row["debit"] = ($(this).text());
											debit = debit + parseFloat(($(this).text()));
									}
									else if (i === 4) {
											row["credit"] = ($(this).text());
											credit = credit + parseFloat(($(this).text()));
									}
									else if (i === 5) {
											row["balance"] = ($(this).text());
											credit = credit + parseFloat(($(this).text()));
									}
								});
								data.push(row);
							}
						});

							req =	$.ajax({
								 headers: { "X-CSRFToken": getCookie("csrftoken") },
								 type: 'POST',
								 url : '/transaction/cash_receiving_voucher/new/',
								 data:{
									 'account_id':account_id,
									 'invoice_no': invoice_no,
									 'doc_date': doc_date,
									 'cheque_no': cheque_no,
									 'cheque_date': cheque_no,
									 'description': description,
									 'date':date,
									 'customer':customer,
									 'items': JSON.stringify(data),
								 },
								 dataType: 'json'
							 })
							 .done(function done(data){
								 alert("CR Voucher Submitted");
								 location.reload();
							 })
					});


					$(".load-invoices-brv").click(function(){
						var invoice_no = $('#invoice_no').val()
						console.log(invoice_no);
						if($('#box').prop("checked") == true){
								var check = 1;
						}
						else{
								check = 0
						}
						var account_title = $('#account_title').find(":selected").text();
						var bank_account = $('#bank_account').find(":selected").text();

						req =	$.ajax({
							 headers: { "X-CSRFToken": getCookie("csrftoken") },
							 type: 'POST',
							 data:{
								 'check':check,
								 'invoice_no': invoice_no,
								 'account_title': account_title,
								 'bank_account': bank_account,
							 },
							 dataType: 'json'
						 })
						 .done(function done(data){
							 var balance_amount = 0;
							 var parent_amount = $('#amount').val();
							 console.log(data.pi);
								 var index = $("table tbody tr:last-child").index();
								 for (var i = 0; i < data.pi.length; i++) {
									 console.log(data.pi[i][3]);
									 b_amount = parseFloat(data.pi[i][3]) - parseFloat(data.pi[i][4])
									 if (parent_amount > 0) {
										 is_abs = parent_amount - parseFloat(b_amount)
											if (parent_amount > parseFloat(b_amount)){
												balance_amount = 0.00 ;
											}
											else{
												parent_amount = parent_amount - parseFloat(b_amount)
												balance_amount = Math.abs(parent_amount)
											}
										 var row = '<tr>' +
												 '<td>'+data.account_id+'</td>' +
												 '<td>'+data.bank_account+'</td>' +
												 '<td>'+data.pi[i][5]+'</td>' +
												 '<td>'+b_amount.toFixed(2)+'</td>' +
												 '<td>0.00</td>' +
												 '<td>'+balance_amount.toFixed(2)+'</td>' +
									 // '<td><a class="add-jv" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-jv" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete-jv" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
										 '</tr>';
									 $("table").append(row);
								 $("table tbody tr").eq(index + 1).find(".add-jv, .edit-jv").toggle();
										 $('[data-toggle="tooltip"]').tooltip();
											parent_amount = parent_amount - parseFloat(b_amount)
									 }
								 }
						 })
					});


					$('#new-jv-form-brv').on('submit',function(e){
							e.preventDefault();
							var account_id = 0
							var table = $('#new-brv-table');
							var data = [];
							var debit = 0;
							var credit = 0;
							var invoice_no = $('#invoice_no').val();
							var doc_date = $('#doc_date').val();
							var cheque_no = $('#cheque_no').val();
							var cheque_date = $('#cheque_date').val();
							var date = $('#date').val();
							var customer = $('#account_title').find(":selected").text();
							var bank = $('#bank_account').find(":selected").text();
							var description = $('#description').val();

							table.find('tr').each(function (i, el){
								if(i != 0)
								{
									var $tds = $(this).find('td');
									var row = {
										'account_id' : "",
										'account_title' : "",
										'invoice_no' : "",
										'debit' : "",
										'credit' : "",
										'balance' : "",
									};
									$tds.each(function(i, el){
										if (i === 0) {
												row["account_id"] = ($(this).text());
										}
										if (i === 1) {
												row["account_title"] = ($(this).text());
										}
										else if (i === 2) {
												row["invoice_no"] = ($(this).text());
												debit = debit + parseFloat(($(this).text()));
										}
										else if (i === 3) {
												row["debit"] = ($(this).text());
												debit = debit + parseFloat(($(this).text()));
										}
										else if (i === 4) {
												row["credit"] = ($(this).text());
												credit = credit + parseFloat(($(this).text()));
										}
										else if (i === 5) {
												row["balance"] = ($(this).text());
												credit = credit + parseFloat(($(this).text()));
										}
									});
									data.push(row);
									console.log(data);
								}
							});

								req =	$.ajax({
									 headers: { "X-CSRFToken": getCookie("csrftoken") },
									 type: 'POST',
									 url : '/transaction/bank_receiving_voucher/new/',
									 data:{
										 'account_id':account_id,
										 'invoice_no': invoice_no,
										 'doc_date': doc_date,
										 'cheque_no': cheque_no,
										 'cheque_date': cheque_date,
										 'description': description,
										 'date':date,
										 'customer':customer,
										 'bank' : bank,
										 'items': JSON.stringify(data),
									 },
									 dataType: 'json'
								 })
								 .done(function done(data){
									 alert("BR Voucher Submitted");
									 location.reload();
								 })
						});


						$(".load-invoices-bpv").click(function(){
							var invoice_no = $('#invoice_no').val()
							console.log(invoice_no);
							if($('#box').prop("checked") == true){
									var check = 1;
							}
							else{
									check = 0
							}
							var account_title = $('#account_title').find(":selected").text();
							var bank_account = $('#bank_account').find(":selected").text();

							req =	$.ajax({
								 headers: { "X-CSRFToken": getCookie("csrftoken") },
								 type: 'POST',
								 data:{
									 'check':check,
									 'invoice_no': invoice_no,
									 'account_title': account_title,
									 'bank_account': bank_account,
								 },
								 dataType: 'json'
							 })
							 .done(function done(data){
								 var balance_amount = 0;
								 var parent_amount = $('#amount').val();
								 console.log(data.pi);
									 var index = $("table tbody tr:last-child").index();
									 for (var i = 0; i < data.pi.length; i++) {
										 console.log(data.pi[i][3]);
										 b_amount = parseFloat(data.pi[i][3]) + parseFloat(data.pi[i][4])
										 if (parent_amount > 0) {
											 is_abs = parent_amount - parseFloat(b_amount)
												if (parent_amount > parseFloat(b_amount)){
													balance_amount = 0.00 ;
												}
												else{
													parent_amount = parent_amount - parseFloat(b_amount)
													balance_amount = Math.abs(parent_amount)
												}
											 var row = '<tr>' +
													 '<td>'+data.account_id+'</td>' +
													 '<td>'+data.bank_account+'</td>' +
													 '<td>'+data.pi[i][5]+'</td>' +
													 '<td>0.00</td>' +
													 '<td>'+b_amount.toFixed(2)+'</td>' +
													 '<td>'+balance_amount.toFixed(2)+'</td>' +
											 '</tr>';
										 $("table").append(row);
									 $("table tbody tr").eq(index + 1).find(".add-jv, .edit-jv").toggle();
											 $('[data-toggle="tooltip"]').tooltip();
												parent_amount = parent_amount - parseFloat(b_amount)
										 }
									 }
							 })
						});


					$('#new-jv-form-bpv').on('submit',function(e){
							e.preventDefault();
							var account_id = 0
							var table = $('#new-bpv-table');
							var data = [];
							var debit = 0;
							var credit = 0;
							var invoice_no = $('#invoice_no').val();
							var doc_date = $('#doc_date').val();
							var cheque_no = $('#cheque_no').val();
							var cheque_date = $('#cheque_date').val();
							var date = $('#date').val();
							var customer = $('#account_title').find(":selected").text();
							var bank = $('#bank_account').find(":selected").text();
							var description = $('#description').val();

							table.find('tr').each(function (i, el){
								if(i != 0)
								{
									var $tds = $(this).find('td');
									var row = {
										'account_id' : "",
										'account_title' : "",
										'invoice_no' : "",
										'debit' : "",
										'credit' : "",
										'balance' : "",
									};
									$tds.each(function(i, el){
										if (i === 0) {
												row["account_id"] = ($(this).text());
										}
										if (i === 1) {
												row["account_title"] = ($(this).text());
										}
										else if (i === 2) {
												row["invoice_no"] = ($(this).text());
												debit = debit + parseFloat(($(this).text()));
										}
										else if (i === 3) {
												row["debit"] = ($(this).text());
												debit = debit + parseFloat(($(this).text()));
										}
										else if (i === 4) {
												row["credit"] = ($(this).text());
												credit = credit + parseFloat(($(this).text()));
										}
										else if (i === 5) {
												row["balance"] = ($(this).text());
												credit = credit + parseFloat(($(this).text()));
										}
									});
									data.push(row);
									console.log(data);
								}
							});

								req =	$.ajax({
									 headers: { "X-CSRFToken": getCookie("csrftoken") },
									 type: 'POST',
									 url : '/transaction/bank_payment_voucher/new/',
									 data:{
										 'account_id':account_id,
										 'invoice_no': invoice_no,
										 'doc_date': doc_date,
										 'cheque_no': cheque_no,
										 'cheque_date': cheque_date,
										 'description': description,
										 'date':date,
										 'customer':customer,
										 'bank' : bank,
										 'items': JSON.stringify(data),
									 },
									 dataType: 'json'
								 })
								 .done(function done(data){
									 alert("BP Voucher Submitted");
									 location.reload();
								 })
						});



				$(".load-invoices-cpv").click(function(){
					var invoice_no = $('#invoice_no').val()
					console.log(invoice_no);
					if($('#box').prop("checked") == true){
							var check = 1;
					}
					else{
							check = 0
					}
					var account_title = $('#account_title').find(":selected").text();

					req =	$.ajax({
						 headers: { "X-CSRFToken": getCookie("csrftoken") },
						 type: 'POST',
						 data:{
							 'check':check,
							 'invoice_no': invoice_no,
							 'account_title': account_title,
						 },
						 dataType: 'json'
					 })
					 .done(function done(data){
						 var balance_amount = 0;
						 var parent_amount = $('#amount').val();
						 console.log(data.pi);
							 var index = $("table tbody tr:last-child").index();
							 for (var i = 0; i < data.pi.length; i++) {
								 console.log(data.pi[i][3]);
								 b_amount = parseFloat(data.pi[i][3]) + parseFloat(data.pi[i][4])
								 if (parent_amount > 0) {
									 is_abs = parent_amount - parseFloat(b_amount)
										if (parent_amount > parseFloat(b_amount)){
											balance_amount = 0.00 ;
										}
										else{
											parent_amount = parent_amount - parseFloat(b_amount)
											balance_amount = Math.abs(parent_amount)
										}
									 var row = '<tr>' +
											 '<td>1011</td>' +
											 '<td>Cash</td>' +
											 '<td>'+data.pi[i][5]+'</td>' +
											 '<td>0.00</td>' +
											 '<td>'+b_amount.toFixed(2)+'</td>' +
											 '<td>'+balance_amount.toFixed(2)+'</td>' +
								 // '<td><a class="add-jv" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-jv" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete-jv" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
									 '</tr>';
								 $("table").append(row);
							 $("table tbody tr").eq(index + 1).find(".add-jv, .edit-jv").toggle();
									 $('[data-toggle="tooltip"]').tooltip();
										parent_amount = parent_amount - parseFloat(b_amount)
								 }
							 }
					 })
				});


				$('#new-jv-form-cpv').on('submit',function(e){
						e.preventDefault();
						var account_id = 0
						var table = $('#new-cpv-table');
						var data = [];
						var debit = 0;
						var credit = 0;
						var invoice_no = $('#invoice_no').val();
						var doc_date = $('#doc_date').val();
						var cheque_no = $('#cheque_no').val();
						var cheque_date = $('#cheque_date').val();
						var date = $('#date').val();
						var customer = $('#account_title').find(":selected").text();
						var description = $('#description').val();

						table.find('tr').each(function (i, el){
							if(i != 0)
							{
								var $tds = $(this).find('td');
								var row = {
									'account_id' : "",
									'account_title' : "",
									'invoice_no' : "",
									'debit' : "",
									'credit' : "",
									'balance' : "",
								};
								$tds.each(function(i, el){
									if (i === 0) {
											row["account_id"] = ($(this).text());
									}
									if (i === 1) {
											row["account_title"] = ($(this).text());
									}
									else if (i === 2) {
											row["invoice_no"] = ($(this).text());
											debit = debit + parseFloat(($(this).text()));
									}
									else if (i === 3) {
											row["debit"] = ($(this).text());
											debit = debit + parseFloat(($(this).text()));
									}
									else if (i === 4) {
											row["credit"] = ($(this).text());
											credit = credit + parseFloat(($(this).text()));
									}
									else if (i === 5) {
											row["balance"] = ($(this).text());
											credit = credit + parseFloat(($(this).text()));
									}
								});
								data.push(row);
							}
						});

							req =	$.ajax({
								 headers: { "X-CSRFToken": getCookie("csrftoken") },
								 type: 'POST',
								 url : '/transaction/cash_payment_voucher/new/',
								 data:{
									 'account_id':account_id,
									 'invoice_no': invoice_no,
									 'doc_date': doc_date,
									 'cheque_no': cheque_no,
									 'cheque_date': cheque_no,
									 'description': description,
									 'date':date,
									 'customer':customer,
									 'items': JSON.stringify(data),
								 },
								 dataType: 'json'
							 })
							 .done(function done(data){
								 alert("CP Voucher Submitted");
								 location.reload();
							 })
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

		document.getElementById('box').onchange = function() {
    document.getElementById('invoice_no').disabled = !this.checked;
		};
});
