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
					    	<label class='task-sn-capture-label'>"+serQtyEnt+"</label>\
					    	/\
					    	<label class='task-sn-capture-label'>"+serQty+"</label>\
					    	):</label>\
					    	</div>\
					    	<div class='task-sn-capture-data'>"
			
			while (serQtyReq > 0) {
	    		markup = markup + "<div class='task-sn-input-row'>\
	    							<input name='SN"+serQty+"' class='task-sn' id='"+task+"SN"+serQty+"'>\
	    							<button class='btn-sm btn-success submit snValid' type='submit'>Validate</button>\
	    							<button class='btn-sm btn-edit snEdit' type='button' style='display:none;'>Edit</button>\
	    							</div>"
	    		serQtyReq = serQtyReq - 1
	    		serQty = serQty - 1
	    	}
	    	if (!(serQtyEnt == 0)) {
	    		console.log(response.SerialNumbers)
	    		$.each(serialnumbers, function(data) { 
		    		markup = markup + "<div class='task-sn-input-row'>\
		    							<input name='SN"+serQty+"' class='task-sn' value='"+serialnumbers[data]+"' disabled=disabled'>\
		    							<button class='btn-sm btn-success submit snValid' type='submit' style='display: none;'>Validate</button>\
		    							<button class='btn-sm btn-edit snEdit' type='button'>Edit</button>\
		    							</div>"
		    		serQtyReq = serQtyReq - 1
		    		serQty = serQty - 1
	    		});
			}
		target.append(markup)		
		$('#'+task).modal('toggle');
		}
	});
});

$('form').on('click', 'button.snValid', function(e){
    e.preventDefault();
    var jobid = $('#jobview-jobinfo-id').find('label.value').html();
    var jobtaskid = $(this).closest('div.taskData').attr('id');
    var serialnumber = $(this).prev().val();
    var target = $(this).prev();
    var button = $(this).next();

    $.ajax({
        url: '/messagelocus/validate_serial_number/',
        type: 'post',
        data: {'csrfmiddlewaretoken': getCookie('csrftoken'),'JobId': jobid, 'JobTaskId': jobtaskid, 'SerialNumber':serialnumber},
        success: function(response){
        	if (response.status_code == 200) { 
				target.attr('disabled','disabled')
				button.toggle()
				//target.parent().append("<button class='btn-sm btn-edit snEdit' type='button'>Edit</button>")
				//update the captured serial number counter
        	}
        	else { 
        		alert('Invalid Serial Number')
        	}
           
        }
    });
    $(this).toggle()
    //$(this).attr('display','none')
});

$('form.taskData').on('click', 'button.snEdit', function(e){
    e.preventDefault();
    $(this).parent().find('input').attr('disabled', false)
    $(this).prev().toggle()
    $(this).toggle()
});

$('form.taskData').on('click', 'button.taskSend', function(e){
    e.preventDefault();
    var jobid = $('#jobview-jobinfo-JobId').find('label.value').html();
    var jobtaskid = $(this).closest('div.taskData').attr('id');
    $.each($('#'+jobtaskid).find('.task-sn-capture-data').children(), function(child) { 
    	$(this).find('input').attr('disabled', false)
    	debugger;
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