$(document).ready(function(){
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
