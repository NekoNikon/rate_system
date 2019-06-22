function checkSession() {
    var XHR = new XMLHttpRequest();
    XHR.onreadystatechange = function() {
        if (XHR.readyState==4 && XHR.status==200) {
            var d = JSON.parse(XHR.responseText);
            console.log(d);

            if (d['session']) {
                load_side();

                return true;
            }
            return false;
        }
    }
    XHR.open('POST' , '/check');
    XHR.send();
}
function load_side() {
    var XHR = new XMLHttpRequest();
    XHR.onreadystatechange = function() {
        if (XHR.readyState==4 && XHR.status==200) {
            document.getElementById('panel').innerHTML = XHR.responseText;
            document.getElementById('logout').addEventListener('click',logout);
            document.getElementById('edit_rate').addEventListener('click' , edit_rate_page);
            document.getElementById('edit_inds').addEventListener('click' , inds_rate_page);
            // document.getElementById('edit_season').addEventListener('click' , season_rate_page);
            document.getElementById('edit_users').addEventListener('click' , users_rate_page);
            document.getElementById('edit_teachers').addEventListener('click' , teacher_rate_page);

        }
    }
    XHR.open('POST' , '/load_side');
    XHR.send();
}

window.onload = function() {

    editrate = document.getElementById('edit_rate');

    console.log('loaded');
    ajaxGet();
    load_guest_content();

    if (checkSession()==true) {

    }
    else{
        
    }
}

function load_auth_user() {
    var XHR = new XMLHttpRequest();
    XHR.onreadystatechange = function() {
        if(XHR.readyState==4 && XHR.status==200) {
            document.getElementById('main').innerHTML = XHR.responseText;
            console.log('herrr');

            load_side();
        }
    }
    XHR.open('POST' , '/load_user');
    XHR.send();
}
//write response

function load_guest_content() {
    var XHR = new XMLHttpRequest();
    XHR.onreadystatechange = function() {
        if(XHR.readyState==4 && XHR.status==200) {
            document.getElementById('guest').innerHTML = XHR.responseText;
            var searchbtn = document.getElementById('search');
            searchbtn.addEventListener('click' , searchTeacher);
        }
    }
    XHR.open('POST' , '/guest')
    XHR.send();
}





function ajaxGet() {
    var XHR = new XMLHttpRequest();
    XHR.onreadystatechange = function() {
        console.log(XHR.readyState);
        if (XHR.readyState==4 && XHR.status == 200) {
            document.getElementById('main').innerHTML = XHR.responseText;
            var loginbtn = document.getElementById('logginbtn');
            if(loginbtn) loginbtn.addEventListener('click' , login);
            // console.log(loginbtn);

        }
    }
    XHR.open('POST', '/auth');
    XHR.send();
}


function searchTeacher() {
    var code = document.getElementById('code');
    var XHR = new XMLHttpRequest();
    pre_load_rates();
    XHR.onreadystatechange = function() {
        if (XHR.readyState==4 && XHR.status==200) {
            // document.getElementById('main').innerHTML = XHR.responseText;
            console.log(JSON.parse(XHR.responseText));
            
            show_rates_by_season(JSON.parse(XHR.responseText));
        }
    }
    XHR.open('POST' , '/view_rate');
    XHR.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    console.log(typeof( code.value));

    XHR.send('code='+code.value);
}


function pre_load_rates() {
    var XHR = new XMLHttpRequest();
    XHR.onreadystatechange = function() {
        if(XHR.readyState==4 && XHR.status==200) {
            document.getElementById('main').innerHTML = XHR.responseText;
        }
    }
    XHR.open('POST', '/preloadrates');
    // XHR.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    XHR.send();
}

function load_rates(id) {
    pre_load_rates();
    var XHR = new XMLHttpRequest();
    XHR.onreadystatechange = function() {
        if(XHR.readyState==4 && XHR.status==200) {
            // document.getElementById('main').innerHTML = XHR.responseText;
            console.log(id);
            console.log(JSON.parse(XHR.responseText));
            console.log(id.path[0].id);
            render_rate(JSON.parse(XHR.responseText));
        }
    }
    XHR.open('POST' , '/load_rates');
    XHR.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

    XHR.send('id='+id.path[0].id);
}

function edit_rate_page() {
    document.getElementById('main_work').innerHTML = '';
    var XHR = new XMLHttpRequest();
    XHR.onreadystatechange = function() {
        if (XHR.readyState==4 && XHR.status==200) {
            document.getElementById('main_work').innerHTML = XHR.responseText;
            var editteacher = document.getElementsByClassName('btn-edit');
            // editteacher.addEventListener('click' , load_rates);

            for(var i = 0; i<editteacher.length ; i++)
                editteacher[i].addEventListener('click' , load_rates , editteacher[i].id);
        }
    }
    XHR.open('POST' , '/edit_rate_page')
    XHR.send()
}



function inds_rate_page() {
    document.getElementById('main_work').innerHTML = '';
    var XHR = new XMLHttpRequest();
    XHR.onreadystatechange = function(){
        if(XHR.readyState==4 && XHR.status==200) {


            console.log(JSON.parse(XHR.responseText));
            viewinds(JSON.parse(XHR.responseText));
        }
    }
    XHR.open('POST' , '/edit_inds');
    XHR.send();
}

function season_rate_page() {
    var XHR = new XMLHttpRequest();
    XHR.onreadystatechange = function() {
        if(XHR.readyState==4 && XHR.status==200) {
            console.log(JSON.parse(XHR.responseText));
            viewseason(JSON.parse(XHR.responseText));
        }
    }
    XHR.open('POST' , '/edit_season');
    XHR.send();
}

function users_rate_page() {
    var XHR = new XMLHttpRequest();
    XHR.onreadystatechange = function() {
        if(XHR.readyState==4 && XHR.status==200) {
            document.getElementById('main_work').innerHTML = '';
            document.getElementById('main_work').innerHTML = XHR.responseText;
            document.getElementById('send_data_user').addEventListener('click', add_user);
            var delbtns = document.getElementsByClassName('del_user');
            var edituser = document.getElementsByClassName('edit_user');
            for(var i = 0 ; i < delbtns.length ; i++) {
                delbtns[i].addEventListener('click' , function(){
                    del_user(this.id);
                });
            }
            for (var i = 0 ; i < edituser.length ; i++){
                edituser[i].addEventListener('click' , function() {
                    edit_user();
                });
            }
        }
    }
    XHR.open('POST' , '/user_edit');
    XHR.send();
}

function edit_user(id , login  , password , priv ) {

};

function add_user () {
    var XHR = new XMLHttpRequest();
    XHR.onreadystatechange = function() {
        if(XHR.readyState==4 && XHR.status==200) {
            users_rate_page();
        }
    }
    XHR.open('POST','/add_user');
    var form = document.forms['reg'];
    var login = form['login'].value;
    var password = form['password'].value;
    var priv = form['priv'].value;
    console.log(login);
    XHR.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    XHR.send('login='+login+'&password='+password+'&priv='+priv);
}

function teacher_rate_page() {
    var XHR = new XMLHttpRequest();
    XHR.onreadystatechange = function() {
        if(XHR.readyState==4 && XHR.status==200) {
            document.getElementById('main_work').innerHTML = XHR.responseText;
        }
    }
    XHR.open('POST' , '/load_teacher');
    XHR.send();
}

function del_user(id) {
    console.log(id);
    
    var XHR = new XMLHttpRequest();
    XHR.onreadystatechange = function() {
        if(XHR.readyState==4 && XHR.status==200) {
            users_rate_page();
            console.log(id);

        }
    }
    XHR.open('POST','/del_user');
    XHR.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

    XHR.send('id='+id);
}

function edit_teacher() {
    
}