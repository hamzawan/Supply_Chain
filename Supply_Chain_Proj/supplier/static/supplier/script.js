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


		$('#account').on('focusout', function(){
			txtSearch = $(this).val();
			var objList = document.getElementById("account_title")  ;
			for (var i = 0; i < objList.options.length; i++) {
			 if ( objList.options[i].value.trim().toUpperCase() == txtSearch.trim().toUpperCase() ) {
					return true }
			 }
				 alert( 'Account Does not Exist!') ;
				 $(this).val("");
				 return false ; // text does not matched ;
		})

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
			//NEW RFQ SUPPLIER
			$('[data-toggle="tooltip"]').tooltip();
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
						 console.log(type);
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
				 							'<td><a class="add-rfq" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-rfq" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete-rfq" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
				 					'</tr>';
									count++;
				 				$("table").append(row);
				 			$("table tbody tr").eq(index + 1).find(".add-rfq, .edit-rfq").toggle();
				 					$('[data-toggle="tooltip"]').tooltip();

					 });
					 $('#item_code').val("");
				});

			// Add row on add button click
			$(document).on("click", ".add-rfq", function(){
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
				$(this).parents("tr").find(".add-rfq, .edit-rfq").toggle();
				$(".add-new-rfq").removeAttr("disabled");
			}
			});

			// Edit row on edit button click
			$(document).on("click", ".edit-rfq", function(){
					$(this).parents("tr").find("td:not(:last-child)").each(function(i){
						if (i === 4 ) {
							$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
						}
						if (i === 5) {
							$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
						}
			});
			$(this).parents("tr").find(".add-rfq, .edit-rfq").toggle();
			$(".add-new-rfq").attr("disabled", "disabled");
			});

			// Delete row on delete button click
			$(document).on("click", ".delete-rfq", function(){
				var row =  $(this).closest('tr');
				var siblings = row.siblings();
				siblings.each(function(index) {
				$(this).children('td').first().text(index + 1);
				});
				$(this).parents("tr").remove();
				$(".add-new-rfq").removeAttr("disabled");
			});

			//NEW RFQ SUPPLIER END

			$('#submit-rfq-supplier').on('submit',function(e){
				e.preventDefault();
				var table = $('#rfq-supplier-table');
				var data = [];
				var supplier = $('#suppliers').val();
				var rfq_no = $('#rfq_no').val();
				var attn = $('#attn').val();
				var follow_up = $('#follow_up').val();
				var footer_remarks = $('#footer_remarks').val()

				table.find('tr').each(function (i, el){
					if(i != 0)
					{
						var $tds = $(this).find('td');
						var row = {
							'id': "",
							'item_code' : "",
							'item_name' : "",
							'item_description' : "",
							'unit' : "",
							'quantity' : "",
						};
						$tds.each(function(i, el){
							if (i === 1) {
									row["id"] = ($(this).text());
							}
							if (i === 2) {
									row["item_name"] = ($(this).text());
							}
							else if (i === 3) {
									row["item_description"] = ($(this).text());
							}
							else if (i === 5) {
									row["unit"] = ($(this).text());
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
							url : '/supplier/rfq/new/',
							data:{
								'supplier': supplier,
								'rfq_no': rfq_no,
								'attn': attn,
								'follow_up': follow_up,
								'footer_remarks': footer_remarks,
								'items': JSON.stringify(data),
							},
							dataType: 'json'
						})
						.done(function done(data){
							if (data.result != "success") {
								alert(data.result)
							}
							else{
								alert("RFQ Submitted");
								location.reload();
							}
						})
			});


			// END SUBMIT RFQ SUPPLIER

			//EDIT RFQ SUPPLIER

				// edit data to rfq table from product
					$(".edit-rfq-supplier").click(function(){
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
							 if (data.row) {
								 var type = JSON.parse(data.row);
								 for (var i = 0; i < type.length; i++) {
								 var index = $("table tbody tr:last-child").index();
										 var row = '<tr>' +
												 '<td>'+count+'</td>' +
												 '<td style="display:none;">'+type[i]['pk']+'</td>' +
												 '<td>'+ type[i].fields['product_code'] +'</td>' +
												 '<td>'+ type[i].fields['product_name'] +'</td>' +
												 '<td>'+ type[i].fields['product_desc'] +'</td>' +
												 '<td><input type="text" class="form-control" value="'+ type[i].fields['unit'] +'" required ></td>' +
												 '<td><input type="text" class="form-control" required ></td>' +
									 '<td><a class="add-rfq-edit" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-rfq-edit" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete-rfq-edit" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
										 '</tr>';
										 count++;
									 $("table").append(row);
								 $("table tbody tr").eq(index + 1).find(".add-rfq-edit, .edit-rfq-edit").toggle();
										 $('[data-toggle="tooltip"]').tooltip();
									 }
							 }
							 else{
								 alert(data.message)
							 }
						 });
					});

					// Add row on add button click
					$(document).on("click", ".add-rfq-edit", function(){
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
						$(this).parents("tr").find(".add-rfq-edit, .edit-rfq-edit").toggle();
						$(".add-new-rfq-edit").removeAttr("disabled");
					}
					});


					// Edit row on edit button click
					$(document).on("click", ".edit-rfq-edit", function(){
							$(this).parents("tr").find("td:not(:last-child)").each(function(i){
								if (i === 4 ) {
									$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
								}
								if (i === 5) {
									$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
								}
					});
					$(this).parents("tr").find(".add-rfq-edit, .edit-rfq-edit").toggle();
					$(".add-new-rfq-edit").attr("disabled", "disabled");
					});

					// Delete row on delete button click
					$(document).on("click", ".delete-rfq-edit", function(){
						var row =  $(this).closest('tr');
						var siblings = row.siblings();
						siblings.each(function(index) {
						$(this).children('td').first().text(index + 1);
						});
						$(this).parents("tr").remove();
						$(".add-new-rfq-edit").removeAttr("disabled");
					});


				// END EDIT RFQ SUPPLIER

				//UPDATE EDIT RFQ SUPPLIER
					//updating data into supplier rfq using ajax request
					$('#edit-rfq-supplier-form').on('submit',function(e){
						console.log("clicked");
						e.preventDefault();
						var table = $('#edit-rfq-supplier-table');
						var edit_rfq_supplier = $("#edit_rfq_supplier").val()
						var edit_rfq_supplier_name = $("#edit_rfq_supplier_name").val()
						var edit_rfq_attn = $("#edit_rfq_attn").val()
						var edit_rfq_follow_up = $("#edit_rfq_follow_up").val()
						var edit_footer_remarks = $("#edit_footer_remarks").val()
						var data = [];
						var rfq_no = $('#edit_rfq_supplier').val();
						table.find('tr').each(function (i, el){
							if(i != 0)
							{
								var $tds = $(this).find('td');
								var row = {
									'id' : "",
									'item_name' : "",
									'item_description' : "",
									'unit' : "",
									'quantity' : "",
								};
								$tds.each(function(i, el){
									if (i === 1) {
											row["id"] = ($(this).text());
											console.log($(this).text());
									}
									else if (i === 3) {
											row["item_description"] = ($(this).text());
									}
									else if (i === 5) {
											row["unit"] = ($(this).text());
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
									url : `/supplier/rfq/edit/${edit_id}`,
									data:{
										'edit_rfq_supplier_name' :edit_rfq_supplier_name,
										'edit_rfq_attn':edit_rfq_attn,
										'edit_rfq_follow_up':edit_rfq_follow_up,
										'edit_footer_remarks':edit_footer_remarks,
										'items': JSON.stringify(data),
									},
									dataType: 'json'
								})
								.done(function done(data){
									if (data.result != "success") {
										alert(data.result)
									}
									else {
										alert("Updated");
										location.reload();
									}
								})
					});

					//END UPDATE EDIT RFQ SUPPLIER
// ======================================================================================

//=======================================================================================

				//QUOTATION SUPPLIER

// // Append table with add row in quotation supplier

			$(".add-new-quotation-supplier").click(function(){
				var item_code_quotation = $('#item_code_quotation').val();
				req =	$.ajax({
					 headers: { "X-CSRFToken": getCookie("csrftoken") },
					 type: 'POST',
					 url : '/supplier/quotation/new',
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
										 '<td>'+ type[0].fields['product_code'] +'</td>' +
										 '<td>'+ type[0].fields['product_name'] +'</td>' +
										 '<td>'+ type[0].fields['product_desc'] +'</td>' +
										 '<td><input type="text" class="form-control" required ></td>' +
										 '<td><input type="text" class="form-control" required value="'+ type[0].fields['unit'] +'" ></td>' +
										 '<td><input type="text" class="form-control" required ></td>' +
										 '<td><input type="text" class="form-control" required ></td>' +
							 '<td><a class="add-quotation" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-quotation" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete-quotation" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
								 '</tr>';
							 $("table").append(row);
						 $("table tbody tr").eq(index + 1).find(".add-quotation, .edit-quotation").toggle();
								 $('[data-toggle="tooltip"]').tooltip();
							 $('#item_code_quotation').val("");
					 }
					 else{
						 alert(data.message)
					 }
				 })
			});


			// Add row on add button click
			$(document).on("click", ".add-quotation", function(){
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
				$(this).parents("tr").find(".add-quotation, .edit-quotation").toggle();
				$(".add-new-quotation-supplier").removeAttr("disabled");
			}
			});


			// Edit row on edit button click
			$(document).on("click", ".edit-quotation", function(){
					$(this).parents("tr").find("td:not(:last-child)").each(function(i){
						if (i === 5 ) {
							$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
						}
						if (i === 6) {
							$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
						}
						if (i === 7 ) {
							$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
						}
						if (i === 8) {
							$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
						}
			});
			$(this).parents("tr").find(".add-quotation, .edit-quotation").toggle();
			$(".add-new-quotation-supplier").attr("disabled", "disabled");
			});

			// Delete row on delete button click
			$(document).on("click", ".delete-quotation", function(){
				var row =  $(this).closest('tr');
				var siblings = row.siblings();
				siblings.each(function(index) {
				$(this).children('td').first().text(index + 1);
				});
				$(this).parents("tr").remove();
				$(".add-new-quotation-supplier").removeAttr("disabled");
			});


				//SUBMIT QUOTATION SUPPLIER

				//inserting data into supplier quotation using ajax request
				$('#new-quotation-supplier-form').on('submit',function(e){
					e.preventDefault();
					var table = $('#new-quotation-supplier-table');
					var data = [];

					var supplier = $('#suppliers').val();
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
					var footer_remarks = $('#footer_remarks').val()

					table.find('tr').each(function (i, el){
						if(i != 0)
						{
							var $tds = $(this).find('td');
							var row = {
								'id': "",
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
										row["id"] = ($(this).text());
								}
								else if (i === 5) {
										row["quantity"] = ($(this).text());
								}
								else if (i === 6) {
										row["unit"] = ($(this).text());
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
								url : '/supplier/quotation/new',
								data:{
									'supplier': supplier,
									'attn': attn,
									'prcbasis': prcbasis,
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
							.done(function done(data){
								if (data.result != "success") {
									alert(data.result)
								}
								else {
									alert("Quotation Submitted");
									location.reload();
								}
							})
				});

					// EDIT QUOTATION SUPPLIER

					// edit data to rfq table from product
						$(".edit-quotation-supplier").click(function(){
							var item_code = $('#edit_item_code').val();
							req =	$.ajax({
								 headers: { "X-CSRFToken": getCookie("csrftoken") },
								 type: 'POST',
								 url : `/supplier/quotation/edit/${edit_id}`,
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
													 '<td>'+ count +'</td>' +
													 '<td style="display:none;">'+type[i]['pk']+'</td>' +
													 '<td>'+ type[i].fields['product_code'] +'</td>' +
													 '<td>'+ type[i].fields['product_name'] +'</td>' +
													 '<td>'+ type[i].fields['product_desc'] +'</td>' +
													 '<td><input type="text" class="form-control" required ></td>' +
													 '<td><input type="text" class="form-control" required ></td>' +
													 '<td><input type="text" class="form-control" required ></td>' +
													 '<td><input type="text" class="form-control" required ></td>' +
										 '<td><a class="add-quotation-edit" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-quotation-edit" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete-quotation-edit" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
											 '</tr>';
											 count++;
										 $("table").append(row);
									 $("table tbody tr").eq(index + 1).find(".add-quotation-edit, .edit-quotation-edit").toggle();
											 $('[data-toggle="tooltip"]').tooltip();
										 }
								 }
								 else{
									 alert(data.message)
								 }
							 });
						});

						// Add row on add button click
						$(document).on("click", ".add-quotation-edit", function(){
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
							$(this).parents("tr").find(".add-quotation-edit, .edit-quotation-edit").toggle();
							$(".edit-quotation-supplier").removeAttr("disabled");
						}
						});


						// Edit row on edit button click
						$(document).on("click", ".edit-quotation-edit", function(){
								$(this).parents("tr").find("td:not(:last-child)").each(function(i){
									if (i === 5 ) {
										$(this).html('<input type="text" class="form-control form-control-sm" value="' + $(this).text() + '">');
									}
									if (i === 6) {
										$(this).html('<input type="text" class="form-control form-control-sm" value="' + $(this).text() + '">');
									}
									if (i === 7) {
										$(this).html('<input type="text" class="form-control form-control-sm" value="' + $(this).text() + '">');
									}
									if (i === 8) {
										$(this).html('<input type="text" class="form-control form-control-sm" value="' + $(this).text() + '">');
									}
						});
						$(this).parents("tr").find(".add-quotation-edit, .edit-quotation-edit").toggle();
						$(".edit-quotation-supplier").attr("disabled", "disabled");
						});

						// Delete row on delete button click
						$(document).on("click", ".delete-quotation-edit", function(){
							var row =  $(this).closest('tr');
							var siblings = row.siblings();
							siblings.each(function(index) {
							$(this).children('td').first().text(index + 1);
							});
							$(this).parents("tr").remove();
							$(".edit-quotation-supplier").removeAttr("disabled");
						});


					// END EDIT QUOTATION SUPPLIER

					//SUBMIT EDIT QUOTATION SUPPLIER

					//inserting data into supplier quotation using ajax request
					$('#edit-supplier-quotation-submit').on('submit',function(e){
						e.preventDefault();
						var table = $('#edit-quotation-supplier-table');
						var data = [];

						var supplier = $('#quotation_supplier').val();
						var attn = $('#edit_quotation_attn').val();
						var prcbasis = $('#edit_quotation_prcbasis').val();
						var leadtime = $('#edit_quotation_leadtime').val();
						var validity = $('#edit_quotation_validity').val();
						var payment = $('#edit_quotation_payment').val();
						var remarks = $('#edit_quotation_remarks').val();
						var currency = $('#edit_quotation_currency_rate').val();
						var exchange_rate = $('#edit_quotation_exchange_rate').val();
						var follow_up = $('#edit_quotation_follow_up').val();
						var edit_footer_remarks = $('#edit_footer_remarks').val();


						table.find('tr').each(function (i, el){
							if(i != 0)
							{
								var $tds = $(this).find('td');
								var row = {
									'id' : "",
									'item_name' : "",
									'item_description' : "",
									'quantity' : "",
									'unit' : "",
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
									else if (i === 6) {
											row["unit"] = ($(this).text());
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
									url : `/supplier/quotation/edit/${edit_id}`,
									data:{
										'supplier': supplier,
										'attn': attn,
										'prcbasis': prcbasis,
										'leadtime': leadtime,
										'validity': validity,
										'payment': payment,
										'remarks': remarks,
										'currency': currency,
										'exchange_rate':exchange_rate,
										'follow_up': follow_up,
										'edit_footer_remarks': edit_footer_remarks,
										'items': JSON.stringify(data),
									},
									dataType: 'json'
								})
								.done(function done(data){
									if (data.result != "success") {
										alert(data.result)
									}
									else {
										alert("Quotation Submitted");
										location.reload();
									}
								})
					});

// END EDIT SUBMIT QUOTATION SUPPLIER

//=======================================================================================

				//PURCHASE ORDER SUPPLIER

// // Append table with add row in po supplier

			$(".add-new-po-supplier").click(function(){
				var item_code_po = $('#item_code_po').val();
				req =	$.ajax({
					 headers: { "X-CSRFToken": getCookie("csrftoken") },
					 type: 'POST',
					 url : '/supplier/purchase_order/new',
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
										 '<td><pre>'+type[0].fields['product_desc']+'</pre></td>' +
										 '<td><input type="text" class="form-control form-control-sm" required ></td>' +
										 '<td><input type="text" class="form-control" value="'+type[0].fields['unit']+'" required ></td>' +
										 '<td><input type="text" class="form-control" required ></td>' +
										 '<td><input type="text" class="form-control" required ></td>' +
							 '<td><a class="add-po" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-po" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete-po" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
								 '</tr>';
							 $("table").append(row);
						 $("table tbody tr").eq(index + 1).find(".add-po, .edit-po").toggle();
								 $('[data-toggle="tooltip"]').tooltip();
							 $('#item_code_po').val("");
					 }
					 else{
						 alert(data.message)
					 }
				 })
			});


			// Add row on add button click
			$(document).on("click", ".add-po", function(){
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
				$(this).parents("tr").find(".add-po, .edit-po").toggle();
				$(".add-new-po-supplier").removeAttr("disabled");
			}
			});


			// Edit row on edit button click
			$(document).on("click", ".edit-po", function(){
					$(this).parents("tr").find("td:not(:last-child)").each(function(i){
						if (i === 5 ) {
							$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
						}
						if (i === 6) {
							$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
						}
						if (i === 7 ) {
							$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
						}
						if (i === 8) {
							$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
						}
			});
			$(this).parents("tr").find(".add-po, .edit-po").toggle();
			$(".add-new-po-supplier").attr("disabled", "disabled");
			});

			// Delete row on delete button click
			$(document).on("click", ".delete-po", function(){
				var row =  $(this).closest('tr');
				var siblings = row.siblings();
				siblings.each(function(index) {
				$(this).children('td').first().text(index + 1);
				});
				$(this).parents("tr").remove();
				$(".add-new-po-supplier").removeAttr("disabled");
			});


				//SUBMIT PO SUPPLIER

			//inserting data into supplier po using ajax request
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
				var footer_remarks = $('#footer_remarks').val();

				table.find('tr').each(function (i, el){
					if(i != 0)
					{
						var $tds = $(this).find('td');
						var row = {
							'id' : "",
							'item_name' : "",
							'item_description' : "",
							'quantity' : "",
							'unit' : "",
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
							else if (i === 6) {
									row["unit"] = ($(this).text());
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
							url : '/supplier/purchase_order/new',
							data:{
								'supplier': supplier,
								'attn': attn,
								'prcbasis': prcbasis,
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
						.done(function done(data){
							if (data.result != "success") {
								alert(data.result)
							}
							else {
								alert("Purchase Order Submitted");
								location.reload();
							}
						})
			});

				// EDIT PO SUPPLIER

				// edit data to po table from product
					$(".edit-po-supplier").click(function(){
						var item_code = $('#edit_item_code').val();
						req =	$.ajax({
							 headers: { "X-CSRFToken": getCookie("csrftoken") },
							 type: 'POST',
							 url : `/supplier/purchase_order/edit/${edit_id}`,
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
												 '<td style="display:none;">'+type[0]['pk']+'</td>' +
												 '<td>'+ type[i].fields['product_code'] +'</td>' +
												 '<td>'+ type[i].fields['product_name'] +'</td>' +
												 '<td>'+ type[i].fields['product_desc'] +'</td>' +
												 '<td><input type="text" class="form-control" required ></td>' +
												 '<td><input type="text" class="form-control" value="'+ type[i].fields['unit'] +'" required ></td>' +
												 '<td><input type="text" class="form-control" required ></td>' +
												 '<td><input type="text" class="form-control" required ></td>' +
									 '<td><a class="add-po-edit" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-po-edit" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete-po-edit" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
										 '</tr>';
										 count++;
									 $("table").append(row);
								 $("table tbody tr").eq(index + 1).find(".add-po-edit, .edit-po-edit").toggle();
										 $('[data-toggle="tooltip"]').tooltip();
									 }
							 }
							 else{
								 alert(data.message)
							 }
						 });
					});

					// Add row on add button click
					$(document).on("click", ".add-po-edit", function(){
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
						$(this).parents("tr").find(".add-po-edit, .edit-po-edit").toggle();
						$(".edit-po-supplier").removeAttr("disabled");
					}
					});


					// Edit row on edit button click
					$(document).on("click", ".edit-po-edit", function(){
							$(this).parents("tr").find("td:not(:last-child)").each(function(i){
								if (i === 5 ) {
									$(this).html('<input type="text" class="form-control form-control-sm" value="' + $(this).text() + '">');
								}
								if (i === 6) {
									$(this).html('<input type="text" class="form-control form-control-sm" value="' + $(this).text() + '">');
								}
								if (i === 7) {
									$(this).html('<input type="text" class="form-control form-control-sm" value="' + $(this).text() + '">');
								}
								if (i === 8) {
									$(this).html('<input type="text" class="form-control form-control-sm" value="' + $(this).text() + '">');
								}
					});
					$(this).parents("tr").find(".add-po-edit, .edit-po-edit").toggle();
					$(".edit-po-supplier").attr("disabled", "disabled");
					});

					// Delete row on delete button click
					$(document).on("click", ".delete-po-edit", function(){
						var row =  $(this).closest('tr');
						var siblings = row.siblings();
						siblings.each(function(index) {
						$(this).children('td').first().text(index + 1);
						});
						$(this).parents("tr").remove();
						$(".edit-po-supplier").removeAttr("disabled");
					});



				//SUBMIT EDIT PO SUPPLIER

				//inserting data into supplier quotation using ajax request
				$('#edit-supplier-po-submit').on('submit',function(e){
					e.preventDefault();
					var table = $('#edit-po-supplier-table');
					var data = [];

					var supplier = $('#edit_po_supplier').val();
					var attn = $('#edit_po_attn').val();
					var prcbasis = $('#edit_po_prcbasis').val();
					var leadtime = $('#edit_po_leadtime').val();
					var validity = $('#edit_po_validity').val();
					var payment = $('#edit_po_payment').val();
					var remarks = $('#edit_po_remarks').val();
					var currency = $('#edit_po_currency_rate').val();
					var exchange_rate = $('#edit_po_exchange_rate').val();
					var follow_up = $('#edit_po_follow_up').val();
					var edit_footer_remarks = $('#edit_footer_remarks').val();

					table.find('tr').each(function (i, el){
						if(i != 0)
						{
							var $tds = $(this).find('td');
							var row = {
								'id' : "",
								'item_name' : "",
								'item_description' : "",
								'quantity' : "",
								'unit' : "",
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
								else if (i === 6) {
										row["unit"] = ($(this).text());
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
								url : `/supplier/purchase_order/edit/${edit_id}`,
								data:{
									'supplier': supplier,
									'attn': attn,
									'prcbasis': prcbasis,
									'leadtime': leadtime,
									'validity': validity,
									'payment': payment,
									'remarks': remarks,
									'currency': currency,
									'exchange_rate':exchange_rate,
									'follow_up': follow_up,
									'edit_footer_remarks':edit_footer_remarks,
									'items': JSON.stringify(data),
								},
								dataType: 'json'
							})
							.done(function done(data){
								if (data.result != "success") {
									alert(data.result)
								}
								else {
									alert("Purchase Order Updated");
									location.reload();
								}
							})
				});

					// END EDIT SUBMIT PO SUPPLIER

	//=======================================================================================

					//DC ORDER SUPPLIER

		// // Append table with add row in dc supplier

					$(".add-new-dc-supplier").click(function(){
						var item_code_dc = $('#item_code_dc').val();
						req =	$.ajax({
							 headers: { "X-CSRFToken": getCookie("csrftoken") },
							 type: 'POST',
							 url : '/supplier/delivery_challan/new',
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
										 	 	 '<td>'+ type[0].fields['product_code'] +'</td>' +
												 '<td>'+ type[0].fields['product_name'] +'</td>' +
												 '<td><pre>'+ type[0].fields['product_desc'] +'</pre></td>' +
												 '<td><input type="text" class="form-control form-control-sm" required ></td>' +
												 '<td><input type="text" class="form-control" value="'+ type[0].fields['unit'] +'" required ></td>' +
												 '<td><input type="text" class="form-control" required ></td>' +
												 '<td><input type="text" class="form-control" required ></td>' +
									 '<td><a class="add-dc" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-dc" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete-dc" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
										 '</tr>';
									 $("table").append(row);
								 $("table tbody tr").eq(index + 1).find(".add-dc, .edit-dc").toggle();
										 $('[data-toggle="tooltip"]').tooltip();
									 $('#item_code_dc').val("");
							 }
							 else{
								 alert(data.message)
							 }
						 })
					});


					// Add row on add button click
					$(document).on("click", ".add-dc", function(){
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
						$(this).parents("tr").find(".add-dc, .edit-dc").toggle();
						$(".add-new-dc-supplier").removeAttr("disabled");
					}
					});


					// Edit row on edit button click
					$(document).on("click", ".edit-dc", function(){
							$(this).parents("tr").find("td:not(:last-child)").each(function(i){
								if (i === 5 ) {
									$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
								}
								if (i === 6) {
									$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
								}
								if (i === 7 ) {
									$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
								}
								if (i === 8) {
									$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
								}
					});
					$(this).parents("tr").find(".add-dc, .edit-dc").toggle();
					$(".add-new-dc-supplier").attr("disabled", "disabled");
					});

					// Delete row on delete button click
					$(document).on("click", ".delete-dc", function(){
						var row =  $(this).closest('tr');
						var siblings = row.siblings();
						siblings.each(function(index) {
						$(this).children('td').first().text(index + 1);
						});
						$(this).parents("tr").remove();
						$(".add-new-dc-supplier").removeAttr("disabled");
					});


						//SUBMIT DC SUPPLIER

						//inserting data into supplier dc using ajax request
						$('#new-dc-supplier-form').on('submit',function(e){
							e.preventDefault();
							var table = $('#new-dc-supplier-table');
							var data = [];

							var supplier = $('#dc_supplier').val()
							var follow_up = $('#follow_up').val()
							var footer_remarks = $('#footer_remarks').val()

							table.find('tr').each(function (i, el){
								if(i != 0)
								{
									var $tds = $(this).find('td');
									var row = {
										'id' : "",
										'item_name' : "",
										'item_description' : "",
										'quantity' : "",
										'unit' : "",
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
										else if (i === 6) {
												row["unit"] = ($(this).text());
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
										url : '/supplier/delivery_challan/new',
										data:{
											'supplier': supplier,
											'footer_remarks': footer_remarks,
											'follow_up': follow_up,
											'items': JSON.stringify(data),
										},
										dataType: 'json'
									})
									.done(function done(data){
										if (data.result != "success") {
											alert(data.result)
										}
										else {
											alert("Deliver Challan Submitted");
											location.reload();
										}
									})
						});

// ==================================================================================================================================
							// EDIT MRN SUPPLIER

								// Add row on add button click
								$(document).on("click", ".add-mrn", function(){
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
									$(this).parents("tr").find(".add-mrn, .edit-mrn").toggle();
								}
								});


								// Edit row on edit button click
								$(document).on("click", ".edit-mrn", function(){
										$(this).parents("tr").find("td:not(:last-child)").each(function(i){
											if (i === 5) {
												$(this).html('<input type="text" class="form-control form-control-sm" value="' + $(this).text() + '">');
											}
								});
								$(this).parents("tr").find(".add-mrn, .edit-mrn").toggle();
								});

							//SUBMIT EDIT MRN SUPPLIER

							//updating data into supplier mrn using ajax request
							$('#edit-mrn-supplier-submit').on('submit',function(e){
								console.log(edit_id);
								e.preventDefault();
								var table = $('#edit-mrn-supplier-table');
								var follow_up = $('#follow_up').val();
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

					//ADD ITEM

					$(".add-new-row").click(function(){
						var type = $('#main_category').find(":selected").text();
						var size = $('#sub_category').find(":selected").text();
						var product_name = $('#size').val();
						var product_desc = $('#product_desc').val();
						var unit = $('#select_unit').find(":selected").text();

						var opening_stock = $('#opening_stock').val();
						console.log(unit);
						req =	$.ajax({
							 headers: { "X-CSRFToken": getCookie("csrftoken") },
							 type: 'POST',
							 url : '/inventory/add_product/',
							 data:{
								 'type': type,
								 'size': size,
								 'product_name': product_name,
								 'unit':unit,
								 'product_desc': product_desc,
								 'opening_stock': opening_stock,
							 },
							 dataType: 'json'
						 })
						 .done(function done(data){
								 var index = $("table tbody tr:last-child").index();
										 var row = '<tr>' +
										 		'<td>'+count+'</td>' +
												 '<td style="display:none">'+data.main_category_id+'</td>' +
												 '<td style="display:none">'+data.sub_category_id+'</td>' +
												 '<td>'+data.type+'</td>' +
												 '<td>'+data.size+'</td>' +
												 '<td>'+data.type+' '+data.size+' '+data.product_name+'</td>' +
												 '<td><pre><span class="inner-pre" style="font-size: 11px"">'+data.product_desc+'</span></pre></td>' +
												 '<td>'+data.product_name+'</td>' +
												 '<td>'+data.unit+'</td>' +
												 '<td>'+data.opening_stock+'</td>' +
									 '<td><a class="add-item" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-item" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete-item" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
										 '</tr>';
									 $("table").append(row);
								 $("table tbody tr").eq(index + 1).find(".add-item, .edit-item").toggle();
										 $('[data-toggle="tooltip"]').tooltip();
										 count++;
						 })
					});


					// Add row on add button click
					$(document).on("click", ".add-item", function(){
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
						$(this).parents("tr").find(".add-item, .edit-item").toggle();
						$(".add-new-row").removeAttr("disabled");
					}
					});


					// Edit row on edit button click
					$(document).on("click", ".edit-item", function(){
							$(this).parents("tr").find("td:not(:last-child)").each(function(i){
							$(this).html('<input type="text" class="form-control" value="' + $(this).text() + '">');
					});
					$(this).parents("tr").find(".add-item, .edit-item").toggle();
					$(".add-new-row").attr("disabled", "disabled");
					});

					// Delete row on delete button click
					$(document).on("click", ".delete-item", function(){
						var row =  $(this).closest('tr');
						var siblings = row.siblings();
						siblings.each(function(index) {
						$(this).children('td').first().text(index + 1);
						});
						$(this).parents("tr").remove();
						$(".add-new-row").removeAttr("disabled");
					});


						//SUBMIT DC SUPPLIER

						//inserting data into supplier dc using ajax request
						$('#add-item-form').on('submit',function(e){
							e.preventDefault();
							var table = $('#add-item-table');
							var data = [];

							table.find('tr').each(function (i, el){
								if(i != 0)
								{
									var $tds = $(this).find('td');
									var row = {
										'main_category_id' : "",
										'sub_category_id' : "",
										'item_name' : "",
										'item_description' : "",
										'unit' : "size",
										'unit' : "",
										'opening_stock':"",
									};
									$tds.each(function(i, el){
										if (i === 1) {
												row["main_category_id"] = ($(this).text());
										}
										if (i === 2) {
												row["sub_category_id"] = ($(this).text());
										}
										else if (i === 5) {
												row["item_name"] = ($(this).text());
										}
										else if (i === 6) {
												row["item_description"] = ($(this).text());
										}
										else if (i === 7) {
												row["size"] = ($(this).text());
										}
										else if (i === 8) {
												row["unit"] = ($(this).text());
										}
										else if (i === 9) {
												row["opening_stock"] = ($(this).text());
										}
									});
									data.push(row);
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
										alert("Item Added");
										location.reload();
									})
						});

							// EDIT DC SUPPLIER


								$(".edit-dc-supplier").click(function(){
									var item_code = $('#edit_item_code').val();
									req =	$.ajax({
										 headers: { "X-CSRFToken": getCookie("csrftoken") },
										 type: 'POST',
										 url : `/supplier/delivery_challan/edit/${edit_id}`,
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
															 '<td style="display:none;">'+type[0]['pk']+'</td>' +
															 '<td>'+ type[i].fields['product_code'] +'</td>' +
															 '<td>'+ type[i].fields['product_name'] +'</td>' +
															 '<td>'+ type[i].fields['product_desc'] +'</td>' +
															 '<td><input type="text" class="form-control" required ></td>' +
															 '<td><input type="text" class="form-control" value="'+ type[i].fields['unit'] +'" required ></td>' +
															 '<td><input type="text" class="form-control" required ></td>' +
												 '<td><a class="add-dc-edit" title="Add" data-toggle="tooltip"><i class="material-icons">&#xE03B;</i></a><a class="edit-dc-edit" title="Edit" data-toggle="tooltip"><i class="material-icons">&#xE254;</i></a><a class="delete-dc-edit" title="Delete" data-toggle="tooltip"><i class="material-icons">&#xE872;</i></a></td>' +
													 '</tr>';
													 count++;
												 $("table").append(row);
											 $("table tbody tr").eq(index + 1).find(".add-dc-edit, .edit-dc-edit").toggle();
													 $('[data-toggle="tooltip"]').tooltip();
												 }
										 }
										 else{
											 alert(data.message)
										 }
									 });
								});

								// Add row on add button click
								$(document).on("click", ".add-dc-edit", function(){
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
									$(this).parents("tr").find(".add-dc-edit, .edit-dc-edit").toggle();
									$(".edit-dc-supplier").removeAttr("disabled");
								}
								});


								// Edit row on edit button click
								$(document).on("click", ".edit-dc-edit", function(){
										$(this).parents("tr").find("td:not(:last-child)").each(function(i){
											if (i === 4 ) {
												$(this).html('<input type="text" class="form-control form-control-sm" value="' + $(this).text() + '">');
											}
											if (i === 5) {
												$(this).html('<input type="text" class="form-control form-control-sm" value="' + $(this).text() + '">');
											}
											if (i === 6) {
												$(this).html('<input type="text" class="form-control form-control-sm" value="' + $(this).text() + '">');
											}
											if (i === 7) {
												$(this).html('<input type="text" class="form-control form-control-sm" value="' + $(this).text() + '">');
											}
								});
								$(this).parents("tr").find(".add-dc-edit, .edit-dc-edit").toggle();
								$(".edit-dc-supplier").attr("disabled", "disabled");
								});

								// Delete row on delete button click
								$(document).on("click", ".delete-dc-edit", function(){
									var row =  $(this).closest('tr');
									var siblings = row.siblings();
									siblings.each(function(index) {
									$(this).children('td').first().text(index + 1);
									});
									$(this).parents("tr").remove();
									$(".edit-dc-supplier").removeAttr("disabled");
								});


					//inserting data into supplier dc using ajax request
					$('#edit-supplier-dc-submit').on('submit',function(e){
						e.preventDefault();
						var table = $('#edit-dc-supplier-table');
						var data = [];

							var supplier = $('#edit_dc_supplier').val()
							var edit_footer_remarks = $('#edit_footer_remarks').val()
							var follow_up = $('#follow_up').val()
							console.log(edit_footer_remarks);
						table.find('tr').each(function (i, el){
							if(i != 0)
							{
								var $tds = $(this).find('td');
								var row = {
									'id' : "",
									'item_name' : "",
									'item_description' : "",
									'quantity' : "",
									'unit' : "",
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
									else if (i === 6) {
											row["unit"] = ($(this).text());
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
									url : `/supplier/delivery_challan/edit/${edit_id}`,
									data:{
										'supplier':supplier,
										'follow_up': follow_up,
										'edit_footer_remarks': edit_footer_remarks,
										'items': JSON.stringify(data),
									},
									dataType: 'json'
								})
								.done(function done(){
									alert("Delivery Challan Updated");
									location.reload();
								})
					});

				$(document).ready(function() {
						$('.sort').DataTable();
					});
});
