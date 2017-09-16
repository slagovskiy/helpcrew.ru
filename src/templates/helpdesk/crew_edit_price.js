function getPrice(service) {
    $.getJSON( "{% url 'api_service_price_list' %}" + service + "/", function( data ) {
        try {
            if (data['message'] == '') {
                var tmpl = $.templates("#tmpl-service-price-list");
                var html = tmpl.render(data);
                $('#hidden-service-price-list').html(html);
                $.fancybox.open({
                    src: '#hidden-service-price-list',
                    type: 'inline',
                    opts: {modal: true}
                });
            }
        }
        catch (err) {
            console.error(err);
        }
    });
}

function editPrice(price) {
    if (price == '0') {
        var tmpl = $.templates("#tmpl-service-price-edit");
        var html = tmpl.render({data: ''});
        $('#hidden-service-price-edit').html(html);
        $('#form-service-price-edit input[name="service"]').val($('#service-id').val());
        $.fancybox.open({
            src: '#hidden-service-price-edit',
            type: 'inline',
            opts: {modal: true}
        });
        $.validate({
            form : '#form-service-price-edit'
        });
        $('#datetimepicker-start-date').datetimepicker({
            format: 'YYYY-MM-DD',
            keepOpen: false
        });
    } else {
        $.getJSON( "{% url 'api_service_price_edit' %}" + price + "/", function( data ) {
            try {
                if (data['message'] == '') {
                    var tmpl = $.templates("#tmpl-service-price-edit");
                    var html = tmpl.render(data);
                    $('#hidden-service-price-edit').html(html);
                    $.fancybox.open({
                        src: '#hidden-service-price-edit',
                        type: 'inline',
                        opts: {modal: true}
                    });
                    $.validate({
                        form : '#form-service-price-edit'
                    });
                    $('#datetimepicker-start-date').datetimepicker({
                        format: 'YYYY-MM-DD',
                        keepOpen: false
                    });
                } else {
                    $.notify(data['message'], 'error');
                }
            }
            catch (err) {
                console.error(err);
            }
        });
    }
}

function savePrice(price) {
    if (price == '') price = '0';
    $.ajax({
        type: 'POST',
        url: $('#form-service-price-edit').attr('action') + price + '/',
        data: $('#form-service-price-edit').serialize()
    })
        .done(function(data){
            if(data=='ok') {
                $.fancybox.close();
                $.fancybox.close();
                $.notify('Сохранено', 'success');
                getPrice($('#form-service-price-edit input[name="service"]').val());
                loadEventsList(100);
            }
            else {
                $.notify(data, 'warn');
            }
        })
        .fail(function(){
            $.notify('Ошибка передачи данных', 'error');
        });

}
