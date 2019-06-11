$(document).ready(function () {
    $("div.search_by_genre select").val("none");
    $("div.search_by_type select").val("none");

    var selected = $('input[type=radio][name=book_type]:checked').val();
    if (selected == 'genre') {
        $('.search_by_type').hide();
        $('.search_by_genre').show();
    } else {
        $('.search_by_genre').hide();
        $('.search_by_type').show();
    }
    $('input[type=radio][name=book_type]').change(function () {
        if (this.value == 'genre') {
            $('.search_by_type').hide();
            $('.search_by_genre').show();
        } else {
            $('.search_by_genre').hide();
            $('.search_by_type').show();
        }
    });
});