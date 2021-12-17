var states={
    ACT:['Testies']
}
var main = document.getElementById('main-menu');
var sub = document.getElementById('sub-menu');

main.addEventListener('change', function(){

var selected_option = states[this.value];

while(sub.options.length > 0){
sub.options.remove(0);
}


Array.from(selected_option.foreach(function(el){

    let option = new Option(el, el);

    sub.appendChild(option);


});