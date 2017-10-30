
$("#btn-soumettre-message").click(function(e) {
    e.preventDefault();
    var message = $("#ta-message").val();
    if (message.length > 0) {
        $("#conteneur-message").removeClass("has-error");
        $("#conteneur-message span").addClass("invisible");
        $("#form-message").submit();
    } else {
        $("#conteneur-message").addClass("has-error");
        $("#conteneur-message span").removeClass("invisible");
    }
});
