function onClickLogin(){
	var username_pattern = new RegExp("^[a-zA-Z]+$");
	var password_pattern = new RegExp("^[a-zA-Z0-9]{6,12}$");
	let username = document.forms[0].Username.value;
	let password = document.forms[0].Password.value;
	if (!username_pattern.test(username)) {
        alert("Only English character can be used as username!");
        document.forms[0].Username.focus();
        return;
    }
    if (!password_pattern.test(password)) {
        alert("Only English character and digits can be used as password, which shoule be in the range of 6-12!");
        document.forms[0].Password.focus();
        return;
    }

    if (username == 'Boris' && password == '123456'){
    	document.location.href = './table.html',true;
    	// alert("good goog")
    }else{
    	alert("Wrong username or password!")
    }
}