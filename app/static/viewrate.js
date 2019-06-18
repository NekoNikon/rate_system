function showrate(data) {
    // console.log(data['inds_name']);
    document.getElementById('main_work').innerHTML = '';
    var date_set = new Set(data['seasons']);
    console.log(data);
    var html = '<h2>'+data['teacher']+'</h2>\n';
        html +='<div id="info_rate"></div>';
    var table = "<table class='table'>";
        table+= "<tbody>";
        for (var i = 0 ; i < data['data'].length; i++) {
            table+= '<tr>';
            for (var j = 0 ; j < data['data'][i].length ; j++) {
                table+= '<td>'+data['data'][i][j] + '</td>';
            }
            table+='</tr>';
        }
        table+= "</tbody>";


    document.getElementById('main_work').innerHTML = html;
    document.getElementById('info_rate').innerHTML = table;
}