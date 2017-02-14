$(function() {
    var dataTable = $('table').dataTable({
    	ajax: {
    		url: 'drugs',
    		// dataSrc: '',
    		dataSrc:'data',
    		type: 'GET',
    		contentType: 'application/json'
    	},
    	columns: [
    		{
    			data: 'name', 
    			render: function(data, type, full, meta){
    				var pert_id = full['pert_id'];
    				return '<a target="_blank" href="report/' + pert_id + '">' + data + '</a>';
    			}
    		},
    		{'data': 'pert_id'},
    		{'data': 'nsigs'}
    	],
        bPaginate: true,
        deferRender: true,
        // Initialize sorted by number of signatures.
        // order: [[ 0, 'asc' ]],
    });
    $('.dataTables_filter').hide();
    $('#search-box').keyup(function() {
       dataTable.fnFilter(this.value);
    });
});
