function getsumm(data) 
{
    console.log('main???');
    var XHR = new XMLHttpRequest();
    XHR.onreadystatechange = function() {
        if(XHR.readyState==4 && XHR.status==200) {
            var av =  JSON.parse(XHR.responseText)['avg'];
            av=parseFloat(av);
            document.getElementById('summ').innerHTML= 'Сумма рейтинга: ' + JSON.parse(XHR.responseText)['summ']+' баллов';
            document.getElementById('avg').innerHTML= 'Средний рейтинг: ' + av.toFixed(1)+' баллов';
            // alert(res);
            // return res;
        }
    }
    XHR.open('POST' , '/summrate');
    XHR.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    XHR.send('id='+data['teacher_id']);
}

function show_rates_by_season(data) {
    // var intable = '<tbody>';
    //     intable+= '</tbody>';
    getsumm(data);
    
    // alert(res);

    window.current_teaher = data['teacher_id'];
    document.getElementById('teacher_name').innerText = data['teacher'];
    var val = data['seasons'];
    var rate = data['res'];
    console.log(rate);
    
    // var cell_input = '<td><input type="text" placeholder="0"></td><td><input class="btn btn-primary" type="button" value="add"></td>';
    var arr = [];
    // console.log(val);
    for(var i = 0; i<val.length ;i++) {
        // console.log(val[i][0]);
        arr[i] = document.getElementById(val[i][0]);
    }
    str ='';
    value = 0;
    for(var i = 0 ; i<arr.length; i++) {
        // arr[i].innerHTML += '<tbody>';
        for(var j = 0 ; j<data['inds'].length; j++) {
            str += '<tr id='+ data['inds'][j][0] +'><td><h6>'+data['inds'][j][1]+'</h6></td>';
            str += '<td><input disabled id="in'+data['inds'][j][0]+'_'+arr[i].id+'" type="text" value="0" placeholder="0"</td>';
            str += '</tr>';
        }
        arr[i].innerHTML  = str;
        str ='';
        // arr[i].innerHTML += '</tbody>';
        for (var i = 0 ; i < arr.length ; i++) {
            for(var j = 0 ; j < rate[i].length ; j++) {
                document.getElementById('in'+rate[i][j][0]+'_'+arr[i].id).setAttribute('value' , rate[i][j][1]);
            }
        }
    }
}

function render_rate(data) {
    // var intable = '<tbody>';
    //     intable+= '</tbody>';
    console.log(data);
    getsumm(data);
    // document.getElementById('main_work').innerHTML ='';
    window.current_teaher = data['teacher_id'];
    document.getElementById('teacher_name').innerHTML = data['teacher'];
    var val = data['seasons'];
    var rate = data['res'];
    console.log(rate);
    
    // var cell_input = '<td><input type="text" placeholder="0"></td><td><input class="btn btn-primary" type="button" value="add"></td>';
    var arr = [];
    // console.log(val);
    for(var i = 0; i<val.length ;i++) {
        // console.log(val[i][0]);
        arr[i] = document.getElementById(val[i][0]);
    }
    str ='';
    value = 0;
    for(var i = 0 ; i<arr.length; i++) {
        // arr[i].innerHTML += '<tbody>';
        for(var j = 0 ; j<data['inds'].length; j++) {
            str += '<tr id='+ data['inds'][j][0] +'><td><h6>'+data['inds'][j][1]+'</h6></td>';
            str += '<td><input id="in'+data['inds'][j][0]+'_'+arr[i].id+'" type="text" value="0" placeholder="0"</td>';
            str += '<td><div id="b'+data['inds'][j][0]+'_'+arr[i].id+'" data-ind='+data['inds'][j][0]+' class="button addrate d-flex align-items-center">Сохранить</div></td>'+'</tr>';
        }
        arr[i].innerHTML  = str;
        str ='';
        // arr[i].innerHTML += '</tbody>';
    }
    for (var i = 0 ; i < arr.length ; i++) {
        for(var j = 0 ; j < rate[i].length ; j++) {
            document.getElementById('in'+rate[i][j][0]+'_'+arr[i].id).setAttribute('value' , rate[i][j][1]);
        }
    }
    var add = document.getElementsByClassName('addrate');
    for(var i = 0 ; i < add.length ; i++) {
        
        add[i].addEventListener('click', addrate , add[i].getAttribute('data-ind'));
    }
}

function addrate(el) {
    console.log(el);
    var  sp = el.path[0].id.split('_');
    console.log(sp);
    var code_ind = el.path[0].id.substring(1);
    console.log(code_ind);
    var val = document.getElementById('in'+code_ind).value;
    if(val == '') { val = '0'; }
    console.log(val);
    // var sp = code_ind.split('_');
    var code_season = sp[1];
    var XHR = new XMLHttpRequest();
    XHR.onreadystatechange = function() {
        if(XHR.readyState==4 && XHR.status==200) {
            console.log(JSON.parse(XHR.responseText));
            var data = {};
            data['teacher_id'] = window.current_teaher;
            getsumm(data);
        }
    }
    XHR.open('POST','/addrate');
    XHR.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    XHR.send('val='+val+'&ind='+code_ind[0]+'&season='+code_season+'&teacher='+window.current_teaher);
}