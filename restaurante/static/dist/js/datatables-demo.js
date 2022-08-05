// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTable').DataTable({

    "paging":  true,
        "ordering": true,
        "info":     true,
        "searching": true,
      });
});
