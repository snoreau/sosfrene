
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

$(".btn-coin-droit").click(function (event) {
    var id = $(this).data("notification");
    var $target = $(this);
    $.post("/archiver-notifications/", { id: id })
        .done(function(data) {
            if (data.reussite) {
                $target.parent().remove();
            }
        })
        .fail(function(data) {
            console.log("Erreur lors de l'archivage d'une notification: " + data);
        });
});
