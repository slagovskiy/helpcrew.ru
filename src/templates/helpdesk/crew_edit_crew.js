function loadCrew() {
    $.getJSON( "{% url 'api_crew_edit' %}{{ crew.slug }}/", function( data ) {
        try {
            if (data['message'] == '') {
                var tmpl = $.templates("#tmpl-crew-edit");
                var html = tmpl.render(data);
                $('#crew-edit').html(html);
                $.validate({
                    form : '#form-crew-edit'
                });
                $('#datetimepicker-work-start-time').datetimepicker({
                    format: 'HH:mm',
                    keepOpen: false
                });
                $('#datetimepicker-work-end-time').datetimepicker({
                    format: 'HH:mm',
                    keepOpen: false
                });
                $('#datetimepicker-lunch-start-time').datetimepicker({
                    format: 'HH:mm',
                    keepOpen: false
                });
                $('#datetimepicker-lunch-end-time').datetimepicker({
                    format: 'HH:mm',
                    keepOpen: false
                });
            }
        }
        catch (err) {
            console.error(err);
        }
    });
}

function saveCrew(crew) {
    if (crew == '') crew = '0';
    $.ajax({
        type: 'POST',
        url: $('#form-crew-edit').attr('action') + crew + '/',
        data: $('#form-crew-edit').serialize()
    })
        .done(function(data){
            if(data=='ok') {
                $.fancybox.close();
                $.notify('Сохранено', 'success');
                loadCrew();
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
