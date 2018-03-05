function getCookie (name) {
	var cookieValue=null;
	if(document.cookie && document.cookie!=''){
		for(var i=0;i<cookie.length;i++){
			var cookie = jQuery.trim(cookies[i]);
			if (cookie.substring(0,name.length+1)==(name+'=')){
				cookieValue=decodeURIComponent(cookie.substring(name.length+1));
				break;
			}
		}
	}
}

$.ajaxSetup({
	beforeSend:function (xhr,settings) {
		if(!(/^http:-*/.test(settings.url)||/^https:.*/.test(settings.url))){
			xhr.setRequestHeader("x-CSRFToken",getCookie('csrftoken'));
		}
	}
})