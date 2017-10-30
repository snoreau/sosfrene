
var listePhotos = [];

var csrftoken = $("input:hidden[name='csrfmiddlewaretoken']").val();
function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

Dropzone.options.photosForm = {
    addRemoveLinks: true,
    parallelUploads: 100,
    autoProcessQueue: false,
    maxFiles: 3,
    acceptedFiles: "image/*",
    dictCancelUpload: "Annuler",
    dictRemoveFile: "Retirer la photo",
    dictDefaultMessage: "Cliquez pour ajouter ou déposez vos photos ici",
    init: function() {
        this.on("success", traiterTelechargementPhoto);
        this.on("queuecomplete", traiterFinTelechargement);
    }
};{}

$("#btn-localisation").click(function () {
    navigator.geolocation.getCurrentPosition(
            localisationReussite, localisationErreur);
});

$("#btn-soumettre-signalement").click(function () {
    $(".alert-success").addClass("invisible");

    var dropzone = Dropzone.forElement("#photos-form");
    totalPhotos = dropzone.getQueuedFiles().length;
    description = $("#id_description").val();

    if (description.length == 0) {
        $.notify({
            message: "Vous devez entrer une description."
        }, dangerOptions);
    } else if (totalPhotos == 0) {
        $.notify({
            message: "Vous devez choisir au moins une photo."
        }, dangerOptions);
    } else {
        $.LoadingOverlay("show");
        dropzone.processQueue();
    }
});

function localisationReussite(position) {
    $("#id_longitude").val(position.coords.longitude);
    $("#id_latitude").val(position.coords.latitude);
    $("#btn-soumettre-signalement").prop("disabled", false);
    $("#message-localisation")
        .text("Votre position est définie.")
        .addClass("reussite");
};

function localisationErreur(erreur) {
    $("#message-localisation")
        .text("Malheureusement, vous ne pourrez pas faire un signalement.")
        .addClass("erreur");
};

function traiterTelechargementPhoto(event, response) {
    if (response.photos_pk !== undefined) {
        for(var i = 0; i < response.photos_pk.length; i++) {
            listePhotos.push(response.photos_pk[i]);
        }
    }
}

function traiterFinTelechargement() {
    $("#id_photos_pks").val(JSON.stringify({ photos_pks: listePhotos }));
    $("#form-nouveau-signalement").submit();
}
