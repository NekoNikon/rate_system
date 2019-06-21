function logout() {
    var XHR = new XMLHttpRequest();
    XHR.onreadystatechange = function() {
        if(XHR.readyState==4 && XHR.status==200) {
            document.open();
            document.write(XHR.responseText);
            document.close();
        }
    }
    XHR.open('POST' , '/logout');
    XHR.send();
}

function login() {
    var XHR = new XMLHttpRequest();
    XHR.onreadystatechange = function() {
        if(XHR.readyState==4 && XHR.status==200) {
            document.getElementById('main').innerHTML = XHR.responseText;
            // load_side();
            load_side();
            var editrate = document.getElementById('edit_rate');
            editrate.addEventListener('click' , edit_rate_page);
            var logoutbtn = document.getElementById('logout');
            logoutbtn.addEventListener('click' , logout);
        }
    }
    XHR.open('POST' , '/login');
    XHR.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    var form = document.forms['login_form'];
    var f_login = form['f_login'];
    var f_password = form['f_password'];
    var strsend = 'login='+f_login.value +'&password='+f_password.value;
    XHR.send(strsend);
}