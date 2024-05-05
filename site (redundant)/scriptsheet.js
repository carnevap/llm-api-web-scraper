window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 80 || document.documentElement.scrollTop > 80) {
    document.getElementById("navbar").style.padding = "10px 10px";
    document.getElementById("logo").style.fontSize = "30px";
  } else {
    document.getElementById("navbar").style.padding = "60px 10px";
    document.getElementById("logo").style.fontSize = "40px";
  }
}

function myMap() {
  var mapProp= {
    center:new google.maps.LatLng(42.306485, -83.066693),
    zoom:5,
  };
  var map = new google.maps.Map(document.getElementById("googleMap"),mapProp);
}

function topFunction() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}