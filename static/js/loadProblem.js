$(document).ready(function() {
    $.ajax({
        url : "/static/input/01",
        dataType: "text",
        success : function (data) {
            $("#problem").html(data);
        }
    });
});