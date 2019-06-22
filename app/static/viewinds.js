function viewinds(data) {
    window.ddd = data;
    var main_work =  document.getElementById('main_work');
    var count=0;
    main_work.innerHTML = '';
    main_work.innerHTML += '<div class="red d-flex justify-content-start"><input type="text" id="name_group" size=80 placeholder="Новая группа индикаторов"><div class="button d-flex justify-content-start align-items-center" id="gadd" value="Добавить"> Добавить</div></div><br>';
    for(var i = 0 ; i < data.length; i++)  {
        // main_work.innerHTML += '<div class="block_inds">';
        main_work.innerHTML += '<div class="red group_id d-flex justify-content-between" id="g'+data[i][count][3]+'" ><div class="text">Раздел</div><input size=80 class="green" type="text" value="' + data[i][count][4] + '"><div id="'+data[i][count][3]+'" class="btngroupind button d-flex justify-content-center">Ok</div></div>';
        main_work.innerHTML += '<div class="d-flex justify-content-between"><input type="text" id="name_ind_'+data[i][count][3]+'" placeholder="новый индикатор" size="80"><div class="iadd button d-flex justify-content-center" value="Добавить индикатор" id="'+ data[i][count][3] +'">Добавить</div></div>';
        // main_work.innerHTML += '<div class="inds">';
        for(var j = 0; j < data[i].length; j++) {
            console.log(data[i].length);
            main_work.innerHTML += '<div class="red d-flex justify-content-between"><input size=130 id="i'+data[i][count][0]+'" value="' + data[i][j][1] + '" type="text"><div id="' + data[i][j][0] + '"  class="btnind button d-flex justify-content-center">Ok</div></div>';
            count++;
        }
        count=0;
    }
    var group_id = document.getElementsByClassName('group_id');
    
    //binds
    var updateindsgroup = document.getElementsByClassName('btngroupind');
    for(var i = 0 ; i < updateindsgroup.length; i++) {
        updateindsgroup[i].addEventListener('click' , function(){
            str = document.querySelector('#g'+this.id+' > input').value;
            updategroupind(this.id , str);
        });
    }
    document.getElementById('gadd').addEventListener('click' ,addgroup);
    var updateinds = document.getElementsByClassName('btnind');
    for(var i = 0 ; i < updateinds.length ; i++) {
        updateinds[i].addEventListener('click' , function() {
            str = document.querySelector('#i'+this.id).value;
            updateind(this.id , str);
        });
    }
    var iadd = document.getElementsByClassName('iadd');
    for(var i = 0 ; i < iadd.length ; i++) {
        iadd[i].addEventListener('click' , function() {
            addInd(this.id , document.querySelector('#name_ind_'+this.id).value);
        });
    }
}

function addgroup() { 
    var XHR = new XMLHttpRequest();
    XHR.onreadystatechange = function() {
        if (XHR.readyState==4 && XHR.status==200) {
            inds_rate_page();
        }
    }
    XHR.open('POST', '/add_group_ind');
    XHR.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    XHR.send('name='+document.getElementById('name_group').value);
}

function addInd(id , name) {
    console.log(id+'/'+name);
    var XHR = new XMLHttpRequest();
    XHR.onreadystatechange = function() {
        if(XHR.readyState==4 && XHR.status==200) {
            inds_rate_page();
        }
    }
    XHR.open('POST', '/add_ind');
    XHR.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    XHR.send('id='+id+'&name='+name);

}

function updategroupind(id , value) {
    console.log(id + '/'+value);
    var XHR = new XMLHttpRequest();
    XHR.onreadystatechange = function() {
        if(XHR.readyState==4 && XHR.status==200) {
            inds_rate_page();
        }
    }
    if(value=='') {
        
        XHR.open('POST' , '/delete_group_ind');
        XHR.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        XHR.send('id='+id);
    }
    else {
        XHR.open('POST' , '/update_group_ind');
        XHR.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        XHR.send('id='+id +'&value='+ value);
    }
}

function updateind(id , value) {
    console.log(id + '/'+ value);
    var XHR = new XMLHttpRequest();
    XHR.onreadystatechange = function() {
        if(XHR.readyState==4 && XHR.status==200) {
            inds_rate_page();
        }
    }
    if(value=='') {
        
        XHR.open('POST' , '/delete_ind');
        XHR.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        XHR.send('id='+id);
    }
    else {
        XHR.open('POST' , '/update_ind');
        XHR.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        XHR.send('id='+id +'&name='+ value);
    }
}