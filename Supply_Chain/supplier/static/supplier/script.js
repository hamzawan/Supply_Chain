$(document).ready(function(){
	var arr = [];
	var count = 1;
	var edit_id;
	var price;
	var quantity;
	var amount;
	var total_amount = 0
	var grand = 0;
	var new_total_amount = 0;
	$(".has_id").click(function(){
			 edit_id = this.id;
		});


	var obj = {
		'item_name' : "Mouse",
		'item_description' : "Black",
		'unit' : "pcs",
		'quantity' : "10",
	};
	$('[data-toggle="tooltip"]').tooltip();
	var actions = $("table td:last-child").html();
	// Append table with add row form on add new button click
    $(".add-new").click(function(){
		$(this).attr("disabled", "disabled");
		var index = $("table tbody tr:last-child").index();
        var row = '<tr>' +
						'<td><input type="text" readonly class="form-control" name="name" value='+count+'></td>' +
            '<td><input type="text" class="form-control" name="name" id="name"></td>' +
            '<td><input type="text" class="form-control" name="department" id="department"></td>' +
            '<td><input type="text" class="form-control" name="phone" id="phone"></td>' +
						'<td><input type="text" class="form-control" name="phone" id="phone"></td>' +
			'<td><a class="add" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
        '</tr>';
    	$("table").append(row);
		$("table tbody tr").eq(index + 1).find(".add, .edit").toggle();
        $('[data-toggle="tooltip"]').tooltip();
    });

	// add data to rfq table from product
		$(".add-new-rfq").click(function(){
			var item_code = $('#item_code').val();
			req =	$.ajax({
				 headers: { "X-CSRFToken": getCookie("csrftoken") },
				 type: 'POST',
				 url : '/supplier/rfq/new/',
				 data:{
					 'item_code': item_code,
				 },
				 dataType: 'json'
			 })
			 .done(function done(data){
				 var type = JSON.parse(data.row);
				 for (var i = 0; i < type.length; i++) {
				 var index = $("table tbody tr:last-child").index();
						 var row = '<tr>' +
								 '<td><input type="text" readonly class="form-control" value='+count+'></td>' +
								 '<td><input type="text" class="form-control" readonly value='+ type[i].fields['product_code'] +'></td>' +
								 '<td><input type="text" class="form-control" readonly value='+ type[i].fields['product_name'] +'></td>' +
								 '<td><input type="text" class="form-control" readonly value='+ type[i].fields['product_desc'] +'></td>' +
								 '<td><input type="text" class="form-control" required ></td>' +
								 '<td><input type="text" class="form-control" required ></td>' +
					 '<td><a class="add" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
						 '</tr>';
						 count++;
					 $("table").append(row);
				 $("table tbody tr").eq(index + 1).find(".add, .edit").toggle();
						 $('[data-toggle="tooltip"]').tooltip();
					 }
			 });
		});


		// edit data to rfq table from product
			$(".edit_rfq").click(function(){
				var item_code = $('#edit_item_code').val();
				req =	$.ajax({
					 headers: { "X-CSRFToken": getCookie("csrftoken") },
					 type: 'POST',
					 url : `/supplier/rfq/edit/${edit_id}`,
					 data:{
						 'item_code': item_code,
					 },
					 dataType: 'json'
				 })
				 .done(function done(data){

					 console.log(data.row);
					 if (data.row) {
						 var type = JSON.parse(data.row);
						 for (var i = 0; i < type.length; i++) {
						 var index = $("table tbody tr:last-child").index();
								 var row = '<tr>' +
										 '<td><input type="text" readonly class="form-control" value='+count+'></td>' +
										 '<td><input type="text" class="form-control" readonly value='+ type[i].fields['product_code'] +'></td>' +
										 '<td><input type="text" class="form-control" readonly value='+ type[i].fields['product_name'] +'></td>' +
										 '<td><input type="text" class="form-control" readonly value='+ type[i].fields['product_desc'] +'></td>' +
										 '<td><input type="text" class="form-control" required ></td>' +
										 '<td><input type="text" class="form-control" required ></td>' +
							 '<td><a class="add" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
								 '</tr>';
								 count++;
							 $("table").append(row);
						 $("table tbody tr").eq(index + 1).find(".add, .edit").toggle();
								 $('[data-toggle="tooltip"]').tooltip();
							 }
					 }
					 else{
						 alert(data.message)
					 }
				 });
			});



		$(".add-new-item").click(function(){
		$(this).attr("disabled", "disabled");
		var index = $("table tbody tr:last-child").index();
				var row = '<tr>' +
						'<td><input type="text" readonly class="form-control" name="name" value='+count+'></td>' +
						'<td><input type="text" class="form-control" name="name" id="name"></td>' +
						'<td><input type="text" class="form-control" name="department" id="department"></td>' +
						'<td><input type="text" class="form-control" name="phone" id="phone"></td>' +
						'<td><input type="text" class="form-control" name="phone" id="phone"></td>' +
						'<td><input type="text" class="form-control" name="phone" id="phone"></td>' +
						'<td><input type="text" class="form-control" name="phone" id="phone"></td>' +
						'<td><input type="text" class="form-control" name="phone" id="phone"></td>' +
			'<td><a class="add" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
				'</tr>';
			$("table").append(row);
		$("table tbody tr").eq(index + 1).find(".add, .edit").toggle();
				$('[data-toggle="tooltip"]').tooltip();
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

	// Add row on add button click
	$(document).on("click", ".add", function(){
		var empty = false;
		var input = $(this).parents("tr").find('input[type="text"]');
        input.each(function(){
			if(!$(this).val()){
				$(this).addClass("error");
				empty = true;
			} else{
                $(this).removeClass("error");
            }
		});
		$(this).parents("tr").find(".error").first().focus();
		if(!empty){
			input.each(function(){
				$(this).parent("td").html($(this).val());
			});
			$(this).parents("tr").find(".add, .edit").toggle();
			$(".add-new").removeAttr("disabled");
		}
    });

	// Edit row on edit button click
	$(document).on("click", ".edit", function(){
      $(this).parents("tr").find("td:not(:last-child)").each(function(i){
					if (i === 3) {

						$(this).html('<input type="text" id="quantity" class="form-control" value="' + $(this).text() + '">');
					}

					accepted_quantity = $(this).parent("tr").find("#accepted_quantity").text();
					price = $(this).parent("tr").find("#price").text();

					if (i === 6) {
						amount =  $(this).parent("tr").find("#total_amount");
					}
					if (i === 7) {
						 $(this).html('<input type="text" id="sales_tax" class="form-control" value="' + $(this).text() + '">');
					}
					if (i === 8) {
						 sales_tax_amount =  $(this).parent("tr").find("#sales_tax_amount");
					}
					if (i === 9) {
						 grand_total =  $(this).parent("tr").find("#grand_total");
					}

					$('#sales_tax').on('keyup',function(){
						var i = this.value;
						var tax_amount = i *  amount.text()
						tax_amount = tax_amount / 100
						sales_tax_amount.text(tax_amount.toFixed(2));
						grand = total_amount + tax_amount
						grand_total.text((grand.toFixed(2) ));
					 $('#last_grand_total').val((grand.toFixed(2) ));
					});

					$('#quantity').on('keyup',function(){
						var i = this.value;
						total_amount = i * price;
						amount.text(total_amount.toFixed(2));
						var tax_amount = $('#sales_tax').val() *  amount.text();
						tax_amount = tax_amount / 100;
						amount.text(total_amount.toFixed(2));
						sales_tax_amount.text(tax_amount.toFixed(2));
						grand = total_amount + tax_amount
						grand_total.text((grand.toFixed(2) ));
					 $('#last_grand_total').val((grand.toFixed(2) ));
					});

		});
		$(this).parents("tr").find(".add, .edit").toggle();
		$(".add-new").attr("disabled", "disabled");
    });


		$('#cartage_amount').on('keyup',function(e){
			var i = this.value;
			if (i === "" || isNaN(i)) {
				var a =  parseFloat($('#hidden').val())
				$('#last_grand_total').val(a.toFixed(2));
			}
			else {
				var v =  parseFloat($('#hidden').val()) + parseFloat(i)
				$('#last_grand_total').val(v.toFixed(2));
			}
		});

		$('#additional_tax').on('keyup',function(){
			var i = this.value;
			if (!isNaN($('#cartage_amount').val()) && i !== "") {
				var v = parseFloat($('#cartage_amount').val()) + parseFloat($('#hidden').val()) + parseFloat(i);
				$('#last_grand_total').val(v.toFixed(2));
			}
		})


		$('#withholding_tax').on('keyup',function(){
			var i = this.value;
			var cartage_amount = parseFloat($('#cartage_amount').val());
			var additional_tax = parseFloat($('#additional_tax').val());
			var grand_total = parseFloat($('#hidden').val());
			var a =  cartage_amount + additional_tax + grand_total;
			var withholding_tax =  a.toFixed(2) * i;
			withholding_tax = withholding_tax / 100;
			var amount =  withholding_tax + cartage_amount + additional_tax +  grand_total
			$('#last_grand_total').val(amount.toFixed(2));
		})

	// Delete row on delete button click
	$(document).on("click", ".delete", function(i){
				count--;
				var row =  $(this).closest('tr');
				delete_row = $(this).closest('tr').find('#total_amount').text()
				new_total_amount = new_total_amount - delete_row;
				$('#last_grand_total').val(new_total_amount.toFixed(2));
				var siblings = row.siblings();
				siblings.each(function(index) {
				$(this).children('td').first().text(index + 1);
			})
        $(this).parents("tr").remove();
		$(".add-new").removeAttr("disabled");
    });

	$('#myForm').on('submit',function(e){
		e.preventDefault();
		var table = $('#mytable');
		var data = [];
		var rfq_no = $('#rfq_no').val();
		var attn = $('#attn').val();
		var follow_up = $('#follow_up').val();

		table.find('tr').each(function (i, el){
			if(i != 0)
			{
				var $tds = $(this).find('td');
				var row = {
					'item_code' : "",
					'item_name' : "",
					'item_description' : "",
					'unit' : "",
					'quantity' : "",
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
							row["unit"] = ($(this).text());
					}
					else if (i === 5) {
							row["quantity"] = ($(this).text());
					}
				});
				data.push(row);
			}
		});

			 req =	$.ajax({
					headers: { "X-CSRFToken": getCookie("csrftoken") },
					type: 'POST',
					url : '/supplier/rfq/new/',
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
					location.href = 'http://localhost:8000/supplier/rfq/new/'
				})
	});


	// Append table with add row in quotation supplier
		$(".add-new-quotation-supplier").click(function(){
			var rfq_no = $('#get_rfq_no').val();
			req =	$.ajax({
				 headers: { "X-CSRFToken": getCookie("csrftoken") },
				 type: 'POST',
				 url : '/supplier/quotation/new',
				 data:{
					 'rfq_no': rfq_no,
				 },
				 dataType: 'json'
			 })
			 .done(function done(data){
				 if (data.row) {
					 var type = JSON.parse(data.row);
					 for (var i = 0; i < type.length; i++) {
					 var index = $("table tbody tr:last-child").index();
							 var row = '<tr>' +
									 '<td><input type="text" readonly class="form-control" value='+count+'></td>' +
									 '<td><input type="text" class="form-control" readonly required value='+ type[i].fields['item_code'] +'></td>' +
									 '<td><input type="text" class="form-control" readonly required value='+ type[i].fields['item_name'] +'></td>' +
									 '<td><input type="text" class="form-control" readonly required value='+ type[i].fields['item_description'] +'></td>' +
									 '<td><input type="text" class="form-control" required value='+ type[i].fields['quantity'] +'></td>' +
									 '<td><input type="text" class="form-control" required value='+ type[i].fields['unit'] +'></td>' +
									 '<td><input type="text" class="form-control" required id="phone"></td>' +
									 '<td><input type="text" class="form-control" required id="phone"></td>' +
						 '<td><a class="add" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
							 '</tr>';
						 $("table").append(row);
					 $("table tbody tr").eq(index + 1).find(".add, .edit").toggle();
							 $('[data-toggle="tooltip"]').tooltip();
						 }
						 $('#get_rfq_no').val("");
				 }
				 else{
					 alert(data.message)
				 }
			 })
		});

		//inserting data into supplier quotation using ajax request
		$('#new-quotation-supplier-form').on('submit',function(e){
			e.preventDefault();
			var table = $('#new-quotation-supplier-table');
			var data = [];

			var supplier = $('#quotation_supplier').val();
			var attn = $('#quotation_supplier_attn').val();
			var prcbasis = $('#quotation_supplier_prcbasis').val();
			var leadtime = $('#quotation_supplier_leadtime').val();
			var validity = $('#quotation_supplier_validity').val();
			var payment = $('#quotation_supplier_payment').val();
			var remarks = $('#quotation_supplier_remarks').val();
			var currency = $('#quotation_supplier_currency').val();
			var exchange_rate = $('#quotation_supplier_exchange_rate').val();
			var follow_up = $('#quotation_supplier_follow_up').val();

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
						'unit_price': "",
						'remarks':""
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
								row["unit_price"] = ($(this).text());
						}
						else if (i === 7) {
								row["remarks"] = ($(this).text());
						}
					});
					data.push(row);
				}
			});

				 req =	$.ajax({
						headers: { "X-CSRFToken": getCookie("csrftoken") },
						type: 'POST',
						url : '/supplier/quotation/new',
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
						location.href = 'http://localhost:8000/supplier/quotation/new'
					})
		});

		// Append table with add row in purchase order supplier
			$(".add-new-po-supplier").click(function(){
				var quotation_no = $('#quotation_no').val();
				req =	$.ajax({
					 headers: { "X-CSRFToken": getCookie("csrftoken") },
					 type: 'POST',
					 url : '/supplier/purchase_order/new',
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
									 '<td><input type="text" class="form-control" required value='+ type[i].fields['item_code'] +'></td>' +
									 '<td><input type="text" class="form-control" required value='+ type[i].fields['item_name'] +'></td>' +
									 '<td><input type="text" class="form-control" required value='+ type[i].fields['item_description'] +'></td>' +
									 '<td><input type="text" class="form-control" required value='+ type[i].fields['quantity'] +'></td>' +
									 '<td><input type="text" class="form-control" required value='+ type[i].fields['unit'] +'></td>' +
									 '<td><input type="text" class="form-control" required value='+ type[i].fields['unit_price'] +'></td>' +
									 '<td><input type="text" class="form-control" required value='+ type[i].fields['remarks'] +'></td>' +
						 '<td><a class="add" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
							 '</tr>';
							 count++;
						 $("table").append(row);
					 $("table tbody tr").eq(index + 1).find(".add, .edit").toggle();
							 $('[data-toggle="tooltip"]').tooltip();
						 }
				 });
			});

			//inserting data into supplier quotation using ajax request
			$('#new-po-supplier-form').on('submit',function(e){
				e.preventDefault();
				var table = $('#new-po-supplier-table');
				var data = [];

				var supplier = $('#po_supplier').val();
				var attn = $('#po_supplier_attn').val();
				var prcbasis = $('#po_supplier_prcbasis').val();
				var leadtime = $('#po_supplier_leadtime').val();
				var validity = $('#po_supplier_validity').val();
				var payment = $('#po_supplier_payment').val();
				var remarks = $('#po_supplier_remarks').val();
				var currency = $('#po_supplier_currency').val();
				var exchange_rate = $('#po_supplier_exchange_rate').val();
				var follow_up = $('#po_supplier_follow_up').val();

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
							'unit_price': "",
							'remarks':"",
							'quotation_no': ""
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
									row["unit_price"] = ($(this).text());
							}
							else if (i === 7) {
									row["remarks"] = ($(this).text());
							}
						});
						console.log(row);
						data.push(row);
					}
				});
					 req =	$.ajax({
							headers: { "X-CSRFToken": getCookie("csrftoken") },
							type: 'POST',
							url : '/supplier/purchase_order/new',
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
							location.href = 'http://localhost:8000/supplier/purchase_order/new'
						})
			});

			// Append table with add row in delivery challan supplier
				$(".add-new-dc-supplier").click(function(){
					var po_no = $('#po_no').val();
					req =	$.ajax({
						 headers: { "X-CSRFToken": getCookie("csrftoken") },
						 type: 'POST',
						 url : '/supplier/delivery_challan/new',
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
										 '<td><input type="text" class="form-control" readonly required value='+ type[i].fields['item_code'] +'></td>' +
										 '<td><input type="text" class="form-control" readonly required value='+ type[i].fields['item_name'] +'></td>' +
										 '<td><input type="text" class="form-control" readonly required value='+ type[i].fields['item_description'] +'></td>' +
										 '<td><input type="text" class="form-control" required value='+ type[i].fields['quantity'] +'></td>' +
										 '<td><input type="text" class="form-control" readonly required value='+ type[i].fields['unit'] +'></td>' +
										 '<td><input type="text" class="form-control" readonly value='+ type[i].fields['unit_price'] +'></td>' +
										 '<td><input type="text" class="form-control" readonly value='+ data.po_no +'></td>' +
										 '<td><input type="text" class="form-control" readonly value='+ type[i].fields['remarks'] +'></td>' +
							 '<td><a class="add" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
								 '</tr>';
								 count++;
							 $("table").append(row);
						 $("table tbody tr").eq(index + 1).find(".add, .edit").toggle();
								 $('[data-toggle="tooltip"]').tooltip();
							 }
					 });
				});

			//inserting data into supplier dc using ajax request
			$('#new-dc-supplier-form').on('submit',function(e){
				e.preventDefault();
				var table = $('#new-dc-supplier-table');
				var data = [];
				var supplier = $('#dc_supplier').val();
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
							'unit_price': "",
							'remarks':"",
							'po_no' : ""
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
									row["unit_price"] = ($(this).text());
							}
							else if (i === 7) {
									row["po_no"] = ($(this).text());
							}
							else if (i === 8) {
									row["remarks"] = ($(this).text());
							}
						});
						data.push(row);
					}
				});
					 req =	$.ajax({
							headers: { "X-CSRFToken": getCookie("csrftoken") },
							type: 'POST',
							url : '/supplier/delivery_challan/new',
							data:{
								'items': JSON.stringify(data),
							},
							dataType: 'json'
						})
						.done(function done(){
							alert("Delivery Challan Submitted");
							location.href = 'http://localhost:8000/supplier/delivery_challan/new'
						})
			});


			//updating data into supplier rfq using ajax request
			$('#edit-rfq-supplier-form').on('submit',function(e){
				e.preventDefault();
				var table = $('#edit-rfq-supplier-table');
				var edit_rfq_supplier = $("#edit_rfq_supplier").val()
				// var edit_rfq_supplier_name = $("#edit_rfq_supplier_name").val()
				var edit_rfq_attn = $("#edit_rfq_attn").val()
				var edit_rfq_follow_up = $("#edit_rfq_follow_up").val()
				var data = [];
				var rfq_no = $('#edit_rfq_supplier').val();
				table.find('tr').each(function (i, el){
					if(i != 0)
					{
						var $tds = $(this).find('td');
						var row = {
							'item_code' : "",
							'item_name' : "",
							'item_description' : "",
							'unit' : "",
							'quantity' : "",
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
									row["unit"] = ($(this).text());
							}
							else if (i === 5) {
									row["quantity"] = ($(this).text());
							}
						});
						data.push(row);
					}
				});
					 req =	$.ajax({
							headers: { "X-CSRFToken": getCookie("csrftoken") },
							type: 'POST',
							url : `/supplier/rfq/edit/${edit_id}`,
							data:{
								// 'edit_rfq_supplier':edit_rfq_supplier,
								'edit_rfq_attn':edit_rfq_attn,
								'edit_rfq_follow_up':edit_rfq_follow_up,
								'items': JSON.stringify(data),
							},
							dataType: 'json'
						})
						.done(function done(){
							alert("Updated");
							location.href = `http://localhost:8000/supplier/rfq/edit/${edit_id}`
						})
			});


			//updating data into supplier mrn using ajax request
			$('#edit-mrn-supplier-form').on('submit',function(e){
				console.log(edit_id);
				e.preventDefault();
				var table = $('#edit-mrn-supplier-table');
				var edit_rfq_supplier = $("#edit_rfq_supplier").val()
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
							'accpeted_quantity' : "",
							'unit' : "",
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
									row["accepted_quantity"] = ($(this).text());
							}
							else if (i === 6) {
									row["unit"] = ($(this).text());
							}
						});
						data.push(row);
					}
				});
					 req =	$.ajax({
							headers: { "X-CSRFToken": getCookie("csrftoken") },
							type: 'POST',
							url : `/supplier/mrn/edit/${edit_id}`,
							data:{
								'items': JSON.stringify(data),
							},
							dataType: 'json'
						})
						.done(function done(){
							alert("Updated");
							location.href = `http://localhost:8000/supplier/mrn/edit/${edit_id}`
						})
			});

// ==================================================================================================

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


// ========================================================================================================================================================================================================================================================================================================================
				// Purchase

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
						 for (var i = 0; i < type.length; i++) {
						 var index = $("table tbody tr:last-child").index();
						 total_amount = (type[i].fields['unit_price'] * type[i].fields['quantity']);
								 var row = '<tr>' +
										 '<td>'+count+'</td>' +
										 '<td>'+ type[i].fields['item_code'] +'</td>' +
										 '<td>'+ type[i].fields['item_name'] +'</td>' +
										 '<td id="accepted_quantity" >'+ type[i].fields['accepted_quantity'] +'</td>' +
										 '<td>'+ type[i].fields['unit'] +'</td>' +
										 '<td id="price" >'+ type[i].fields['unit_price'] +'</td>' +
										 '<td id="total_amount" >'+total_amount.toFixed(2)+'</td>' +
 										 '<td>0.00</td>' +
										 '<td id="sales_tax_amount">0.00</td>' +
										 '<td id="grand_total"><b>'+total_amount.toFixed(2)+'</b></td>' +
							 '<td><a class="add" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit" title="Edit" data-toggle="tooltip" id="edit_purchase"><i class="material-icons">&#xE254;</i></a><a class="delete" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
								 '</tr>';
								 count++;
							 $("table").append(row);
						 $("table tbody tr").eq(index + 1).find(".add, .edit").toggle();
								 $('[data-toggle="tooltip"]').tooltip();
							 }
							 new_total_amount =  new_total_amount + total_amount
							 $('#hidden').val(new_total_amount)
							 console.log(new_total_amount);
 							 $('#last_grand_total').val(new_total_amount.toFixed(2));

					 });
				});
});
