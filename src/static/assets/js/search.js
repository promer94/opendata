$(document).ready(function () {
    $(".form-inline.pagination.justify-content-center").submit(function (e) {
        e.preventDefault();
        let data = $(e.target).serialize();
        $.ajax({
            method: 'POST',
            url: '/food_entry/add',
            data: data
        }).done(
            function (response) {
                let food_id = $(e.target).attr('id');
                if (response.success === 1) {
                    submitResponse('success_message', food_id)
                }
                if (response.error === 1) {
                    submitResponse('error_message', food_id)
                }

            }
        ).fail(
            function (jqXHR, textStatus) {
                let food_id = $('#foodId').val();
                submitResponse('error_network_message', food_id)
            }
        )
    });

    function submitResponse(message, id) {
        let elementId = '#' + id + message;
        let unitID = '#' + id + 'unitNumber';
        $(elementId).fadeIn('slow');
        $(unitID).val('');
        setTimeout(function(){
            $(elementId).fadeOut('slow')
        }, 3000)
    }
});

