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
							 // new_total_amount =  new_total_amount + total_amount
							 // $('#hidden').val(new_total_amount)
							 // console.log(new_total_amount);
 							 // $('#last_grand_total').val(new_total_amount.toFixed(2));

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

});
