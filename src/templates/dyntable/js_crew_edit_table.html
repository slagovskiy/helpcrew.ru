function loadTableList() {
    $.getJSON( "{% url 'api_table_list' %}{{ crew.slug }}/", function( data ) {
        try {
            if (data['message'] == '') {
                var tmpl = $.templates("#tmpl-crew-table-list");
                var html = tmpl.render(data);
                $('#crew-table-list').html(html);
            }
        }
        catch (err) {
            console.error(err);
        }
    });
}

function editTable(table) {
    if (table == '0') {
        var tmpl = $.templates("#tmpl-crew-table-edit");
        var html = tmpl.render({data: ''});
        $('#hidden-crew-table-edit').html(html);
        $.fancybox.open({
            src: '#hidden-crew-table-edit',
            type: 'inline',
            opts: {modal: true}
        });
        $.validate({
            form : '#form-crew-table-edit'
        });
    } else {
        $.getJSON( "{% url 'api_table_edit' %}" + table + "/", function( data ) {
            try {
                if (data['message'] == '') {
                    var tmpl = $.templates("#tmpl-crew-table-edit");
                    var html = tmpl.render(data);
                    $('#hidden-crew-table-edit').html(html);
                    $.fancybox.open({
                        src: '#hidden-crew-table-edit',
                        type: 'inline',
                        opts: {modal: true}
                    });
                    $.validate({
                        form : '#form-crew-table-edit'
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

function deleteTable(table) {
    $.ajax({
        type: 'GET',
        url: '{% url 'api_table_delete' %}' + table + '/'
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

function saveTable(table) {
    if (table == '') table = '0';
    $.ajax({
        type: 'POST',
        url: $('#form-crew-table-edit').attr('action') + table + '/',
        data: $('#form-crew-table-edit').serialize()
    })
        .done(function(data){
            if(data=='ok') {
                $.fancybox.close();
                $.notify('Сохранено', 'success');
                loadTableList();
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
