
$("#btn-confirmer-specimen").click(function() {
    var statut = $("#statut-specimen").val();
    var label = $("#label-statut").text();
    var labelBouton = $("#btn-confirmer-specimen").html();

    if (statut == "") {
        statut = "true";
        label = "Statut: confirmé"
        labelBouton = "Annuler la confirmation"
    } else {
        statut = "";
        label = "Statut: à confirmer"
        labelBouton = "Confirmer le spécimen"
    }

    $("#statut-specimen").val(statut);
    $("#label-statut").text(label);
    $("#btn-confirmer-specimen").html(labelBouton);
});

$("#btn-soumettre-traitement").click(function(e) {
    e.preventDefault();
    var message = $("#ta-message").val();
    if (message.length > 0) {
        $("#conteneur-message").removeClass("has-error");
        $("#conteneur-message span").addClass("invisible");
        $("#form-traitement").submit();
    } else {
        $("#conteneur-message").addClass("has-error");
        $("#conteneur-message span").removeClass("invisible");
    }
});
