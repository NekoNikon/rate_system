// function pre_view_rates() {
//     var XHR = new XMLHttpRequest();
//     XHR.onreadystatechange = function() {
//         if(XHR.readyState==4 && XHR.status==200) {
//             document.getElementById('main').innerHTML = XHR.responseText;
//         }
//     }
//     XHR.open('POST', '/preloadrates');
//     // XHR.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
//     XHR.send();
// }

// function showrate(data) {
//     // pre_view_rates();
//     document.getElementById('main_work').innerHTML ='';
//     document.getElementById('main_work').innerHTML +=  '<h4 class="text">'+data['teacher']+'</h4>';
//     pre_view_rates();
//     // console.log(data['inds_name']);
//     console.log(data);
    
//     window.current_teaher = data['teacher_id'];
//     // document.getElementById('main_work').innerHTML +=  data['teacher'].toString();
//     var val = data['seasons'];
//     var rate = data['res'];
//     console.log();
    
//     // var cell_input = '<td><input type="text" placeholder="0"></td><td><input class="btn btn-primary" type="button" value="add"></td>';
//     var arr = [];
//     // console.log(val);
//     for(var i = 0; i<val.length ;i++) {
//         // console.log(val[i][0]);
//         console.log(val[i][0]);
        
//         arr.push(document.getElementById(val[i][0]));
//         console.log(arr[i]);
        
//     }
//     str ='';
//     value = 0;
//     console.log(val);
    
//     for(var i = 0 ; i<arr.length; i++) {
//         // arr[i].innerHTML += '<tbody>';
//         for(var j = 0 ; j<data['inds'].length; j++) {
//             str += '<tr id='+ data['inds'][j][0] +'><td><h7>'+data['inds'][j][1]+'</h7></td>';
//             str += '<td><input id="in'+data['inds'][j][0]+'_'+arr[i].id+'" type="text" value="0" placeholder="0"</td>';
//             str += '<td><div id="b'+data['inds'][j][0]+'_'+arr[i].id+'" data-ind='+data['inds'][j][0]+' class="button addrate d-flex align-items-center">Сохранить</div></td>'+'</tr>';
//         }
//         arr[i].innerHTML  = str;
//         str ='';
//         // arr[i].innerHTML += '</tbody>';
//     }
//     for (var i = 0 ; i < arr.length ; i++) {
//         for(var j = 0 ; j < rate[i].length ; j++) {
//             document.getElementById('in'+rate[i][j][0]+'_'+arr[i].id).setAttribute('value' , rate[i][j][1]);
//         }
//     }
//     var add = document.getElementsByClassName('addrate');
//     for(var i = 0 ; i < add.length ; i++) {
        
//         add[i].addEventListener('click', addrate , add[i].getAttribute('data-ind'));
//     }
// }