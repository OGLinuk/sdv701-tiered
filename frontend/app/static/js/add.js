$(document).ready(function () {
    $('.used-book-conditions').hide();
    $('input[type=radio][name=book_type]').change(function () {
        if (this.value == 'Used') {
        $('.used-book-conditions').show();
        }
        else {
        $('.used-book-conditions').hide();
        }
    });
});