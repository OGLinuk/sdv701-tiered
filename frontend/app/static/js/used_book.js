$(document).ready(function () {
    var selected = $('input[type=radio][name=book_type]:checked').val();
    if (selected == 'New') {
        $('.used-book-conditions').hide();
    } else {
        $('.used-book-conditions').show();
    }
    $('input[type=radio][name=book_type]').change(function () {
        if (this.value == 'New') {
        $('.used-book-conditions').hide();
        } else {
        $('.used-book-conditions').show();
        }
    });
});