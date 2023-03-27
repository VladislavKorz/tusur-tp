let count = 0;

function add_button(){

    var btn = document.createElement('div');
    btn.className = "col-1";
    btn.innerHTML  = '<button type="button" class="btn btn-primary btn-circle btn-warning" onclick="del(this)"><p class="fas fa-map">✕︎</p></button>';
    var curent_count = count++;
    var value_clone = document.createElement('div');
    value_clone.id = curent_count+1;
    value_clone.className = 'row g-2';
    value_clone.setAttribute("name",'invests')
    value_clone.innerHTML =' <div class="col-6">\
              <input name="name_investments" id="name"  type="text" class="form-control" id="name_startup" placeholder="Описание">\
            </div>\
            <div class="col-5">\
              <input name="value_investments" id="value" type="number" class="form-control" id="name_startup" placeholder="Сумма">'
    btn.id = curent_count+1
    value_clone.appendChild(btn);
    var last = document.getElementsByName('invests')
    last[last.length-1].insertAdjacentHTML('afterEnd', value_clone.outerHTML);
    
    
}

function del(el){
    var par = el.parentNode
    par.parentNode.parentNode.removeChild(par.parentNode);
}
            
