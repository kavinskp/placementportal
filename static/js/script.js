$(document).ready(function () {
    $(".data-table").each(function (_, table) {
        $(table).DataTable();
    });
});
$(document).on('hidden.bs.modal', function (event) {
  if ($('.modal:visible').length) {
    $('body').addClass('modal-open');
  }
});

