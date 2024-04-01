
/* Job */
/*-------------------------------------------------------------------*/
// Job: job (jobview.html) button click
$('.button-get-job').on('click', function(e) {
	// remove slash and last directory from URL
	var url = parseURL(window.location.href)
	window.location.href = url.url+$(this).html()+'/'; 
});

// Job: job close button click
$('.btn-close-job').on('click', function(e) { 
	e.preventDefault();
	var url = parseURL(window.location.href)
	//var jobid = $('#jobview-jobinfo-JobId').find('label.value').html();
	$.ajax({ 
		url: window.location.href+'close_job/',
		type: 'post',
		data: {'csrfmiddlewaretoken': getCookie('csrftoken')},
		success: function(response) { 
			if (response.status_code == 200) {
				window.location.href = url.url+'active/';
			}
			else { 
				window.location.reload();
			}
		}
	});
});

// Job: event selection dropdown
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
		else if (name == 'Print') { action = 'print' }
		$('#div-induct-robot').hide();
	}
	$('#form-send-event').attr('action',action+'/');
});

// Job: event form submission
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


/* Tasks */
/*-------------------------------------------------------------------*/

// Task: task modal show button click
$('.button-get-task').on('click', function() { 
	var task = $(this).html();
	var jobid = $('#jobview-jobinfo-id').find('label.value').html();
	var target = $('#'+task+' .task-sn-capture');
	//var system = getCookie('system');
	//var url = parseURL(window.location.href)
	target.css('display','block');
	$.ajax({ 
		url: window.location.href+"get_capture_field_data/",
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

// Task: task send button click
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

// Task: task modal close button click
$('.taskData button.close').on('click', function() { 
	var modalObject = $(this).closest('.modal');
	modalObject.find('.task-sn-capture').empty();
	modalObject.modal("toggle");
});



/* Task: Serial Numbers */
/*-------------------------------------------------------------------*/

// Serial Number: edit button click
$('form.taskData').on('click', 'button.sn-edit', function(e){
    e.preventDefault();
    $(this).parent().find('input').attr('disabled', false)
    $(this).parent().find('input').removeClass('sn-valid')
    $(this).prev().toggle()
    $(this).toggle()
});

// Serial Number: validate button click
$('form').on('click', 'button.sn-validate', function(e){
    e.preventDefault();
    var jobtaskid = $(this).closest('div.taskData').attr('id');
    var serialnumber = $(this).prev().val();
    var target = $(this).prev();
    var old_button = $(this)
    var new_button = $(this).next();
    //var system = getCookie('system');
    var url = parseURL(window.location.href)
    if (serialnumber == '') { 
    	alert('Please enter a serial number for validation!')
    	return
    }
    $.ajax({
        url: window.location.href+'validate_serial_number/',
        type: 'post',
        data: {'csrfmiddlewaretoken': getCookie('csrftoken'), 'JobTaskId': jobtaskid, 'SerialNumber':serialnumber},
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


/* Putaway Requests */
/*-------------------------------------------------------------------*/

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
	var url = parseURL(window.location.href)
	var modalObject = $(this).closest('.modal');
	//var system = getCookie('system');
	if ($('#active-input-licenseplate').val() == '' || $('#active-input-requestrobot').val() == '' ) {
		$(modalObject).find('.invalid-feedback').show();
		$(modalObject).find('.invalid-feedback').css('display','flex')
		//alert('Please fill out all fields.')
		return
	}
	$.ajax({ 
		url: url.url+'putawayjobrequest/',
		type: 'post',
		data: $('#active-form-putaway-request').serialize(),
		success: function(response) { 
			clearModal(modalObject);
			modalObject.modal('toggle');
			window.location.reload();
		}
	});
});

