$(document).ready(function() {
    var processing_state = 0;
    var token = $('[name="csrfmiddlewaretoken"]').val()
    $('#train_model_dataset').click(function(e) {
        if(processing_state == 0) {
            $('#card_title').text('Train model with dataset')
            $('#detection_tab').removeClass('active');
            $('#check_log').removeClass('active');
            $(this).addClass('active');
            var status_html = `<div class="form-group row" id="status_div">
                                <label class="col-xl-3 col-lg-3 col-form-label font-weight-bolder">Status</label>
                                <div class="col-lg-9 col-xl-9">
                                    <textarea name="status" id="status" class="form-control bg-dark text-white" cols="30" rows="10" readonly></textarea>
                                </div>
                            </div>`;
            $('#card-body').html(status_html);
            Swal.fire({
                title: 'Are you sure?',
                text: "You can start to train dataset.",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Yes, train it!'
            }).then(function (result) {
                if (result.value) {
                    // KTApp.blockPage({
                    //     overlayColor: 'red',
                    //     state: 'danger',
                    //     message: 'Please wait for 20 ~ 40 mins...<br> <h3><b id="hour">00</b>:<b id="min">00</b>:<b id="sec">00</b></h3> '
                    // });
                    // var sec = 0;
                    // var min = 0;
                    // var hour = 0;
                    processing_state = 1;
                    var counter = setInterval(function() {
                        $.ajax({
                            url : '/getmessage1',
                            method : 'post',
                            data : {
                                csrfmiddlewaretoken: token
                            },
                            success : function(data) {
                                $('#status').text(data.message)
                                $('#status').scrollTop($('#status')[0].scrollHeight);
                            }
                        });
                        // sec++;
                        // if(sec >= 60) {
                        //     min++;
                        //     sec = 0;
                        //     if(min == 60) {
                        //         hour++;
                        //         min = 0;
                        //         if(hour == 24) {
                        //             hour = 0;
                        //         } 
                        //         if(hour < 10) {
                        //             $('#hour').text('0'+hour);
                        //         }else
                        //         {
                        //             $('#hour').text(hour);
                        //         }
                        //     } 
                        //     if(min < 10) {
                        //         $('#min').text('0'+min);
                        //     }else
                        //     {
                        //         $('#min').text(min);
                        //     }
                        // } 
                        // if(sec < 10) {
                        //     $('#sec').text('0'+sec);
                            
                        // }else
                        // {
                        //     $('#sec').text(sec);     
                        // }
                    }, 500);
    
                    $.ajax({
                        url : '/trainmodel',
                        method : 'post',
                        data : {
                            csrfmiddlewaretoken: token
                        },
                        success : function(data) {
                            console.log(data);
                            // KTApp.unblockPage();
                            clearInterval(counter);
                            processing_state = 0;
                            // $('#file_div').hide(500);
                            // $('#detection_div').hide(500);
                            // $('#result_div').hide(500);
                            toastr['success'](data.message);
                            $('#status').text(data.status)
                            $('#status').scrollTop($('#status')[0].scrollHeight);
                            
                        },
                        error : function() {
                            toastr['error']('Happening any errors on training model.');
                            clearInterval(counter);
                            processing_state = 0;
                            // KTApp.unblockPage();
                        }
                    })
                }
            });
        } else {
            toastr['warning']('Please wait for a few minutes...');
        }
        
    });

    $('#check_log').click(function(e) {
        if(processing_state == 1) {
            e.preventDefault();
            
            toastr.warning('Please wait for a few minutes...');
        }
    });

    $('#detection_tab').click(function(e) {
        if(processing_state == 1) {
            e.preventDefault();
            
            toastr.warning('Please wait for a few minutes...');
        }
    });

    $('#btn_detection').click(function()
    {
        var token = $('[name="csrfmiddlewaretoken"]').val()
        if(processing_state == 0) {
            processing_state = 1;
            strPcapFilePath = $("#pcapfile").val();
            if(strPcapFilePath.search(".pcap") == -1 )
            {
                toastr['error']('You should choose the pcap file.');
                return;
            }else
            {
                toastr['success']('Detecting the abnormal attack.');
            }
            // KTApp.blockPage({
            //     overlayColor: 'red',
            //     state: 'danger',
            //     message: 'Please wait...'
            // });
            var files = $('#pcapfile')[0].files;
            var fd = new FormData();
            fd.append('file', files[0]);
            fd.append('csrfmiddlewaretoken', token);
            processing_state = 1;
            $.ajax({
                url: '/file_upload',
                type: 'post',
                data: fd,
                contentType: false,
                processData: false,
                success: function(data){
                    console.log(data)
                    var interv = setInterval(() => {
                        $.ajax({
                            url : '/getmessage2',
                            method : 'post',
                            data : {
                                csrfmiddlewaretoken: token
                            },
                            success : function(data) {
                                $('#status').text(data.message)
                                $('#status').scrollTop($('#status')[0].scrollHeight);
                            }
                        });
                    }, 500);
                    $.ajax({
                        url : '/detector',
                        method : 'post',
                        data : {
                            path : strPcapFilePath,
                            csrfmiddlewaretoken: token
                        },
                        success : function(data) {
                            console.log(data);
                            if(data.state == -1)
                            {
                                //ALERT SUSPICIOUS ACTIVITY FOUND!!!
                                //Abnormal attack!
                                $('#result').val('ALERT SUSPICIOUS ACTIVITY FOUND!!!\nAbnormal attack!');
                            }else if (data.state == 0) 
                            {
                                //Normal
                                $('#result').val('Normal');
                            }
                            // KTApp.unblockPage();
                            clearInterval(interv);
                            processing_state = 0;
                            $('#status').text(data.message)
                            $('#status').scrollTop($('#status')[0].scrollHeight);
                        },
                        error : function() {
                            toastr['error']('Happening any errors on abnormal detector.');
                            clearInterval(interv);
                            processing_state = 0;
                            // KTApp.unblockPage();
                        }
                    })
                },
             });
        } else {
            toastr['error']('Please wait for a few minutes...');
        }
    });


    $('#clear').click(function() {
        if(processing_state == 0) {
            Swal.fire({
                title: 'Are you sure?',
                text: "You can clear data in models.",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Yes, clear it!'
            }).then(function (result) {
                if (result.value) {
                    KTApp.blockPage({
                        overlayColor: 'red',
                        state: 'danger',
                        message: 'Please wait...'
                    });
                    $.ajax({
                        url : '/clearmodel',
                        method : 'post',
                        data : {
                            csrfmiddlewaretoken: token
                        },
                        success : function(data) {
                            console.log(data);
            
                            toastr['success'](data.message)
                            KTApp.unblockPage();
                        },
                        error : function() {
                            toastr['error']('Happening any errors on training model.');
                            KTApp.unblockPage();
                        }
                    })
                }
            });
        } else {
            toastr.warning('Please wait for a few minutes...');
        }
        
        
    });
});

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