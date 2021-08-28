$(document).ready(function () {
    $(".data-table").each(function (_, table) {
        $(table).DataTable();
    });
});

$(function () {
  $('[data-toggle="popover"]').popover()
})