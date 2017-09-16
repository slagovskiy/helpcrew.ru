function loadFieldList(table) {
    $.getJSON( "{% url 'api_field_list' %}" + table + "/", function( data ) {
        try {
            if (data['message'] == '') {
                var tmpl = $.templates("#tmpl-table-field-list");
                var html = tmpl.render(data);
                $('#hidden-table-field-list').html(html);
                $.fancybox.open({
                    src: '#hidden-table-field-list',
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

function editField(field) {
    if (field == '0') {
        var tmpl = $.templates("#tmpl-table-field-edit");
        var html = tmpl.render({data: ''});
        $('#hidden-table-field-edit').html(html);
        $('#form-table-field-edit input[name="table"]').val($('#table-id').val());
        $.fancybox.open({
            src: '#hidden-table-field-edit',
            type: 'inline',
            opts: {modal: true}
        });
        $.validate({
            form : '#form-table-field-edit'
        });
        $('.selectpicker').selectpicker('render');
    } else {
        $.getJSON( "{% url 'api_field_edit' %}" + field + "/", function( data ) {
            try {
                if (data['message'] == '') {
                    var tmpl = $.templates("#tmpl-table-field-edit");
                    var html = tmpl.render(data);
                    $('#hidden-table-field-edit').html(html);
                    $.fancybox.open({
                        src: '#hidden-table-field-edit',
                        type: 'inline',
                        opts: {modal: true}
                    });
                    $.validate({
                        form : '#form-table-field-edit'
                    });
                    $('.selectpicker').selectpicker('render');
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

function deleteField(field) {
    $.ajax({
        type: 'GET',
        url: '{% url 'api_field_delete' %}' + field + '/'
    })
        .done(function(data){
            if (data=='ok') {
                $.notify('Сохранено', 'success');
                loadTableList();
                loadEventsList(100);
            } else {
                $.notify(data, 'warn');
            }
        })
        .fail(function(){
            $.notify('Ошибка передачи данных');
        });
}

function saveField(field) {
    if (field == '') field = '0';
    $.ajax({
        type: 'POST',
        url: $('#form-table-field-edit').attr('action') + field + '/',
        data: $('#form-table-field-edit').serialize()
    })
        .done(function(data){
            if(data=='ok') {
                $.fancybox.close();
                $.fancybox.close();
                $.notify('Сохранено', 'success');
                loadFieldList($('#form-table-field-edit input[name="table"]').val());
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
