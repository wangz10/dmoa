$(function() {
    var dataTable = $('table').dataTable({
        bPaginate: true,
        // Initialize sorted by number of signatures.
        order: [[ 0, 'asc' ]]
    });
    $('.dataTables_filter').hide();
    $('#search-box').keyup(function() {
       dataTable.fnFilter(this.value);
    });
});
