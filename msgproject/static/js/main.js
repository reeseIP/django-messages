// static/js/main.js

function setCookie(name,value,days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

function eraseCookie(name) {   
    document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

function clearModal(modalObject) {
	var modalData = $(modalObject).find('div.modal-body');
  	modalData.children().each(function(child) { 
	    $(this).find('input').val('');
 	 });
}

// document ready
$(document).ready( function() {
	var system = getCookie('system');
	if (system) { 
		$('#select-system').html(system+' \u2BC6');
	}
	else {
		$('#select-system').html('System'+' \u2BC6');
	}
});

// on click select event button, display event dropdown list
$('#select-event').on('click',function() {
	$('#div-dropdown-status').toggle();
});

// dropdown system options
$('#select-system').on('click',function() {
	$('#div-dropdown-system').toggle();
});

/* on click dropdown list option set the select event button
 to the clicked option.  If option = induct, display robot input */
$('#div-dropdown-status button.option').on('click', function(){ 
	var name = $(this).html();
	var action = $(this).attr('name');
	if (action == 'induct') {
		$('#div-induct-robot').show();
	}
	else {
		$('#div-induct-robot').hide();
	}
	$('#select-event').html(name+' \u2BC6');
	$('#form-send-event').attr('action',action+'/');
	$('#div-dropdown-status').toggle();
});

// dropdown system option button click
$('#div-dropdown-system button.option').on('click', function(){ 
	var name = $(this).html();
	var action = $(this).attr('name');
	if (!(sessionStorage.system == name)) {
		$("#modalSystem").modal("toggle");
	};
	$('#div-dropdown-system').toggle();
	// set the system in sessionStorage, set the HTML name and cookie 
	// in function after credentials are set, otherwise revert the 
	// sessionStorage to the cookie value
	sessionStorage.system = name;
});

// modalSystem close button click
$('#modalSystem button.close').on('click', function() { 
	var modalObject = $(this).closest('.modal');
	sessionStorage.system = getCookie('system');
	modalObject.modal("toggle");
	clearModal(modalObject);
});

// modalSystem close button click
$('#modalSystem button.submit').on('click', function() {
	var modalObject = $(this).closest('.modal');
	$.post('/messagelocus/set_target_user/', {csrfmiddlewaretoken:getCookie('csrftoken'), sessionid:getCookie('sessionid'), system:sessionStorage.system, username:$("#tarSysUser").val(), password:$("#tarSysPass").val()}, function(result) {
		if (result == 'Invalid User') {
			alert('Invalid User');
		}
		else { 
			setCookie('system',sessionStorage.system,1);
			setCookie('username',$("#tarSysUser").val(),1);
			$('#select-system').html(getCookie('system')+' \u2BC6');
			modalObject.modal("toggle");
		}
		clearModal(modalObject);
 	 });
});

// modalTask close button click
$('.taskData button.close').on('click', function() { 
	var modalObject = $(this).closest('.modal');
	modalObject.modal("toggle");
});

// modalTask toggle
$('.btn-task-data').on('click', function() { 
	var task = $(this).html();
	var jobid = $('#jobview-jobinfo-id').find('label.value').html()
	var target = $('#'+task+' .task-sn-capture')
	target.css('display','block')

	$.getJSON("/messagelocus/get_capture_field_data", {'JobId': jobid, 'JobTaskId': task}, function(response) {
		var serQty = response.SerialQty
		var serQtyEnt = response.SerialNumbers.length
		var markup = "<div class='task-sn-capture-header'>\
				 		<label class='task-sn-capture-label'>Serial Numbers (\
				    	<label class='task-sn-capture-label'>"+serQtyEnt+"</label>\
				    	/\
				    	<label class='task-sn-capture-label'>"+serQty+"</label>\
				    	):</label>\
				    	</div>\
				    	<div class='task-sn-capture-data'>"
		
		if (serQtyEnt == 0) {
			while (serQty > 0) {
    			markup = markup + "<form action='/messagelocus/validate_serial_number' method='post'>\
    								<input class='task-sn-capture-input' id='"+task+"SN"+serQty+"'>\
    								<button class='btn-sm btn-success submit' type='submit'>Validate</button>\
    								</form>"
    			serQty = serQty - 1
    		}
		}
		else {

		}
		target.append(markup)
		//$('#'+task+' .task-sn-capture').append(markup)
	});
	$('#'+task).modal('toggle');
});