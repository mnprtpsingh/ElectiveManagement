$(document).ready(function() {
    $('#sortable').sortable({
        containment: $('.card-body'),
        axis: "y",
    });
    $('form').submit(function() {
        const sortedIDs = $('#sortable').sortable('toArray');
        $('input[name="preferences"]').val(sortedIDs.join(' '));
    });
});