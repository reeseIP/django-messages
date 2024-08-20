// static/js/main.js

/* Helper Functions */
/*-------------------------------------------------------------------*/

function parseURL(url) {
	// get the service and system level of url
	// example:
	// request at http://localhost:8000/LOCUS/EW1/active/, service:messagelocus; system:EW1
	// parse the url to http://localhost:8000/LOCUS/EW1/
	index = url.indexOf('/',7)+1
	if (url.indexOf('/',index+1) >= 1) {
		service = url.substring(index, url.indexOf('/',index+1))
		index = url.indexOf('/',index)+1
		if (url.indexOf('/',index+1) >= 1) {
			system = url.substring(index, url.indexOf('/',index+1))
			index = url.indexOf('/',index)
		}
		else { 
			system = undefined
		}
	}
	else {
		service = undefined
		system = undefined
	}

	url = url.substring(0, index+1)
	return {  'service':service,
			  'system':system,
			  'url':url, 
	}
}

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
	$(modalObject).find('.invalid-feedback').hide();
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
	var url = parseURL(window.location.href)
	if (url.system == undefined) {
		$('#base-a-active').hide();
		$('#base-a-closed').hide();
		$('#base-div-system-users').hide();
	}
	else {
		$('#base-a-active').show();
		$('#base-a-closed').show();
		$('#base-div-system-users').show();
		$('#base-div-system-users .dropdown-header').text(url.system+' Users');
		$('#modalSystem .modal-title').text(url.system+' Authorization');
	}
});

/* Core Contorls */
/*-------------------------------------------------------------------*/

// search form submission
// **** redo search and bring up a list of results all matching the searched value regardless of system ******
$('#base-form-search').on('submit', function(e) { 
	e.preventDefault();
	var search_value = $('#base-input-navbar-search').val();
	//var system = getCookie('system');
	if ($('#base-input-navbar-search').val() == '') {
		return;
	}
	$.ajax({ 
		url: `/search/${search_value}/`,
		type: 'post',
		data: $('#base-form-search').serialize(),
		//success: function(response) { 
		//	if (response.status_code == 200) {
		//		window.location.href = '/messagelocus/'+system+'/'+jobid+'/';
		//	}
		//	else {
		//		alert('Search produced no results.')
		//		return
		//	}
		//}
	});
});

// get active jobs list
$('#base-a-active').on('click', function(e) {
	var url = parseURL(window.location.href)
	window.location.href = url.url+'active/';
});

// get closed jobs list
$('#base-a-closed').on('click', function(e) {
	var url = parseURL(window.location.href)
	window.location.href = url.url+'closed/';
});


/* User Control Dropdown Menu */
/*-------------------------------------------------------------------*/

// User Control:  toggle theme link click
$('#base-toggle-theme').on('click', function(e) { 
	if ($('#base-html-document').attr('data-bs-theme') == 'light') { 
		$('#base-html-document').attr('data-bs-theme', 'dark');
		setCookie("theme", "dark",1);
	}
	else {
		$('#base-html-document').attr('data-bs-theme', 'light'); 
		setCookie("theme", "light",1);
	}
});

// User Control: new or set user click
$('#base-div-user-controls').on('click', 'a.nav-link', function(e) { 
	var radio_input = $(this).find('input.form-check-input');
	var users = $(this).closest('div')
	var service = $(this).parent().find('.base-input-service').val();
	var system = $(this).parent().find('.base-input-system').val();
	var username = $(this).parent().find('.base-input-username').val();
	var radio_sys_user = $(`#rbg-${service}-${system}-${username}`)
	e.preventDefault();
	if ($(this).html() == $('#base-a-add-new-user').html()) {
		$("#modalSystem").modal("toggle");
	}
	else if ($(this).html() == $('#base-a-user-logout').html()) {
		$.ajax({
			url: `/logout/`, 
			type:'post',
			data: { 
				csrfmiddlewaretoken:getCookie('csrftoken'), 
				sessionid:getCookie('sessionid'), 
			}, 
			success: function(response) {
				window.location.href = '/login/';
			}
		 });
	}
	else {
		$.ajax({
			url: `/set_target_user/${service}/${system}/${username}/`, 
			type:'post',
			data: { 
				csrfmiddlewaretoken:getCookie('csrftoken'), 
				sessionid:getCookie('sessionid'), 
			}, 
			success: function(response) {
				if (response.status_code == 200) {
					//users.find('*').prop('checked', false);
					radio_input.prop("checked","checked");
					radio_sys_user.prop("checked","checked");
				}
			}
		 });
	}
});

// User Control:  delete target user button click
$('#base-div-user-controls').on('click', 'button.btn-delete-user', function(e) { 
	e.preventDefault();
	//var url = parseURL(window.location.href)
	var closest_li = $(this).closest('li');
	var service = $(this).parent().find('.base-input-service').val();
	var system = $(this).parent().find('.base-input-system').val();
	var username = $(this).parent().find('.base-input-username').val();
	var radio_sys_user = $(`#rbg-${service}-${system}-${username}`)

	$.ajax({ 
		url: `/delete_target_user/${service}/${system}/${username}/`,
		type: 'post',
		data: {csrfmiddlewaretoken:getCookie('csrftoken')},
		success: function(response) {
			closest_li.remove();
			radio_sys_user.closest('li').remove();
		}
	});
});

// User Control: system user modal close button click
$('#modalSystem button.close').on('click', function() { 
	var modalObject = $(this).closest('.modal');
	modalObject.modal("toggle");
	clearModal(modalObject);
	//$('#base-select-target-system').val($('#base-option-system-initial').val())
});

// User Control: system user modal submit button click
$('#modalSystem button.submit').on('click', function(e) {
	e.preventDefault()
	var url = parseURL(window.location.href)
	var modalObject = $(this).closest('.modal');
	var username = $('#tarSysUser').val();
	//var system = $('#base-select-target-system').val();
	if ($('#tarSysUser').val() == '' || $('#tarSysPass').val() == ''){
		$(modalObject).find('.invalid-feedback').show();
		$(modalObject).find('.invalid-feedback').css('display','flex')
		//alert('Please fill out all fields.')
		return
	}
	$.ajax({
		url: `/set_target_user/${url.service}/${url.system}/${username}/`,
		type:'post',
		data: { csrfmiddlewaretoken:getCookie('csrftoken'), 
				sessionid:getCookie('sessionid'),  
				password:$("#tarSysPass").val()
			   }, 
		success: function(response) {
			if (response.status_code == 200) {
					modalObject.modal("toggle");
			}
			clearModal(modalObject);
			window.location.reload();
		}
 	 });
});


/* Sidebar Menu Controls */
/*-------------------------------------------------------------------*/

$('#base-div-sidebar').on('click', 'button.menu-root', function(e) {
	$('#base-div-sidebar .navbar-collapse').removeClass('show');
	$('#base-div-sidebar .navbar-collapse').addClass('collapse');
	$('#base-div-sidebar .dropdown-toggle').attr('aria-expanded', 'false');
});

// Sidebar Control:  delete target user button click
$('#base-div-sidebar').on('click', 'button.btn-delete-user', function(e) { 
	e.preventDefault();
	//var url = parseURL(window.location.href)
	var closest_li = $(this).closest('li');
	var service = $(this).parent().find('.base-input-service').val();
	var system = $(this).parent().find('.base-input-system').val();
	var username = $(this).parent().find('.base-input-username').val();
	var radio_sys_user = $(`#rbg-system-users-${username}`)
	
	$.ajax({
		url: `/delete_target_user/${service}/${system}/${username}/`,
		type: 'post',
		data: {csrfmiddlewaretoken:getCookie('csrftoken')},
		success: function(response) {
			closest_li.remove();
			radio_sys_user.closest('li').remove();
		}
	});
});

// Sidebar Control: new or set user click
$('#base-div-sidebar').on('click', 'a.nav-link', function(e) { 
	var radio_input = $(this).find('input.form-check-input');
	var users = $(this).closest('div.collapse')
	var service = $(this).parent().find('.base-input-service').val();
	var system = $(this).parent().find('.base-input-system').val();
	var username = $(this).parent().find('.base-input-username').val();
	var radio_sys_user = $(`#rbg-system-users-${username}`)
	e.preventDefault();
	//if ($(this).html() == $('#base-a-add-new-user').html()) {
	//	$("#modalSystem").modal("toggle");
	//}
	$.ajax({
			url: `/set_target_user/${service}/${system}/${username}/`, 
			type:'post',
			data: { csrfmiddlewaretoken:getCookie('csrftoken'), 
					sessionid:getCookie('sessionid'), 
				   }, 
			success: function(response) {
				if (response.status_code == 200) {
					//users.find('*').prop('checked', false);
					radio_input.prop("checked","checked");
					radio_sys_user.prop("checked","checked");
				}
			}
	 	 });
});

