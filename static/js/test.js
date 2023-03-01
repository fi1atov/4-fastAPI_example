$(document).ready(
	function() {
		var data = $("#employee").val();
		$.ajax({
			url : 'http://localhost:8000/recepts',
			type : 'GET',
			dataType : 'JSON',
			success : function(data) {
				$(data).each(
						function() {
							$('tbody#emp').append(
									'<tr>' +
									'<td><a href="recept/' + this.id + '"' + '>' + this.title + '</a></td>' +
									'<td>' + this.count_views + '</td>' +
									'<td>' + this.time_cook + '</td>' +
									'</tr>'
							)
						});
			},
			error : function(data) {
				alert("error");
			}

		});
	});

$(
	function () {
	$("#employee").on("click", function () {
		var data = $("#employee").val();
		$.ajax({
			url : 'http://localhost:8000/recepts',
			type : 'GET',
			dataType : 'JSON',
			success : function(data) {
				$('#content tr').not(':first').remove();
				var html = '';
				$.each(data, function(key, value) {
					var html = '<tr>'+
						'<td><a href="recept/' + this.id + '"' + '>' + value.title + '</a></td>' +
						'<td>' + value.count_views + '</td>' +
						'<td>' + value.time_cook + '</td>' +
					'</tr>';

					$('#content tr').last().after(html);
				});
			},
			error : function(data) {
				alert("error");
			}
		});
	});
});

$(
	function () {
	$( "#myForm" ).submit(function( event ) {
	  	// Stop form from submitting normally
	  	event.preventDefault();

	  	// Get some values from elements on the page:
	    var $form = $( this );
		let title_data = $form.find("input[name='title']").val();
		let time_cook_data = $form.find("input[name='time_cook']").val();
		let ingridients_data = $form.find("input[name='ingridients']").val();
		let description_data = $form.find("input[name='description']").val();

		$.ajax({
			type: "POST",
			url: "/add_recept",
			data: JSON.stringify({
				"title": title_data,
				"time_cook": time_cook_data,
				"ingridients": ingridients_data,
				"description": description_data
		  	}),
			contentType: "application/json; charset=utf-8",
			dataType:"json",
		  	success: function(){
				$( "#myForm" )[0].reset();
			},
			error: function(errMsg) {
				alert(errMsg);
			}
		});

	});
});