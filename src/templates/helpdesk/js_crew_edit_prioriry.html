function loadPriorityList() {
    $.getJSON( "{% url 'api_priority_list' %}{{ crew.slug }}/", function( data ) {
        try {
            if (data['message'] == '') {
                var tmpl = $.templates("#tmpl-task-priority-list");
                var html = tmpl.render(data);
                $('#task-priority-list').html(html);
            }
        }
        catch (err) {
            console.error(err);
        }
    });
}

function editPriority(priority) {
    if (priority == '0') {
        var tmpl = $.templates("#tmpl-task-priority-edit");
        var html = tmpl.render({data: ''});
        $('#hidden-task-priority-edit').html(html);
        $.fancybox.open({
            src: '#hidden-task-priority-edit',
            type: 'inline',
            opts: {modal: true}
        });
        $.validate({
            form : '#form-task-priority-edit'
        });
    } else {
        $.getJSON( "{% url 'api_priority_edit' %}" + priority + "/", function( data ) {
            try {
                if (data['message'] == '') {
                    var tmpl = $.templates("#tmpl-task-priority-edit");
                    var html = tmpl.render(data);
                    $('#hidden-task-priority-edit').html(html);
                    $.fancybox.open({
                        src: '#hidden-task-priority-edit',
                        type: 'inline',
                        opts: {modal: true}
                    });
                    $.validate({
                        form : '#form-task-priority-edit'
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

function deletePriority(priority) {
    $.ajax({
        type: 'GET',
        url: '{% url 'api_priority_delete' %}' + priority + '/'
    })
        .done(function(data){
            if (data=='ok') {
                $.notify('Сохранено', 'success');
                loadPriorityList();
                loadEventsList(100);
            } else {
                $.notify(data, 'warn');
            }
        })
        .fail(function(){
            $.notify('Ошибка передачи данных');
        });
}

function savePriority(priority) {
    if (priority == '') priority = '0';
    $.ajax({
        type: 'POST',
        url: $('#form-task-priority-edit').attr('action') + priority + '/',
        data: $('#form-task-priority-edit').serialize()
    })
        .done(function(data){
            if(data=='ok') {
                $.fancybox.close();
                $.notify('Сохранено', 'success');
                loadPriorityList();
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
