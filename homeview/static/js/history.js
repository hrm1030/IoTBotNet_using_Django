"use strict";
// Class definition

var KTDatatableHtmlTableDemo = function() {
    // Private functions

    // demo initializer
    var demo = function() {
        var table = $('#log_table');
		var oTable = table.DataTable({
            responsive: true,
			pagingType: 'full_numbers',
        });
        $('#kt_datatable_search_status').on('change', function() {
			oTable.search($(this).val().toLowerCase(), 'Status');
		});

		$('#kt_datatable_search_type').on('change', function() {
			oTable.search($(this).val().toLowerCase(), 'Type');
		});

		$('#log_table_search_status, #log_table_search_type').selectpicker();

        $('#train_model_dataset').click(function() {
            KTApp.blockPage({
                overlayColor: 'red',
                state: 'danger',
                message: 'Please wait...'
            });
    
            setTimeout(function() {
                KTApp.unblockPage();
            }, 2000);
        });

        $('#clear').click(function() {
            KTApp.blockPage({
                overlayColor: 'red',
                state: 'danger',
                message: 'Please wait...'
            });
    
            setTimeout(function() {
                KTApp.unblockPage();
            }, 2000);
        });

    };

    return {
        // Public functions
        init: function() {
            // init dmeo
            demo();
        },
    };
}();

jQuery(document).ready(function() {
	KTDatatableHtmlTableDemo.init();
});
