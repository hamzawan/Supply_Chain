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
										 '<td>'+count+'</td>' +
										 '<td>'+ type[0].fields['product_code'] +'</td>' +
										 '<td>'+ type[0].fields['product_name'] +'</td>' +
										 '<td id="desc" >'+ type[0].fields['product_desc'] +'</td>' +
										 '<td id="quantity" ><input type="text" class="form-control" value=""></td>' +
										 '<td><input type="text" class="form-control" value=""></td>' +
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
								$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
							}
							if (i === 4) {
								$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
							}
							if (i === 5) {
								 $(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
							}
							if (i === 7) {
								 $(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
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
					var supplier = $('#supplier_name_purchase').val();
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
								alert("Purchase Created");
								location.href = 'http://localhost:8000/transaction/purchase/new/'
							})
				});


// =============================================================================

				// add data to rfq table from product
					$(".add-item-sale").click(function(){
						var item_code_sale = $('#item_code_sale').val();
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
							 var type = JSON.parse(data.row);
							 var index = $("table tbody tr:last-child").index();
							 total_amount = (type[0].fields['unit_price'] * type[0].fields['quantity']);
									 var row = '<tr>' +
											 '<td>'+count+'</td>' +
											 '<td>'+ type[0].fields['product_code'] +'</td>' +
											 '<td>'+ type[0].fields['product_name'] +'</td>' +
											 '<td id="desc" >'+ type[0].fields['product_desc'] +'</td>' +
											 '<td id="quantity" ><input type="text" class="form-control" value=""></td>' +
											 '<td><input type="text" class="form-control" value=""></td>' +
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
						$(".add-item-sale").removeAttr("disabled");
					}

					var get_price = $($(this).parents("tr").find("#price")).filter(function() {
									price = $(this).text();
									return price
							}).closest("tr");

					var get_quantity = $($(this).parents("tr").find("#quantity")).filter(function() {
									quantity = $(this).text();
									return quantity
							}).closest("tr");

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
									$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
								}
								if (i === 4) {
									$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
								}
								if (i === 5) {
									 $(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
								}
								if (i === 7) {
									 $(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
								}

					});
					$(this).parents("tr").find(".add-transaction, .edit-transaction").toggle();
					$(".add-item-sale").attr("disabled", "disabled");
					});

					// Delete row on delete button click
					$(document).on("click", ".delete-transaction", function(){
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
				var table = $('#new-purchase-table');
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
							url : '/transaction/sale/new/',
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
							location.href = 'http://localhost:8000/transaction/sale/new/'
						})
			});

// ==================================================================================================================================
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
											location.href = `http://localhost:8000/transaction/purchase/return/${edit_id}`
										})
							});

//=======================================================================================

// ==================================================================================================================================
							// EDIT PURCHASE RETURN

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


});
