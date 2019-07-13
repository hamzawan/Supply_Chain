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


	var obj = {
		'item_name' : "Mouse",
		'item_description' : "Black",
		'unit' : "pcs",
		'quantity' : "10",
	};

// ====================================================================================== //
			//NEW RFQ CUSTOMER
			$('[data-toggle="tooltip"]').tooltip();
				$(".add-new-rfq-customer").click(function(){
					var item_code = $('#item_code').val();
					req =	$.ajax({
						 headers: { "X-CSRFToken": getCookie("csrftoken") },
						 type: 'POST',
						 url : '/customer/rfq/new/',
						 data:{
							 'item_code': item_code,
						 },
						 dataType: 'json'
					 })
					 .done(function done(data){
						 var type = JSON.parse(data.row);
							 // Append table with add row form on add new button click
				 			$(this).attr("disabled", "disabled");
				 			var index = $("table tbody tr:last-child").index();
				 					var row = '<tr>' +
				 							'<td>'+count+'</td>' +
											'<td style="display:none;">'+type[0]['pk']+'</td>' +
				 							'<td>'+type[0].fields['product_code']+'</td>' +
				 							'<td>'+type[0].fields['product_name']+'</td>' +
				 							'<td><pre>'+type[0].fields['product_desc']+'</pre></td>' +
				 							'<td>'+type[0].fields['unit']+'</td>' +
				 							'<td><input type="text" class="form-control" value=""></td>' +
				 							'<td><a class="add-rfq-customer" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-rfq-customer" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete-rfq-customer" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
				 					'</tr>';
									count++;
				 				$("table").append(row);
				 			$("table tbody tr").eq(index + 1).find(".add-rfq-customer, .edit-rfq-customer").toggle();
				 					$('[data-toggle="tooltip"]').tooltip();

					 });
				});

			// Add row on add button click
			$(document).on("click", ".add-rfq-customer", function(){
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
				$(this).parents("tr").find(".add-rfq-customer, .edit-rfq-customer").toggle();
				$(".add-new-rfq-customer").removeAttr("disabled");
			}
			});

			// Edit row on edit button click
			$(document).on("click", ".edit-rfq-customer", function(){
					$(this).parents("tr").find("td:not(:last-child)").each(function(i){
						if (i === 4 ) {
							$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
						}
						if (i === 5) {
							$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
						}
			});
			$(this).parents("tr").find(".add-rfq-customer, .edit-rfq-customer").toggle();
			$(".add-new-rfq-customer").attr("disabled", "disabled");
			});

			// Delete row on delete button click
			$(document).on("click", ".delete-rfq-customer", function(){
				var row =  $(this).closest('tr');
				var siblings = row.siblings();
				siblings.each(function(index) {
				$(this).children('td').first().text(index + 1);
				});
				$(this).parents("tr").remove();
				$(".add-new-rfq-customer").removeAttr("disabled");
			});

      	//NEW RFQ CUSTOMER END

			$('#new-rfq-customer-submit').on('submit',function(e){
				e.preventDefault();
				var table = $('#rfq-customer-table');
				var data = [];
				var customer = $('#customer_rfq').val();
				var rfq_no = $('#rfq_no').val();
				var attn = $('#attn').val();
				var footer_remarks = $('#footer_remarks').val();
				var follow_up = $('#follow_up').val();

				table.find('tr').each(function (i, el){
					if(i != 0)
					{
						var $tds = $(this).find('td');
						var row = {
							'id' : "",
							'quantity' : "",
						};
						$tds.each(function(i, el){
							if (i === 1) {
									row["id"] = ($(this).text());
							}
							else if (i === 6) {
									row["quantity"] = ($(this).text());
							}
						});
						data.push(row);
					}
				});

					 req =	$.ajax({
							headers: { "X-CSRFToken": getCookie("csrftoken") },
							type: 'POST',
							url : '/customer/rfq/new/',
							data:{
								'customer': customer,
								'rfq_no': rfq_no,
								'attn': attn,
								'footer_remarks': footer_remarks,
								'follow_up': follow_up,
								'items': JSON.stringify(data),
							},
							dataType: 'json'
						})
						.done(function done(){
							alert("RFQ Submitted");
							location.reload();
						})
			});


			// END SUBMIT RFQ CUSTOMER

			//EDIT RFQ CUSTOMER

				// edit data to rfq table from product
					$(".edit-rfq-customer").click(function(){
						var item_code = $('#edit_item_code').val();
						req =	$.ajax({
							 headers: { "X-CSRFToken": getCookie("csrftoken") },
							 type: 'POST',
							 url : `/customer/rfq/edit/${edit_id}`,
							 data:{
								 'item_code': item_code,
							 },
							 dataType: 'json'
						 })
						 .done(function done(data){
							 if (data.row) {
								 var type = JSON.parse(data.row);
								 for (var i = 0; i < type.length; i++) {
								 var index = $("table tbody tr:last-child").index();
										 var row = '<tr>' +
												 '<td>'+count+'</td>' +
												 '<td style="display:none;">'+ type[i]['pk'] +'</td>' +
												 '<td>'+type[i].fields['product_code']+'</td>' +
												 '<td>'+type[i].fields['product_name']+'</td>' +
												 '<td><pre>'+type[i].fields['product_desc']+'</pre></td>' +
												 '<td>'+type[i].fields['unit'] +'</td>'+
												 '<td><input type="text" class="form-control" required ></td>' +
									 '<td><a class="add-rfq-edit-customer" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-rfq-edit-customer" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete-rfq-edit-customer" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
										 '</tr>';
										 count++;
									 $("table").append(row);
								 $("table tbody tr").eq(index + 1).find(".add-rfq-edit-customer, .edit-rfq-edit-customer").toggle();
										 $('[data-toggle="tooltip"]').tooltip();
									 }
							 }
							 else{
								 alert(data.message)
							 }
						 });
					});

					// Add row on add button click
					$(document).on("click", ".add-rfq-edit-customer", function(){
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
						$(this).parents("tr").find(".add-rfq-edit-customer, .edit-rfq-edit-customer").toggle();
						$(".edit-rfq-customer").removeAttr("disabled");
					}
					});


					// Edit row on edit button click
					$(document).on("click", ".edit-rfq-edit-customer", function(){
							$(this).parents("tr").find("td:not(:last-child)").each(function(i){
								if (i === 6) {
									$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
								}
					});
					$(this).parents("tr").find(".add-rfq-edit-customer, .edit-rfq-edit-customer").toggle();
					$(".edit-rfq-customer").attr("disabled", "disabled");
					});

					// Delete row on delete button click
					$(document).on("click", ".delete-rfq-edit-customer", function(){
						var row =  $(this).closest('tr');
						var siblings = row.siblings();
						siblings.each(function(index) {
						$(this).children('td').first().text(index + 1);
						});
						$(this).parents("tr").remove();
						$(".edit-rfq-customer").removeAttr("disabled");
					});


				// END EDIT RFQ SUPPLIER

				//UPDATE EDIT RFQ SUPPLIER
					//updating data into supplier rfq using ajax request
					$('#edit-rfq-customer-form').on('submit',function(e){
						e.preventDefault();
						var table = $('#edit-rfq-customer-table');
						var customer = $("#edit_rfq_customer").val()
						var footer_remarks = $('#footer_remarks').val()
						var edit_rfq_attn = $("#edit_rfq_attn").val()
						var edit_rfq_follow_up = $("#edit_rfq_follow_up").val()
						var data = [];
						var rfq_no = $('#edit_rfq_customer').val();
						table.find('tr').each(function (i, el){
							if(i != 0)
							{
								var $tds = $(this).find('td');
								var row = {
									'id' : "",
									'quantity' : "",
								};
								$tds.each(function(i, el){
									if (i === 1) {
											row["id"] = ($(this).text());
											console.log($(this).text());
									}
									else if (i === 6) {
											row["quantity"] = ($(this).text());
											console.log($(this).text());
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
										'footer_remarks': footer_remarks,
										'customer': customer,
										'edit_rfq_attn':edit_rfq_attn,
										'edit_rfq_follow_up':edit_rfq_follow_up,
										'items': JSON.stringify(data),
									},
									dataType: 'json'
								})
								.done(function done(){
									alert("Updated");
									location.reload();
								})
					});

					//END UPDATE EDIT RFQ SUPPLIER
// ======================================================================================

				//QUOTATION CUSTOMER

// // Append table with add row in quotation supplier

			$(".add-new-quotation-customer").click(function(){
				var item_code_quotation = $('#item_code_quotation').val();
				req =	$.ajax({
					 headers: { "X-CSRFToken": getCookie("csrftoken") },
					 type: 'POST',
					 url : '/customer/quotation/new',
					 data:{
						 'item_code_quotation': item_code_quotation,
					 },
					 dataType: 'json'
				 })
				 .done(function done(data){
					 if (data.row) {
						 var type = JSON.parse(data.row);
						 var index = $("table tbody tr:last-child").index();
								 var row = '<tr>' +
										 '<td>'+count+'</td>' +
										 '<td style="display:none;">'+type[0]['pk']+'</td>' +
										 '<td>'+type[0].fields['product_code']+'</td>' +
										 '<td>'+type[0].fields['product_name']+'</td>' +
										 '<td><pre>'+type[0].fields['product_desc']+'</pre></td>' +
										 '<td><input type="text" class="form-control" required ></td>' +
										 '<td>'+type[0].fields['unit']+'</td>' +
										 '<td><input type="text" class="form-control" required ></td>' +
										 '<td><input type="text" class="form-control" required ></td>' +
							 '<td><a class="add-quotation-customer" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-quotation-customer" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete-quotation-customer" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
								 '</tr>';
							 $("table").append(row);
						 $("table tbody tr").eq(index + 1).find(".add-quotation-customer, .edit-quotation-customer").toggle();
								 $('[data-toggle="tooltip"]').tooltip();
							 $('#item_code_quotation').val("");
					 }
					 else{
						 alert(data.message)
					 }
				 })
			});


			// Add row on add button click
			$(document).on("click", ".add-quotation-customer", function(){
			var empty = false;
			var input = $(this).parents("tr").find('input[type="text"]');
					input.each(function(i){
			if (i == 2) {
						$(this).removeClass("error");
			}
			else{
				if(!$(this).val()){
					$(this).addClass("error");
					empty = true;
				}
				else{
						$(this).removeClass("error");
						}
			}
			});
			$(this).parents("tr").find(".error").first().focus();
			if(!empty){
				input.each(function(){
					$(this).parent("td").html($(this).val());
				});
				$(this).parents("tr").find(".add-quotation-customer, .edit-quotation-customer").toggle();
				$(".add-new-quotation-customer").removeAttr("disabled");
			}
			});


			// Edit row on edit button click
			$(document).on("click", ".edit-quotation-customer", function(){
					$(this).parents("tr").find("td:not(:last-child)").each(function(i){
						if (i === 5 ) {
							$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
						}
						if (i === 7 ) {
							$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
						}
						if (i === 8) {
							$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
						}
			});
			$(this).parents("tr").find(".add-quotation-customer, .edit-quotation-customer").toggle();
			$(".add-new-quotation-customer").attr("disabled", "disabled");
			});

			// Delete row on delete button click
			$(document).on("click", ".delete-quotation-customer", function(){
				var row =  $(this).closest('tr');
				var siblings = row.siblings();
				siblings.each(function(index) {
				$(this).children('td').first().text(index + 1);
				});
				$(this).parents("tr").remove();
				$(".add-new-quotation-customer").removeAttr("disabled");
			});


				//SUBMIT QUOTATION SUPPLIER

				//inserting data into supplier quotation using ajax request
				$('#new-quotation-customer-form').on('submit',function(e){
					e.preventDefault();
					var table = $('#new-quotation-customer-table');
					var data = [];

					var customer = $('#customer_quotation').val();
					var attn = $('#quotation_customer_attn').val();
					var prcbasis = $('#quotation_customer_prcbasis').val();
					var yrref = $('#quotation_customer_yrref').val();
					var leadtime = $('#quotation_customer_leadtime').val();
					var validity = $('#quotation_customer_validity').val();
					var payment = $('#quotation_customer_payment').val();
					var remarks = $('#quotation_customer_remarks').val();
					var currency = $('#quotation_customer_currency').val();
					var exchange_rate = $('#quotation_customer_exchange_rate').val();
					var follow_up = $('#quotation_customer_follow_up').val();
					var footer_remarks = $('#footer_remarks').val();

					table.find('tr').each(function (i, el){
						if(i != 0)
						{
							var $tds = $(this).find('td');
							var row = {
								'id' : "",
								'quantity' : "",
								'unit_price': "",
								'remarks':""
							};
							$tds.each(function(i, el){
								if (i === 1) {
										row["id"] = ($(this).text());
								}
								else if (i === 5) {
										row["quantity"] = ($(this).text());
								}
								else if (i === 7) {
										row["unit_price"] = ($(this).text());
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
								url : '/customer/quotation/new',
								data:{
									'customer':customer,
									'attn': attn,
									'prcbasis': prcbasis,
									'leadtime': leadtime,
									'validity': validity,
									'payment': payment,
									'yrref': yrref,
									'remarks': remarks,
									'currency': currency,
									'exchange_rate':exchange_rate,
									'follow_up': follow_up,
									'footer_remarks': footer_remarks,
									'items': JSON.stringify(data),
								},
								dataType: 'json',
							})
							.done(function done(data){
								alert("Quotation Submitted");
								var win = window.open(`/customer/print_quotation_customer/${data.last_id}`, '_blank');
								if (win) {
								    //Browser has allowed it to be opened
								    win.focus();
								} else {
								    //Browser has blocked it
								    alert('Please allow popups for this website');
								}
								location.reload()
								// window.location.href = 'http://localhost:8000/customer/send_email/140/2';
							})
				});

					// EDIT QUOTATION SUPPLIER

					// edit data to rfq table from product
						$(".edit-quotation-customer").click(function(){
							var item_code = $('#edit_item_code').val();
							req =	$.ajax({
								 headers: { "X-CSRFToken": getCookie("csrftoken") },
								 type: 'POST',
								 url : `/customer/quotation/edit/${edit_id}`,
								 data:{
									 'item_code': item_code,
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
													 '<td style="display:none;" >'+type[i]['pk']+'</td>' +
													 '<td>'+type[i].fields['product_code']+'</td>' +
													 '<td>'+type[i].fields['product_name']+'</td>' +
													 '<td><pre>'+type[i].fields['product_desc']+'</pre></td>' +
													 '<td><input type="text" class="form-control" required ></td>' +
													 '<td>'+type[i].fields['unit']+'</td>' +
													 '<td><input type="text" class="form-control" required ></td>' +
													 '<td><input type="text" class="form-control" required ></td>' +
										 '<td><a class="add-quotation-edit-customer" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-quotation-edit-customer" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete-quotation-edit-customer" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
											 '</tr>';
											 count++;
										 $("table").append(row);
									 $("table tbody tr").eq(index + 1).find(".add-quotation-edit-customer, .edit-quotation-edit-customer").toggle();
											 $('[data-toggle="tooltip"]').tooltip();
											 $(".has_id").attr("disabled", "disabled");
										 }
								 }
								 else{
									 alert(data.message)
								 }
							 });
						});

						// Add row on add button click
						$(document).on("click", ".add-quotation-edit-customer", function(){
						var empty = false;
						var input = $(this).parents("tr").find('input[type="text"]');
						input.each(function(i){
				if (i == 2) {
							$(this).removeClass("error");
				}
				else{
					if(!$(this).val()){
						$(this).addClass("error");
						empty = true;
					}
					else{
							$(this).removeClass("error");
							}
				}
				});
						$(this).parents("tr").find(".error").first().focus();
						if(!empty){
							input.each(function(){
								$(this).parent("td").html($(this).val());
							});
							$(this).parents("tr").find(".add-quotation-edit-customer, .edit-quotation-edit-customer").toggle();
							$(".edit-quotation-customer").removeAttr("disabled");
							$(".has_id").removeAttr("disabled");
						}
						});


						// Edit row on edit button click
						$(document).on("click", ".edit-quotation-edit-customer", function(){
								$(this).parents("tr").find("td:not(:last-child)").each(function(i){
									if (i === 5) {
										$(this).html('<input type="text" class="form-control form-control-sm" value="' + $(this).text() + '">');
									}
									if (i === 7) {
										$(this).html('<input type="text" class="form-control form-control-sm" value="' + $(this).text() + '">');
									}
									if (i === 8) {
										$(this).html('<input type="text" class="form-control form-control-sm" value="' + $(this).text() + '">');
									}
						});
						$(this).parents("tr").find(".add-quotation-edit-customer, .edit-quotation-edit-customer").toggle();
						$(".edit-quotation-customer").attr("disabled", "disabled");
						$(".has_id").attr("disabled", "disabled");
						});

						// Delete row on delete button click
						$(document).on("click", ".delete-quotation-edit-customer", function(){
							var row =  $(this).closest('tr');
							var siblings = row.siblings();
							siblings.each(function(index) {
							$(this).children('td').first().text(index + 1);
							});
							$(this).parents("tr").remove();
							$(".edit-quotation-customer").removeAttr("disabled");
							$(".has_id").removeAttr("disabled");
						});


					// END EDIT QUOTATION SUPPLIER

					//SUBMIT EDIT QUOTATION SUPPLIER

					//inserting data into supplier quotation using ajax request
					$('#edit-customer-quotation-submit').on('submit',function(e){
						e.preventDefault();
						var table = $('#edit-quotation-customer-table');
						var data = [];
						var customer = $('#quotation_customer_edit').val();
						var attn = $('#edit_quotation_attn').val();
						var prcbasis = $('#edit_quotation_prcbasis').val();
						var yrref = $('#edit_quotation_yrref').val();
						var leadtime = $('#edit_quotation_leadtime').val();
						var validity = $('#edit_quotation_validity').val();
						var payment = $('#edit_quotation_payment').val();
						var remarks = $('#edit_quotation_remarks').val();
						var currency = $('#edit_quotation_currency_rate').val();
						var exchange_rate = $('#edit_quotation_exchange_rate').val();
						var follow_up = $('#edit_quotation_follow_up').val();
						var footer_remarks = $('#footer_remarks').val();

						table.find('tr').each(function (i, el){
							if(i != 0)
							{
								var $tds = $(this).find('td');
								var row = {
									'item_id' : "",
									'quantity' : "",
									'unit_price': "",
									'remarks':""
								};
								$tds.each(function(i, el){
									if (i === 1) {
											row["id"] = ($(this).text());
									}
									else if (i === 5) {
											row["quantity"] = ($(this).text());
									}
									else if (i === 7) {
											row["unit_price"] = ($(this).text());
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
									url : `/customer/quotation/edit/${edit_id}`,
									data:{
										'customer': customer,
										'attn': attn,
										'prcbasis': prcbasis,
										'yrref': yrref,
										'leadtime': leadtime,
										'validity': validity,
										'payment': payment,
										'remarks': remarks,
										'currency': currency,
										'exchange_rate':exchange_rate,
										'follow_up': follow_up,
										'footer_remarks': footer_remarks,
										'items': JSON.stringify(data),
									},
									dataType: 'json'
								})
								.done(function done(){
									alert("Quotation Updated");
									location.reload();
								})
					});

// END EDIT SUBMIT QUOTATION SUPPLIER

//=======================================================================================

				//PURCHASE ORDER SUPPLIER

// // Append table with add row in po supplier

			$(".add-new-po-customer").click(function(){
				var item_code_po = $('#item_code_po').val();
				req =	$.ajax({
					 headers: { "X-CSRFToken": getCookie("csrftoken") },
					 type: 'POST',
					 url : '/customer/purchase_order/new',
					 data:{
						 'item_code_po': item_code_po,
					 },
					 dataType: 'json'
				 })
				 .done(function done(data){
					 if (data.row) {
						 var type = JSON.parse(data.row);
						 var index = $("table tbody tr:last-child").index();
								 var row = '<tr>' +
										 '<td>'+count+'</td>' +
										 '<td style="display:none;">'+type[0]['pk']+'</td>' +
										 '<td>'+type[0].fields['product_code']+'</td>' +
										 '<td>'+type[0].fields['product_name']+'</td>' +
										 '<td><pre>'+ type[0].fields['product_desc'] +'</pre></td>' +
										 '<td><input type="text" class="form-control form-control-sm" required ></td>' +
										 '<td>'+type[0].fields['unit']+'</td>' +
										 '<td><input type="text" class="form-control" required ></td>' +
										 '<td><input type="text" class="form-control" required ></td>' +
							 '<td><a class="add-po-customer" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-po-customer" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete-po-customer" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
								 '</tr>';
							 $("table").append(row);
						 $("table tbody tr").eq(index + 1).find(".add-po-customer, .edit-po-customer").toggle();
								 $('[data-toggle="tooltip"]').tooltip();
							 $('#item_code_po').val("");
							 $(".has_id").attr("disabled", "disabled");
					 }
					 else{
						 alert(data.message)
					 }
				 })
			});


			// Add row on add button click
			$(document).on("click", ".add-po-customer", function(){
			var empty = false;
			var input = $(this).parents("tr").find('input[type="text"]');
			input.each(function(i){
				if (i == 2) {
							$(this).removeClass("error");
				}
				else{
					if(!$(this).val()){
						$(this).addClass("error");
						empty = true;
					}
					else{
							$(this).removeClass("error");
							}
				}
				});
			$(this).parents("tr").find(".error").first().focus();
			if(!empty){
				input.each(function(){
					$(this).parent("td").html($(this).val());
				});
				$(this).parents("tr").find(".add-po-customer, .edit-po-customer").toggle();
				$(".add-new-po-customer").removeAttr("disabled");
				$(".has_id").removeAttr("disabled");
			}
			});


			// Edit row on edit button click
			$(document).on("click", ".edit-po-customer", function(){
					$(this).parents("tr").find("td:not(:last-child)").each(function(i){
						if (i === 5) {
							$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
						}
						if (i === 7 ) {
							$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
						}
						if (i === 8) {
							$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
						}
			});
			$(this).parents("tr").find(".add-po-customer, .edit-po-customer").toggle();
			$(".add-new-po-customer").attr("disabled", "disabled");
			$(".has_id").attr("disabled", "disabled");

			});

			// Delete row on delete button click
			$(document).on("click", ".delete-po-customer", function(){
				var row =  $(this).closest('tr');
				var siblings = row.siblings();
				siblings.each(function(index) {
				$(this).children('td').first().text(index + 1);
				});
				$(this).parents("tr").remove();
				$(".add-new-po-customer").removeAttr("disabled");
				$(".has_id").removeAttr("disabled");
			});


				//SUBMIT PO CUSTOMER

			//inserting data into supplier po using ajax request
			$('#new-po-customer-form').on('submit',function(e){
				e.preventDefault();
				var table = $('#new-po-customer-table');
				var data = [];
				var customer = $('#po_customer').val();
	  		var attn = $('#po_customer_attn').val();
	  		var prcbasis = $('#po_customer_prcbasis').val();
				var po_client = $('#po_client').val();
	  		var leadtime = $('#po_customer_leadtime').val();
	  		var validity = $('#po_customer_validity').val();
	  		var payment = $('#po_customer_payment').val();
	  		var remarks = $('#po_customer_remarks').val();
	  		var currency = $('#po_customer_currency').val();
	  		var exchange_rate = $('#po_customer_exchange_rate').val();
	  		var follow_up = $('#po_customer_follow_up').val();
				var footer_remarks = $('#footer_remarks').val();

				table.find('tr').each(function (i, el){
					if(i != 0)
					{
						var $tds = $(this).find('td');
						var row = {
							'id' : "",
							'quantity' : "",
							'unit_price': "",
							'remarks':""
						};
						$tds.each(function(i, el){
							if (i === 1) {
									row["id"] = ($(this).text());
							}
							else if (i === 5) {
									row["quantity"] = ($(this).text());
							}
							else if (i === 7) {
									row["unit_price"] = ($(this).text());
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
							url : '/customer/purchase_order/new',
							data:{
								'customer':customer,
								'attn': attn,
								'prcbasis': prcbasis,
								'po_client': po_client,
								'leadtime': leadtime,
								'validity': validity,
								'payment': payment,
								'remarks': remarks,
								'currency': currency,
								'exchange_rate':exchange_rate,
								'follow_up': follow_up,
								'footer_remarks': footer_remarks,
								'items': JSON.stringify(data),
							},
							dataType: 'json'
						})
						.done(function done(){
							alert("Purchase Order Submitted");
							location.reload();
						})
			});

				// EDIT PO SUPPLIER

				// edit data to po table from product
					$(".edit-po-customer").click(function(){
						console.log(edit_id);
						var item_code = $('#edit_item_code').val();
						req =	$.ajax({
							 headers: { "X-CSRFToken": getCookie("csrftoken") },
							 type: 'POST',
							 url : `/customer/purchase_order/edit/${edit_id}`,
							 data:{
								 'item_code': item_code,
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
												 '<td style="display:none;" >'+type[i]['pk']+'</td>' +
												 '<td>'+type[i].fields['product_code']+'</td>' +
												 '<td>'+type[i].fields['product_name']+'</td>' +
												 '<td><pre>'+type[i].fields['product_desc']+'</pre></td>' +
												 '<td><input type="text" class="form-control" required ></td>' +
												 '<td>'+type[i].fields['unit']+'</td>' +
												 '<td><input type="text" class="form-control" required ></td>' +
												 '<td><input type="text" class="form-control" required ></td>' +
									 '<td><a class="add-po-edit-customer" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-po-edit-customer" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete-po-edit-customer" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
										 '</tr>';
										 count++;
									 $("table").append(row);
								 $("table tbody tr").eq(index + 1).find(".add-po-edit-customer, .edit-po-edit-customer").toggle();
										 $('[data-toggle="tooltip"]').tooltip();
										 $(".has_id").attr("disabled", "disabled");
									 }
							 }
							 else{
								 alert(data.message)
								 $(".edit-po-customer").removeAttr("disabled");
								 $(".has_id").removeAttr("disabled");
							 }
						 });
					});

					// Add row on add button click
					$(document).on("click", ".add-po-edit-customer", function(){
					var empty = false;
					var input = $(this).parents("tr").find('input[type="text"]');
					input.each(function(i){
						if (i == 2) {
									$(this).removeClass("error");
						}
						else{
							if(!$(this).val()){
								$(this).addClass("error");
								empty = true;
							}
							else{
									$(this).removeClass("error");
									}
						}
						});
					$(this).parents("tr").find(".error").first().focus();
					if(!empty){
						input.each(function(){
							$(this).parent("td").html($(this).val());
						});
						$(this).parents("tr").find(".add-po-edit-customer, .edit-po-edit-customer").toggle();
						$(".edit-po-customer").removeAttr("disabled");
						$(".has_id").removeAttr("disabled");
					}
					});


					// Edit row on edit button click
					$(document).on("click", ".edit-po-edit-customer", function(){
							$(this).parents("tr").find("td:not(:last-child)").each(function(i){
								if (i === 5) {
									$(this).html('<input type="text" class="form-control form-control-sm" value="' + $(this).text() + '">');
								}
								if (i === 7) {
									$(this).html('<input type="text" class="form-control form-control-sm" value="' + $(this).text() + '">');
								}
								if (i === 8) {
									$(this).html('<input type="text" class="form-control form-control-sm" value="' + $(this).text() + '">');
								}
					});
					$(this).parents("tr").find(".add-po-edit-customer, .edit-po-edit-customer").toggle();
					$(".edit-po-customer").attr("disabled", "disabled");
					$(".has_id").attr("disabled", "disabled");
					});

					// Delete row on delete button click
					$(document).on("click", ".delete-po-edit-customer", function(){
						var row =  $(this).closest('tr');
						var siblings = row.siblings();
						siblings.each(function(index) {
						$(this).children('td').first().text(index + 1);
						});
						$(this).parents("tr").remove();
						$(".edit-po-customer").removeAttr("disabled");
						$(".has_id").removeAttr("disabled");
					});



				//SUBMIT EDIT PO SUPPLIER

				//inserting data into supplier quotation using ajax request
				$('#edit-customer-po-form').on('submit',function(e){
					e.preventDefault();
					var table = $('#edit-po-customer-table');
					var data = [];

					var customer = $('#edit_po_customer').val();
					var attn = $('#edit_po_attn').val();
					var prcbasis = $('#edit_po_prcbasis').val();
					var po_client = $('#edit_po_client').val();
					var leadtime = $('#edit_po_leadtime').val();
					var validity = $('#edit_po_validity').val();
					var payment = $('#edit_po_payment').val();
					var remarks = $('#edit_po_remarks').val();
					var currency = $('#edit_po_currency_rate').val();
					var exchange_rate = $('#edit_po_exchange_rate').val();
					var follow_up = $('#edit_po_follow_up').val();
					var footer_remarks = $('#footer_remarks').val();

					table.find('tr').each(function (i, el){
						if(i != 0)
						{
							var $tds = $(this).find('td');
							var row = {
								'id' : "",
								'quantity' : "",
								'unit_price': "",
								'remarks':""
							};
							$tds.each(function(i, el){
								if (i === 1) {
										row["id"] = ($(this).text());
								}
								else if (i === 5) {
										row["quantity"] = ($(this).text());
								}
								else if (i === 7) {
										row["unit_price"] = ($(this).text());
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
								url : `/customer/purchase_order/edit/${edit_id}`,
								data:{
									'customer':customer,
									'attn': attn,
									'prcbasis': prcbasis,
									'po_client': po_client,
									'leadtime': leadtime,
									'validity': validity,
									'payment': payment,
									'remarks': remarks,
									'currency': currency,
									'exchange_rate':exchange_rate,
									'follow_up': follow_up,
									'footer_remarks': footer_remarks,
									'items': JSON.stringify(data),
								},
								dataType: 'json'
							})
							.done(function done(){
								alert("Purchase Order Updated");
								location.reload();
							})
				});

					// END EDIT SUBMIT PO SUPPLIER

	//=======================================================================================

					//DC ORDER CUSTOMER

		// // Append table with add row in dc supplier

					$(".add-new-dc-customer").click(function(){
						var item_code_dc = $('#item_code_dc').val();
						req =	$.ajax({
							 headers: { "X-CSRFToken": getCookie("csrftoken") },
							 type: 'POST',
							 url : '/customer/delivery_challan/new',
							 data:{
								 'item_code_dc': item_code_dc,
							 },
							 dataType: 'json'
						 })
						 .done(function done(data){
							 if (data.row) {
								 var type = JSON.parse(data.row);
								 console.log(type);
								 var index = $("table tbody tr:last-child").index();
										 var row = '<tr>' +
												 '<td>'+count+'</td>' +
												 '<td style="display:none;">'+type[0]['pk']+'</td>' +
												 '<td id="get_item_code">'+type[0].fields['product_code']+'</td>' +
												 '<td>'+type[0].fields['product_name']+'</td>' +
												 '<td><pre>'+type[0].fields['product_desc']+'</pre></td>' +
												 '<td id="quantity"><input type="text" class="form-control form-control-sm" required ></td>' +
												 '<td>'+type[0].fields['unit']+'</td>' +
												 '<td style="display:none;"></td>' +
									 '<td><a class="add-dc-customer" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-dc-customer" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete-dc-customer" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
										 '</tr>';
									 $("table").append(row);
								 $("table tbody tr").eq(index + 1).find(".add-dc-customer, .edit-dc-customer").toggle();
										 $('[data-toggle="tooltip"]').tooltip();
									 $('#item_code_dc').val("");
									 $(".add-new-dc-customer").attr("disabled", "disabled");
				 					 $(".has_id").attr("disabled", "disabled");
							 }
							 else{
								 alert(data.message)
							 }
						 })
					});


					$(".add-new-po-customer-dc").click(function(){
						var item_code_po_dc = $('#item_code_po_dc').val()
						console.log(item_code_po_dc);
						req =	$.ajax({
							 headers: { "X-CSRFToken": getCookie("csrftoken") },
							 type: 'POST',
							 url : '/customer/delivery_challan/new',
							 data:{
								 'item_code_po_dc': item_code_po_dc,
							 },
							 dataType: 'json'
						 })
						 .done(function done(data){
							 if (data.row) {
								 console.log(data.row);
								 var index = $("table tbody tr:last-child").index();
								 for (var i = 0; i < data.row.length; i++) {
									 var row = '<tr>' +
											 '<td>'+count+'</td>' +
											 '<td style="display:none;" >'+data.row[i][0]+'</td>' +
											 '<td id="get_item_code">'+data.row[i][1]+'</td>' +
											 '<td>'+data.row[i][2]+'</td>' +
											 '<td><pre>'+data.row[i][7]+'</pre></td>' +
											 '<td id="quantity"><input type="text" class="form-control form-control-sm" required ></td>' +
											 '<td>'+data.row[i][3]+'</td>' +
											 '<td style="display:none;" >'+data.id+'</td>' +
								 '<td><a class="add-dc-customer-po" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-dc-customer-po" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete-dc-customer-po" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
									 '</tr>';
	 									 $("table").append(row);
										 $("table tbody tr").eq(index + 1).find(".add-dc-customer-po, .edit-dc-customer-po").toggle();
										 $('[data-toggle="tooltip"]').tooltip();
										 $('#item_code_dc').val("");
										 $(".add-new-po-customer-dc").attr("disabled", "disabled");
										 $(".has_id").attr("disabled", "disabled");
								 }
							 }
							 else{
								 alert(data.message)
							 }
						 })
					});

					// Add row on add button click
					$(document).on("click", ".add-dc-customer", function(){
					var empty = false;
					var input = $(this).parents("tr").find('input[type="text"]');
					input.each(function(i){
						if (i == 2) {
									$(this).removeClass("error");
						}
						else{
							if(!$(this).val()){
								$(this).addClass("error");
								empty = true;
							}
							else{
									$(this).removeClass("error");
									}
						}
						});
					$(this).parents("tr").find(".error").first().focus();
					if(!empty){
						input.each(function(){
							$(this).parent("td").html($(this).val());
						});
						$(this).parents("tr").find(".add-dc-customer, .edit-dc-customer").toggle();
						$(".add-new-dc-customer").removeAttr("disabled");
						$(".add-new-po-customer-dc").removeAttr("disabled");
						$(".has_id").removeAttr("disabled");
					}
					var get_quantity = $($(this).parents("tr").find("#quantity")).filter(function() {
									quantity = $(this).text();
									return quantity
							}).closest("tr");
					console.log(quantity);
					var get_item_code = $($(this).parents("tr").find("#get_item_code")).filter(function() {
									item_code = $(this).text();
									return item_code
							}).closest("tr");
				item_code = $('#item_code').val()
				req =	$.ajax({
					 headers: { "X-CSRFToken": getCookie("csrftoken") },
					 type: 'POST',
					 url : '/customer/delivery_challan/new',
					 data:{
						 'quantity':quantity,
						 'item_code':item_code
					 },
					 dataType: 'json'
				 })
				 .done(function done(data){

					 if(data.message === "False"){
						alert("Not enough stock")
					// 	var table = $('#new-dc-customer-table');
					// 	table.find("tr").find("td:not(:last-child)").each(function(i){
					// 			if (i === 5) {
					// 				$(this).html('<input type="text" style="border: 1px solid red;" class="form-control form-control-warning" value="' + $(this).text() + '">');
					// 			}
					// });
					table.find("tr").find(".add-transaction-sale, .edit-transaction-sale").toggle();
					$(".add-item-sale").attr("disabled", "disabled");
					 }
					 else{

					 }
				});

					});


					// Edit row on edit button click
					$(document).on("click", ".edit-dc-customer", function(){
							$(this).parents("tr").find("td:not(:last-child)").each(function(i){

								if (i === 5) {
									$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
								}
					});
					$(this).parents("tr").find(".add-dc-customer, .edit-dc-customer").toggle();
					$(".add-new-dc-customer").attr("disabled", "disabled");
					$(".add-new-po-customer-dc").attr("disabled", "disabled");
					$(".has_id").attr("disabled", "disabled");
					});

					// Delete row on delete button click
					$(document).on("click", ".delete-dc-customer", function(){
						var row =  $(this).closest('tr');
						var siblings = row.siblings();
						siblings.each(function(index) {
						$(this).children('td').first().text(index + 1);
						});
						$(this).parents("tr").remove();
						$(".add-new-dc-customer").removeAttr("disabled");
						$(".add-new-po-customer-dc").removeAttr("disabled");
						$(".has_id").removeAttr("disabled");
					});


					$(document).on("click", ".add-dc-customer-po", function(){
					var empty = false;
					var input = $(this).parents("tr").find('input[type="text"]');
					input.each(function(i){
						if (i == 2) {
									$(this).removeClass("error");
						}
						else{
							if(!$(this).val()){
								$(this).addClass("error");
								empty = true;
							}
							else{
									$(this).removeClass("error");
									}
						}
						});
					$(this).parents("tr").find(".error").first().focus();
					if(!empty){
						input.each(function(){
							$(this).parent("td").html($(this).val());
						});
						$(this).parents("tr").find(".add-dc-customer-po, .edit-dc-customer-po").toggle();
						$(".add-new-dc-customer").removeAttr("disabled");
						$(".add-new-po-customer-dc").removeAttr("disabled");
						$(".has_id").removeAttr("disabled");
					}
					var get_quantity = $($(this).parents("tr").find("#quantity")).filter(function() {
									quantity = $(this).text();
									return quantity
							}).closest("tr");
					console.log(quantity);
					var get_item_code = $($(this).parents("tr").find("#get_item_code")).filter(function() {
									item_code = $(this).text();
									return item_code
							}).closest("tr");

				req =	$.ajax({
					 headers: { "X-CSRFToken": getCookie("csrftoken") },
					 type: 'POST',
					 url : '/customer/delivery_challan/new',
					 data:{
						 'quantity':quantity,
						 'item_code':item_code
					 },
					 dataType: 'json'
				 })
				 .done(function done(data){

					 if(data.message === "False"){
						alert("Not enough stock")
					// 	var table = $('#new-dc-customer-table');
					// 	table.find("tr").find("td:not(:last-child)").each(function(i){
					// 			if (i === 5) {
					// 				$(this).html('<input type="text" style="border: 1px solid red;" class="form-control form-control-warning" value="' + $(this).text() + '">');
					// 			}
					// });
					table.find("tr").find(".add-transaction-sale, .edit-transaction-sale").toggle();
					$(".add-item-sale").attr("disabled", "disabled");
					 }
					 else{

					 }
				});

					});


					// Edit row on edit button click
					$(document).on("click", ".edit-dc-customer-po", function(){
							$(this).parents("tr").find("td:not(:last-child)").each(function(i){

								if (i === 5) {
									$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
								}
					});
					$(this).parents("tr").find(".add-dc-customer-po, .edit-dc-customer-po").toggle();
					$(".add-new-dc-customer").attr("disabled", "disabled");
					$(".add-new-po-customer-dc").attr("disabled", "disabled");
					$(".has_id").attr("disabled", "disabled");
					});

					// Delete row on delete button click
					$(document).on("click", ".delete-dc-customer-po", function(){
						var row =  $(this).closest('tr');
						var siblings = row.siblings();
						siblings.each(function(index) {
						$(this).children('td').first().text(index + 1);
						});
						$(this).parents("tr").remove();
						$(".add-new-dc-customer").removeAttr("disabled");
						$(".add-new-po-customer-dc").removeAttr("disabled");
						$(".has_id").removeAttr("disabled");
					});


						//SUBMIT DC SUPPLIER

						//inserting data into supplier dc using ajax request
						$('#new-dc-customer-form').on('submit',function(e){
							e.preventDefault();
							var table = $('#new-dc-customer-table');
							var data = [];

							var customer = $('#dc_customer').val();
							var cartage_amount = $('#cartage_amount').val();
							var comments = $('#comments').val();
							var follow_up = $('#follow_up').val();
							var footer_remarks = $('#footer_remarks').val();

							table.find('tr').each(function (i, el){
								if(i != 0)
								{
									var $tds = $(this).find('td');
									var row = {
										'id' : "",
										'quantity' : "",
										'po_no': "",
									};
									$tds.each(function(i, el){
										if (i === 1) {
												row["id"] = ($(this).text());
										}
										else if (i === 5) {
												row["quantity"] = ($(this).text());
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
											'customer':customer,
											'cartage_amount': cartage_amount,
											'comments': comments,
											'follow_up': follow_up,
											'footer_remarks': footer_remarks,
											'items': JSON.stringify(data),
										},
										dataType: 'json'
									})
									.done(function done(){
										alert("Delivery Challan Submitted");
										location.reload();
									})
						});



								$(".edit-dc-customer").click(function(){
									var item_code = $('#edit_item_code').val();
									req =	$.ajax({
										 headers: { "X-CSRFToken": getCookie("csrftoken") },
										 type: 'POST',
										 url : `/customer/delivery_challan/edit/${edit_id}`,
										 data:{
											 'item_code': item_code,
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
															 '<td style="display:none;" >'+type[i]['pk']+'</td>' +
															 '<td>'+type[i].fields['product_code']+'</td>' +
															 '<td>'+type[i].fields['product_name']+'</td>' +
															 '<td><pre>'+type[i].fields['product_desc']+'</pre></td>' +
															 '<td><input type="text" class="form-control" required ></td>' +
															 '<td>'+type[i].fields['unit']+'</td>' +
															 '<td style="display:none;"></td>' +
												 '<td><a class="add-dc-edit-customer" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-dc-edit-customer" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete-dc-edit-customer" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
													 '</tr>';
													 count++;
												 $("table").append(row);
											 $("table tbody tr").eq(index + 1).find(".add-dc-edit-customer, .edit-dc-edit-customer").toggle();
													 $('[data-toggle="tooltip"]').tooltip();
													 $(".edit-dc-supplier").attr("disabled", "disabled");
					 								$(".has_id").attr("disabled", "disabled");
												 }
										 }
										 else{
											 alert(data.message)
											 $(".edit-dc-customer").removeAttr("disabled");
											 $(".has_id").removeAttr("disabled");
										 }
									 });
								});


								$(".edit-po-customer-dc").click(function(){
									var item_code_po_dc = $('#item_code_po_dc').val()
									console.log(item_code_po_dc);
									req =	$.ajax({
										 headers: { "X-CSRFToken": getCookie("csrftoken") },
										 type: 'POST',
										 url : `/customer/delivery_challan/edit/${edit_id}`,
										 data:{
											 'item_code_po_dc': item_code_po_dc,
										 },
										 dataType: 'json'
									 })
									 .done(function done(data){
										 if (data.row) {
											 console.log(data.row);
											 var index = $("table tbody tr:last-child").index();
											 for (var i = 0; i < data.row.length; i++) {
												 var row = '<tr>' +
														 '<td>'+count+'</td>' +
														 '<td style="display:none;" >'+data.row[i][0]+'</td>' +
														 '<td id="get_item_code">'+data.row[i][1]+'</td>' +
														 '<td>'+data.row[i][2]+'</td>' +
														 '<td><pre>'+data.row[i][7]+'</pre></td>' +
														 '<td id="quantity"><input type="text" class="form-control form-control-sm" required ></td>' +
														 '<td>'+data.row[i][3]+'</td>' +
														 '<td style="display:none;" >'+data.id+'</td>' +
											 '<td><a class="add-edit-dc-customer-po" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-edit-dc-customer-po" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="edit-delete-dc-customer-po" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
												 '</tr>';
													 $("table").append(row);
													 $("table tbody tr").eq(index + 1).find(".add-edit-dc-customer-po, .edit-edit-dc-customer-po").toggle();
													 $('[data-toggle="tooltip"]').tooltip();
													 $('#item_code_dc').val("");
													 $(".edit-po-customer-dc").attr("disabled", "disabled");
													 $(".has_id").attr("disabled", "disabled");
											 }
										 }
										 else{
											 alert(data.message)
										 }
									 })
								});


								// Add row on add button click
								$(document).on("click", ".add-edit-dc-customer-po", function(){
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
									$(this).parents("tr").find(".add-edit-dc-customer-po, .edit-edit-dc-customer-po").toggle();
									$(".edit-po-customer-dc").removeAttr("disabled");
									$(".has_id").removeAttr("disabled");
								}
								});


								// Edit row on edit button click
								$(document).on("click", ".edit-edit-dc-customer-po", function(){
										$(this).parents("tr").find("td:not(:last-child)").each(function(i){
											if (i === 4 ) {
												$(this).html('<input type="text" class="form-control form-control-sm" value="' + $(this).text() + '">');
											}
											if (i === 6) {
												$(this).html('<input type="text" class="form-control form-control-sm" value="' + $(this).text() + '">');
											}
											if (i === 7) {
												$(this).html('<input type="text" class="form-control form-control-sm" value="' + $(this).text() + '">');
											}
								});
								$(this).parents("tr").find(".add-edit-dc-customer-po, .edit-edit-dc-customer-po").toggle();
								$(".edit-po-customer-dc").attr("disabled", "disabled");
								$(".has_id").attr("disabled", "disabled");
								});

								// Delete row on delete button click
								$(document).on("click", ".edit-delete-dc-customer-po", function(){
									var row =  $(this).closest('tr');
									var siblings = row.siblings();
									siblings.each(function(index) {
									$(this).children('td').first().text(index + 1);
									});
									$(this).parents("tr").remove();
									$(".edit-po-customer-dc").removeAttr("disabled");
									$(".has_id").removeAttr("disabled");
								});

								$(document).on("click", ".add-dc-edit-customer", function(){
									console.log("hamza");
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
									$(this).parents("tr").find(".add-dc-edit-customer, .edit-dc-edit-customer").toggle();
									$(".edit-dc-customer").removeAttr("disabled");
									$(".has_id").removeAttr("disabled");
								}
								});


								// Edit row on edit button click
								$(document).on("click", ".edit-dc-edit-customer", function(){
										$(this).parents("tr").find("td:not(:last-child)").each(function(i){
											if (i === 5 ) {
												$(this).html('<input type="text" class="form-control form-control-sm" value="' + $(this).text() + '">');
											}
								});
								$(this).parents("tr").find(".add-dc-edit-customer, .edit-dc-edit-customer").toggle();
								$(".edit-dc-supplier").attr("disabled", "disabled");
								$(".has_id").attr("disabled", "disabled");
								});

								// Delete row on delete button click
								$(document).on("click", ".delete-dc-edit-customer", function(){
									var row =  $(this).closest('tr');
									var siblings = row.siblings();
									siblings.each(function(index) {
									$(this).children('td').first().text(index + 1);
									});
									$(this).parents("tr").remove();
									$(".edit-dc-customer").removeAttr("disabled");
									$(".has_id").removeAttr("disabled");
								});


					//inserting data into supplier dc using ajax request
					$('#edit-customer-dc-submit').on('submit',function(e){
						e.preventDefault();
						var table = $('#edit-dc-customer-table');
						var customer = $('#edit_dc').val();
						var follow_up = $('#follow_up').val()
						var footer_remarks = $('#footer_remarks').val()
						var data = [];

						table.find('tr').each(function (i, el){
							if(i != 0)
							{
								var $tds = $(this).find('td');
								var row = {
									'id' : "",
									'quantity' : "",
									'po_no': "",
								};
								$tds.each(function(i, el){
									if (i === 1) {
											row["id"] = ($(this).text());
									}
									else if (i === 5) {
											row["quantity"] = ($(this).text());
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
									url : `/customer/delivery_challan/edit/${edit_id}`,
									data:{
										'customer':customer,
										'footer_remarks': footer_remarks,
										'follow_up': follow_up,
										'items': JSON.stringify(data),
									},
									dataType: 'json'
								})
								.done(function done(){
									alert("Delivery Challan Updated");
									location.reload();
								})
					});


							// END EDIT DC SUPPLIER
// ==================================================================================================================================
							// EDIT MRN SUPPLIER

								// Add row on add button click
								$(document).on("click", ".add-mrn-customer", function(){
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
									$(this).parents("tr").find(".add-mrn-customer, .edit-mrn").toggle();
								}
								});


								// Edit row on edit button click
								$(document).on("click", ".edit-mrn-customer", function(){
										$(this).parents("tr").find("td:not(:last-child)").each(function(i){
											if (i === 5) {
												$(this).html('<input type="text" class="form-control form-control-sm" value="' + $(this).text() + '">');
											}
								});
								$(this).parents("tr").find(".add-mrn, .edit-mrn-customer").toggle();
								});

							//SUBMIT EDIT MRN SUPPLIER

							//updating data into supplier mrn using ajax request
							$('#edit-mrn-customer-submit').on('submit',function(e){
								console.log(edit_id);
								e.preventDefault();
								var table = $('#edit-mrn-customer-table');
								var follow_up = $('#follow_up').val()
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
											url : `/customer/mrn/edit/${edit_id}`,
											data:{
												'follow_up': follow_up,
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

  $("#search").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#dataTable tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });

	$(document).on("click", ".account_info", function (){
     var eventId = $(this).data('id');
			 req =	$.ajax({
					headers: { "X-CSRFToken": getCookie("csrftoken") },
					type: 'POST',
					url : `/supplier/show_notification/`,
					data:{
						'eventId': eventId,
					},
					dataType: 'json'
				})
				.done(function done(data){
					$('#account_title').html( data.account_title );
					$('#tran_no').html( data.tran_no );
					$('#tran_no_input').val( data.tran_no );
				});
		 });

		 $(document).on("click", ".account_info_supplier", function (){
	      var eventId = $(this).data('id');
	 			 req =	$.ajax({
	 					headers: { "X-CSRFToken": getCookie("csrftoken") },
	 					type: 'POST',
	 					url : `/supplier/show_notification_supplier/`,
	 					data:{
	 						'eventId': eventId,
	 					},
	 					dataType: 'json'
	 				})
	 				.done(function done(data){
	 					$('#account_title_supplier').html( data.account_title );
	 					$('#tran_no_supplier').html( data.tran_no );
	 					$('#tran_no_input_supplier').val( data.tran_no );
	 				});
	 		 });

});
