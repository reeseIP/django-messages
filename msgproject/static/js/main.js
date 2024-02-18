// static/js/main.js

/* Helper Functions */
/*-------------------------------------------------------------------*/

// set cookie
function setCookie(name,value,days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}

// get cookie
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

// erase cookie
function eraseCookie(name) {   
    document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

// clear modal
function clearModal(modalObject) {
	var modalData = $(modalObject).find('div.modal-body');
	$(modalObject).find('.modal-error').hide();
  	modalData.children().each(function(child) { 
	    $(this).find('input').val('');
 	 }); 	
}

// check valid serials
function checkValidSerials(modalObject) { 
	var counter = 0;
	//var total = 0;
	var modalData = $(modalObject).find('div.modal-body');
    var modalsndata = $(modalData).find('div.task-sn-capture-data')
  	$(modalsndata).children().each(function(key,value) { 
  		if ($(this).find('input').hasClass('sn-valid')) { 
  			counter = counter + 1
  		}
	});

	snheader = $(modalObject).find('div.task-sn-capture-header');
	total = $(snheader).find('label.task-sn-capture-label-tot').html();
 	 
  	return { valid: counter, total: total };
}
	

/* Event Binds */
/*-------------------------------------------------------------------*/

// document ready
$(document).ready( function() {
	var system = getCookie('system');
	var username = getCookie('username');
	$("#flexRadioDefault"+system+username).attr('checked','');
});

// job event selection dropdown
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
	$('#form-send-event').attr('action',action+'/');
});

// job event form submission
$('#form-send-event').one('submit', function(e) { 
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
	$(this).submit();
});

// target system user modal close button click
$('#modalSystem button.close').on('click', function() { 
	var modalObject = $(this).closest('.modal');
	modalObject.modal("toggle");
	clearModal(modalObject);
	$('#base-select-target-system').val($('#base-option-system-initial').val())
});

// target system user modal submit button click
$('#modalSystem button.submit').on('click', function(e) {
	e.preventDefault()
	var modalObject = $(this).closest('.modal');
	var system = $('#base-select-target-system').val();
	if ($('#tarSysUser').val() == '' || $('#tarSysPass').val() == '' || $('#base-select-target-system').val() == null) {
		$(modalObject).find('.modal-error').show();
		//alert('Please fill out all fields.')
		return
	}
	$.ajax({
		url:'/messagelocus/set_target_user/', 
		type:'post',
		data: { csrfmiddlewaretoken:getCookie('csrftoken'), 
				sessionid:getCookie('sessionid'), 
				system:system, 
				username:$("#tarSysUser").val(), 
				password:$("#tarSysPass").val()
			   }, 
		success: function(response) {
		if (response.status_code == 200) {
			setCookie('system',system,1);
			setCookie('username',$("#tarSysUser").val(),1);
			$('#base-a-dropdown-system').html(getCookie('system'));
			modalObject.modal("toggle");
			
		}
		clearModal(modalObject);
		window.location.reload();
	}
 	 });
});

// task data modal close button click
$('.taskData button.close').on('click', function() { 
	var modalObject = $(this).closest('.modal');
	modalObject.find('.task-sn-capture').empty();
	modalObject.modal("toggle");
});

// show task data modal button click
$('.button-get-task').on('click', function() { 
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
		    							<button class='btn btn-sm btn-outline-success sn-validate' type='button'>&check;</button>\
		    							<button class='btn btn-sm btn-outline-secondary sn-edit' type='button' style='display:none;'>&#128393;</button>\
		    							</div>"
		    		serQtyReq = serQtyReq - 1
		    		serQty = serQty - 1
		    	}
		    	if (!(serQtyEnt == 0)) {
		    		$.each(serialnumbers, function(data) { 
			    		markup = markup + "<div class='task-sn-input-row'>\
			    							<input name='SN"+serQty+"' class='task-sn sn-valid' value='"+serialnumbers[data]+"' disabled='disabled'>\
			    							<button class='btn btn-sm btn-outline-success sn-validate' type='button' style='display: none;'>&check;</button>\
			    							<button class='btn btn-sm btn-outline-secondary sn-edit' type='button'>&#128393;</button>\
			    							</div>"
			    		serQtyReq = serQtyReq - 1
			    		serQty = serQty - 1
		    		});
				}
				target.append(markup)	
			}	
			$('#'+task).modal('toggle');
			if (response.SerialQty == 0) {
				$(target).css('display','none')
			}	
		}
	});
});

// validate serial number button click
$('form').on('click', 'button.sn-validate', function(e){
    e.preventDefault();
    var jobid = $('#jobview-jobinfo-id').find('label.value').html();
    var jobtaskid = $(this).closest('div.taskData').attr('id');
    var serialnumber = $(this).prev().val();
    var target = $(this).prev();
    var old_button = $(this)
    var new_button = $(this).next();
    if (serialnumber == '') { 
    	alert('Please enter a serial number for validation!')
    	return
    }
    $.ajax({
        url: '/messagelocus/validate_serial_number/',
        type: 'post',
        data: {'csrfmiddlewaretoken': getCookie('csrftoken'),'JobId': jobid, 'JobTaskId': jobtaskid, 'SerialNumber':serialnumber},
        success: function(response) {
        	if (response.status_code == 200) { 
    			if (response.data.ISERROR == 'false' || response.data.isError == 'false') {
					target.attr('disabled','disabled');
					target.addClass('sn-valid');
					var valid = checkValidSerials($(target).closest('.modal'))
					$(target).closest('.modal').find('div.task-sn-capture-header').find('label.task-sn-capture-label-ent').html(valid['valid']);
					new_button.toggle();
					$(old_button).toggle()
				}
				else { 
	        		alert('Invalid Serial Number')
	        	}
        	}
        	else { 
        		alert('Invalid Server Response: '+response.status_code)
        	}
        }
    });
    
});

// edit serial number button click
$('form.taskData').on('click', 'button.sn-edit', function(e){
    e.preventDefault();
    $(this).parent().find('input').attr('disabled', false)
    $(this).parent().find('input').removeClass('sn-valid')
    $(this).prev().toggle()
    $(this).toggle()
});

// send task button click
$('form.taskData').on('click', 'button.task-send', function(e) {
    e.preventDefault();

    var jobid = $('#jobview-jobinfo-JobId').find('label.value').html();
    var jobtaskid = $(this).closest('div.taskData').attr('id');
    var valid = checkValidSerials($(this).closest('.modal'))
    if (!(valid['valid'] == valid['total']) && !(valid['total'] == undefined)) { 
    	i
    	alert('Please validate all serial number entries.')
    	return
    }
    $.each($('#'+jobtaskid).find('.task-sn-capture-data').children(), function(key,value) { 
    	$(this).find('input').attr('disabled', false)
    });
    $(this).closest('form').submit();
    $('#'+jobtaskid).find('.task-sn-capture').empty();
    $('#'+jobtaskid).modal('toggle');
});


// putaway request modal show button
$('#active-button-putaway-request').on('click', function() { 
	$('#active-modal-putaway-request').modal('toggle');
});

// putaway request modal close button
$('#active-modal-putaway-request').on('click', 'button.close', function() { 
	var modalObject = $(this).closest('.modal');
	clearModal(modalObject);
	modalObject.modal("toggle");
});

// putaway request modal submit button
$('#active-modal-putaway-request').on('click', 'button.submit', function(e) { 
	e.preventDefault();
	var modalObject = $(this).closest('.modal');
	if ($('#active-input-licenseplate').val() == '' || $('#active-input-requestrobot').val() == '' ) {
		$(modalObject).find('.modal-error').show();
		//alert('Please fill out all fields.')
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

// search form submission
$('#base-form-search').on('submit', function(e) { 
	e.preventDefault();
	var jobid = $('#base-input-navbar-search').val();
	if ($('#base-input-navbar-search').val() == '') {
		return;
	}
	$.ajax({ 
		url: '/messagelocus/check_job_exists/',
		type: 'post',
		data: $('#base-form-search').serialize(),
		success: function(response) { 
			if (response.status_code == 200) {
				window.location.href = '/messagelocus/'+jobid+'/';
			}
			else {
				alert('Search produced no results.')
				return
			}
		}
	});
});

// user control link click
$('#base-div-user-controls').on('click', 'a.nav-link', function(e) { 
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

// user control delete target user button click
$('#base-div-user-controls').on('click', 'button.btn-delete-user', function(e) { 
	e.preventDefault();
	var username = $(this).parent().find('.base-input-username').val();
	var system = $(this).parent().find('.base-input-system').val();
	$.ajax({ 
		url: '/messagelocus/delete_target_user/',
		type: 'post',
		data: $(this).closest('form').serialize(),
		success: function(response) {
			if (getCookie('system') == system && getCookie('username') == username) {
				eraseCookie('system')
				eraseCookie('username')
			}
			window.location.reload();
		}
	});
});

// user control toggle theme link click
$('#base-toggle-theme').on('click', function(e) { 
	console.log($('#base-html-document').attr('data-bs-theme'))
	if ($('#base-html-document').attr('data-bs-theme') == 'light') { 
		$('#base-html-document').attr('data-bs-theme', 'dark');
		setCookie("theme", "dark",1);
	}
	else {
		$('#base-html-document').attr('data-bs-theme', 'light'); 
		setCookie("theme", "light",1);
	}
});

// close job button click
$('#jobview-btn-close-job').on('click', function(e) { 
	e.preventDefault();
	var jobid = $('#jobview-jobinfo-JobId').find('label.value').html();
	$.ajax({ 
		url: '/messagelocus/close_job/',
		type: 'post',
		data: {'csrfmiddlewaretoken': getCookie('csrftoken'),'JobId': jobid},
		success: function(response) { 
			if (response.status_code == 200) {
				window.location.href = '/messagelocus/active/';
			}
			else { 
				window.location.reload();
			}
		}
	});
});

// get job view button click: active, closed
$('.button-get-job').on('click', function(e) { 
	window.location.href = '/messagelocus/'+$(this).html()+'/'; 
});

