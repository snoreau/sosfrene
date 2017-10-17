$(function(){
    $('.navbar .navbar-collapse').on('show.bs.collapse', function(e) {
        $('.navbar .navbar-collapse').not(this).collapse('hide');
    });
});

$("#btn-ajout-signalement").click(function () {
    if (navigator.geolocation) {
        $("#test").text("test");
    }
    navigator.geolocation.getCurrentPosition(
        localisationReussite, localisationErreur);
});

var localisationReussite = function(position) {
    alert("test");
    console.log(position);
};

var localisationErreur = function(erreur) {
    $("#test").text(erreur.code);
};
