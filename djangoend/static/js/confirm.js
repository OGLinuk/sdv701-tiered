$(function ask() {
    $("#confirm").click(function (e) {
        if (confirm("Confirm?")) {
            $("#confirmForm").submit();
        } else {
            $(this).dialog('close');
        }
    });
});