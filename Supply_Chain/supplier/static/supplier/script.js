$(document).ready(function(){
	var arr = [];
	var count = 1;
	var edit_id;
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
		count++;
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
		count--;
      $(this).parents("tr").find("td:not(:last-child)").each(function(){
			$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
		});
		$(this).parents("tr").find(".add, .edit").toggle();
		$(".add-new").attr("disabled", "disabled");
    });
	// Delete row on delete button click
	$(document).on("click", ".delete", function(){
				if (count === 1) {
					count = 1
				}
				else{
					count--;
				}
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
					'item_name' : "Mouse",
					'item_description' : "Black",
					'unit' : "pcs",
					'quantity' : "10",
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
							'item_name' : "",
							'item_description' : "",
							'quantity' : "",
							'unit' : "",
							'unit_price': "",
							'remarks':"",
							'po_no': ""
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
									row["po_no"] = ($(this).text());
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
				var data = [];
				var rfq_no = $('#edit_rfq_supplier').val();
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
							url : `/supplier/rfq/edit/${edit_id}`,
							data:{
								'items': JSON.stringify(data),
							},
							dataType: 'json'
						})
						.done(function done(){
							alert("Updated");
							location.href = `http://localhost:8000/supplier/rfq/edit/${edit_id}`
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

				//inserting data into supplier dc using ajax request
				$('#new-dc-customer-form').on('submit',function(e){
					e.preventDefault();
					var table = $('#new-dc-customer-table');
					var data = [];
					var customer = $('#dc_customer').val();
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
								'po_no': ""
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
										row["po_no"] = ($(this).text());
								}
							});
							data.push(row);
						}
					});
						 req =	$.ajax({
								headers: { "X-CSRFToken": getCookie("csrftoken") },
								type: 'POST',
								url : '/customer/delivery_challan/new',
								data:{
									'items': JSON.stringify(data),
								},
								dataType: 'json'
							})
							.done(function done(){
								alert("Delivery Challan Submitted");
								location.href = 'http://localhost:8000/customer/delivery_challan/new'
							})
				});


});
