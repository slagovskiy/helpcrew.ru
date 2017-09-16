function loadServiceList() {
    $.getJSON( "{% url 'api_service_list' %}{{ crew.slug }}/", function( data ) {
        try {
            if (data['message'] == '') {
                var tmpl = $.templates("#tmpl-crew-service-list");
                var html = tmpl.render(data);
                $('#crew-service-list').html(html);
            }
        }
        catch (err) {
            console.error(err);
        }
    });
}

function editService(service) {
    if (service == '0') {
        var tmpl = $.templates("#tmpl-crew-service-edit");
        var html = tmpl.render({data: ''});
        $('#hidden-crew-service-edit').html(html);
        $.fancybox.open({
            src: '#hidden-crew-service-edit',
            type: 'inline',
            opts: {modal: true}
        });
        $.validate({
            form : '#form-crew-service-edit'
        });
    } else {
        $.getJSON( "{% url 'api_service_edit' %}" + service + "/", function( data ) {
            try {
                if (data['message'] == '') {
                    var tmpl = $.templates("#tmpl-crew-service-edit");
                    var html = tmpl.render(data);
                    $('#hidden-crew-service-edit').html(html);
                    $.fancybox.open({
                        src: '#hidden-crew-service-edit',
                        type: 'inline',
                        opts: {modal: true}
                    });
                    $.validate({
                        form : '#form-crew-service-edit'
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

function deleteService(service) {
    $.ajax({
        type: 'GET',
        url: '{% url 'api_service_delete' %}' + service + '/'
    })
        .done(function(data){
            if (data=='ok') {
                $.notify('Сохранено', 'success');
                loadServiceList();
                loadEventsList(100);
            } else {
                $.notify(data, 'warn');
            }
        })
        .fail(function(){
            $.notify('Ошибка передачи данных');
        });
}

function saveService(service) {
    if (service == '') service = '0';
    $.ajax({
        type: 'POST',
        url: $('#form-crew-service-edit').attr('action') + service + '/',
        data: $('#form-crew-service-edit').serialize()
    })
        .done(function(data){
            if(data=='ok') {
                $.fancybox.close();
                $.notify('Сохранено', 'success');
                loadServiceList();
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
