// Mobile nav toggle
(function(){
  var btn = document.getElementById('navToggle');
  var menu = document.getElementById('mobileMenu');
  if(btn && menu){
    btn.addEventListener('click', function(){ menu.classList.toggle('open'); });
  }
})();
