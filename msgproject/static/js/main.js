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

function checkValidSerials(modalObject) { 
	var counter = 0;
	//var total = 0;
	var modalData = $(modalObject).find('div.modal-body');
    var modalsndata = $(modalData).find('div.task-sn-capture-data')
  	$(modalsndata).children().each(function(key,value) { 
  		if ($(this).find('input').hasClass('snValid')) { 
  			counter = counter + 1
  		}
	});

	snheader = $(modalObject).find('div.task-sn-capture-header');
	total = $(snheader).find('label.task-sn-capture-label-tot').html();
 	 
  	return { valid: counter, total: total };
}
	

// document ready
$(document).ready( function() {
	var system = getCookie('system');
	if (system) { 
		$('#base-a-dropdown-system').html(system);
	}
	else {
		$('#base-a-dropdown-system').html('System');
	}
});

// on click select event button, display event dropdown list
//$('#jobview-a-dropdown-event').on('click',function() {
//	$('#div-dropdown-status').toggle();
//});

// dropdown system options
//$('#base-a-dropdown-system').on('click',function() {
//	$('#base-ul-dropdown-system-options').toggle();
//});

/* on click dropdown list option set the select event button
 to the clicked option.  If option = induct, display robot input */
$('#jobview-select-dropdown-event').on('change', function(){ 
	var name = $(this).val();
	var action = '';

	if (name == 'Induct') {
		action = 'induct'
		$('#div-induct-robot').show();
	}
	else {
		if (name == 'Accept') { action = 'accept' }
		else if (name == 'Reject') { action = 'reject' }
		else if (name == 'Complete') { action = 'complete' }
		else if (name == 'Cancel Complete') { action = 'cancelcomplete' }
		else if (name == 'Cancel Reject') { action = 'cancelreject' }
		else if (name == 'Update Complete') { action = 'updatecomplete' }
		else if (name == 'Update Reject') { action = 'updatereject' }
		$('#div-induct-robot').hide();
	}
	//$('#jobview-a-dropdown-event').html(name);
	$('#form-send-event').attr('action',action+'/');
	//$('#div-dropdown-status').toggle();
});

// dropdown system option button click
//$('#base-ul-dropdown-system-options a.dropdown-item').on('click', function(){ 
//	var name = $(this).html();
//	var action = $(this).attr('name');
//	if (!(sessionStorage.system == name)) {
//		$("#modalSystem").modal("toggle");
//	};
//	//$('#base-ul-dropdown-system-options').toggle();
//	// set the system in sessionStorage, set the HTML name and cookie 
//	// in function after credentials are set, otherwise revert the 
//	// sessionStorage to the cookie value
//	sessionStorage.system = name;
//});

// modalSystem close button click
$('#modalSystem button.close').on('click', function() { 
	var modalObject = $(this).closest('.modal');
	sessionStorage.system = getCookie('system');
	modalObject.modal("toggle");
	clearModal(modalObject);
	$('#base-select-target-system').val($('#base-option-system-initial').val())
});

// modalSystem close button click
$('#modalSystem button.submit').on('click', function(e) {
	e.preventDefault()
	var modalObject = $(this).closest('.modal');
	var system = $('#base-select-target-system').val();
	$.post('/messagelocus/set_target_user/', {csrfmiddlewaretoken:getCookie('csrftoken'), sessionid:getCookie('sessionid'), system:system, username:$("#tarSysUser").val(), password:$("#tarSysPass").val()}, function(result) {
		if (result == 'Invalid User') {
			alert('Invalid User');
		}
		else { 
			setCookie('system',system,1);
			setCookie('username',$("#tarSysUser").val(),1);
			$('#base-a-dropdown-system').html(getCookie('system'));
			modalObject.modal("toggle");
			window.location.reload();
		}
		clearModal(modalObject);
 	 });
});

// modalTask close button click
$('.taskData button.close').on('click', function() { 
	var modalObject = $(this).closest('.modal');
	modalObject.find('.task-sn-capture').empty();
	modalObject.modal("toggle");
});

// modalTask toggle
$('.btn-task-data').on('click', function() { 
	var task = $(this).html();
	var jobid = $('#jobview-jobinfo-id').find('label.value').html();
	var target = $('#'+task+' .task-sn-capture');
	target.css('display','block');
	$.ajax({ 
		url:"/messagelocus/get_capture_field_data/",
		type: 'post',
		data: {'csrfmiddlewaretoken':getCookie('csrftoken'), 'JobId': jobid, 'JobTaskId': task},
		success: function(response) {
			var serQty = response.SerialQty
			var serQtyEnt = response.SerialNumbers.length
			var serQtyReq = serQty - serQtyEnt
			var serialnumbers = response.SerialNumbers
			var markup = "<div class='task-sn-capture-header'>\
					 		<label class='task-sn-capture-label'>Serial Numbers (\
					    	<label class='task-sn-capture-label-ent'>"+serQtyEnt+"</label>\
					    	/\
					    	<label class='task-sn-capture-label-tot'>"+serQty+"</label>\
					    	):</label>\
					    	</div>\
					    	<div class='task-sn-capture-data'>"
			if (serQty > 0) {
			
			while (serQtyReq > 0) {
	    		markup = markup + "<div class='task-sn-input-row'>\
	    							<input name='SN"+serQty+"' class='task-sn' id='"+task+"SN"+serQty+"'>\
	    							<button class='btn-sm btn-success submit snValidate' type='submit'>Validate</button>\
	    							<button class='btn-sm btn-edit snEdit' type='button' style='display:none;'>Edit</button>\
	    							</div>"
	    		serQtyReq = serQtyReq - 1
	    		serQty = serQty - 1
	    	}
	    	if (!(serQtyEnt == 0)) {
	    		$.each(serialnumbers, function(data) { 
		    		markup = markup + "<div class='task-sn-input-row'>\
		    							<input name='SN"+serQty+"' class='task-sn snValid' value='"+serialnumbers[data]+"' disabled='disabled'>\
		    							<button class='btn-sm btn-success submit snValidate' type='submit' style='display: none;'>Validate</button>\
		    							<button class='btn-sm btn-edit snEdit' type='button'>Edit</button>\
		    							</div>"
		    		serQtyReq = serQtyReq - 1
		    		serQty = serQty - 1
	    		});
			}
		target.append(markup)	
		}	
		$('#'+task).modal('toggle');
		
	}
	});
});

$('form').on('click', 'button.snValidate', function(e){
    e.preventDefault();
    var jobid = $('#jobview-jobinfo-id').find('label.value').html();
    var jobtaskid = $(this).closest('div.taskData').attr('id');
    var serialnumber = $(this).prev().val();
    var target = $(this).prev();
    var button = $(this).next();

    if (serialnumber == '') { 
    	alert('Please enter a serial number for validation!')
    	return
    }

    $.ajax({
        url: '/messagelocus/validate_serial_number/',
        type: 'post',
        data: {'csrfmiddlewaretoken': getCookie('csrftoken'),'JobId': jobid, 'JobTaskId': jobtaskid, 'SerialNumber':serialnumber},
        success: function(response){
        	if (response.status_code == 200) { 
				target.attr('disabled','disabled');
				target.addClass('snValid');
				var valid = checkValidSerials($(target).closest('.modal'))
				$(target).closest('.modal').find('div.task-sn-capture-header').find('label.task-sn-capture-label-ent').html(valid['valid']);
				button.toggle();
        	}
        	else { 
        		alert('Invalid Serial Number')
        	}
        }
    });
    $(this).toggle()
});

$('form.taskData').on('click', 'button.snEdit', function(e){
    e.preventDefault();
    $(this).parent().find('input').attr('disabled', false)
    $(this).parent().find('input').removeClass('snValid')
    $(this).prev().toggle()
    $(this).toggle()
});

$('form.taskData').on('click', 'button.taskSend', function(e) {
    e.preventDefault();
    var jobid = $('#jobview-jobinfo-JobId').find('label.value').html();
    var jobtaskid = $(this).closest('div.taskData').attr('id');
    var valid = checkValidSerials($(this).closest('.modal'))

    if (!(valid['valid'] == valid['total'])) { 
    	alert('Please validate all serial number entries.')
    	return
    }

    $.each($('#'+jobtaskid).find('.task-sn-capture-data').children(), function(key,value) { 
    	$(this).find('input').attr('disabled', false)
    });

    $.ajax({
        url: '/messagelocus/'+jobid+'/task/',
        type: 'post',
        data: $(this).closest('form').serialize(),
        success: function(response){
			$('#'+jobtaskid).find('.task-sn-capture').empty();
        	$('#'+jobtaskid).modal('toggle');
        }
    });
});


$('#active-button-putaway-request').on('click', function() { 
	$('#active-modal-putaway-request').modal('toggle');
});

$('#active-modal-putaway-request').on('click', 'button.close', function() { 
	var modalObject = $(this).closest('.modal');
	clearModal(modalObject);
	modalObject.modal("toggle");
});

$('#active-modal-putaway-request').on('click', 'button.submit', function(e) { 
	e.preventDefault();
	var modalObject = $(this).closest('.modal');
	if ($('#active-input-licenseplate').val() == '' || $('#active-input-requestrobot').val() == '' ) {
		alert('Please fill out all fields.')
		return
	}
	$.ajax({ 
		url: '/messagelocus/putawayjobrequest/',
		type: 'post',
		data: $('#active-form-putaway-request').serialize(),
		success: function(response) { 
			clearModal(modalObject);
			modalObject.modal('toggle');
			window.location.reload();
		}
	});
});

$('#form-send-event').on('submit', function(e) { 
	e.preventDefault()
	var jobid = $('#jobview-jobinfo-JobId').find('label.value').html();
	var action = $(this).attr('action')
	if ($('#jobview-select-dropdown-event').val() == 'Induct' && $('#inp-induct-robot').val() == '') {
		alert('Please enter a robot for induction.');
		return
	}
	else if ($('#jobview-select-dropdown-event').val() == $("#jobview-option-initial-event").val()) {
		alert('Please select an event.');
		return
	}
	$.ajax({ 
		url: '/messagelocus/'+jobid+'/'+action,
		type: 'post',
		data: $('#form-send-event').serialize(),
		success: function(response) { 
			window.location.reload();
		}
	});
});

$('#base-form-search').on('submit', function(e) { 
	e.preventDefault();
	var jobid = $('#base-input-navbar-search').val();
	$.ajax({ 
		url: '/messagelocus/check_job_exists/',
		type: 'post',
		data: $('#base-form-search').serialize(),
		success: function(response) { 
			if (response.job_exists) {
				window.location.href = '/messagelocus/'+jobid+'/';
			}
			else {
				alert('Search produced no results.')
				return
			}
		}
	});
});

$('#base-div-user-controls').on('click', 'a.dropdown-item', function(e) { 
	var closest_ul = $(this).closest('ul').get(0);
	var active_users = $('#base-ul-active-users').get(0);

	if ($(this).html() == $('#base-a-add-new-user').html()) {
		e.preventDefault();
		$("#modalSystem").modal("toggle");
	}
	else if (closest_ul == active_users) {
		e.preventDefault()
		var system = $(this).find('.base-label-system').html();
		var username = $(this).find('.base-label-username').html();
		setCookie('username',username,1);
		setCookie('system',system,1);
		window.location.reload();
	}
});


$('#base-div-user-controls').on('click', 'button.btn-delete-user', function(e) { 
	e.preventDefault();
	$.ajax({ 
		url: '/messagelocus/delete_external_user/',
		type: 'post',
		data: $(this).closest('form').serialize()
	});
});

			
		
//$('#base-ul-dropdown-system-options a.dropdown-item').on('click', function(){ 
//	var name = $(this).html();
//	var action = $(this).attr('name');
//	if (!(sessionStorage.system == name)) {
//		$("#modalSystem").modal("toggle");
//	};
//	//$('#base-ul-dropdown-system-options').toggle();
//	// set the system in sessionStorage, set the HTML name and cookie 
//	// in function after credentials are set, otherwise revert the 
//	// sessionStorage to the cookie value
//	sessionStorage.system = name;
//});