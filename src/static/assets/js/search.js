$("#food-entry-form").submit(function (e) {
    e.preventDefault();
    let data = $("#food-entry-form").serialize();
    console.log(data);
    $.ajax({
        method: 'POST',
        url: '/food_entry/add',
        data: data
    }).done(
        function (response) {
            $('#unitNumber').val('');
            console.log(response)
        }
    ).fail(
        function( jqXHR, textStatus ) {
            console.log( "Request failed: " + textStatus );
        }
    )
});