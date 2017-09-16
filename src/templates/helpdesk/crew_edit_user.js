function loadUserList() {
    $.getJSON( "{% url 'api_user_list' %}{{ crew.slug }}/", function( data ) {
        try {
            if (data['message'] == '') {
                var tmpl = $.templates("#tmpl-crew-user-list");
                var html = tmpl.render(data);
                $('#crew-user-list').html(html);
            }
        }
        catch (err) {
            console.error(err);
        }
    });
}

function saveUser(member, type) {
    $.ajax({
        type: 'GET',
        url: '{% url 'api_user_edit' %}' + member + '/' + type + '/'
    })
        .done(function(data){
            if(data=='ok') {
                $.fancybox.close();
                $.notify('Сохранено', 'success');
                loadUserList();
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


function deleteUser(member) {
    $.ajax({
        type: 'GET',
        url: '{% url 'api_user_delete' %}' + member + '/'
    })
        .done(function(data){
            if (data=='ok') {
                $.notify('Сохранено', 'success');
                loadUserList();
                loadEventsList(100);
            } else {
                $.notify(data, 'warn');
            }
        })
        .fail(function(){
            $.notify('Ошибка передачи данных');
        });
}

function openInvite() {
    var tmpl = $.templates("#tmpl-crew-user-invite");
    var html = tmpl.render('');
    $('#hidden-crew-user-add').html(html);
    $.fancybox.open({
        src: '#hidden-crew-user-add',
        type: 'inline',
        opts: {modal: true}
    });
    $.validate({
        form : '#form-crew-user-invite'
    });
}

function saveInvite() {
    $.ajax({
        type: 'POST',
        url: $('#form-crew-user-invite').attr('action'),
        data: $('#form-crew-user-invite').serialize()
    })
        .done(function(data){
            if(data=='ok') {
                $.fancybox.close();
                $.notify('Приглашение отправлено', 'success');
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

function addExistUser() {
    var tmpl = $.templates("#tmpl-crew-user-add");
    var html = tmpl.render('');
    $('#hidden-crew-user-add').html(html);
    $.fancybox.open({
        src: '#hidden-crew-user-add',
        type: 'inline',
        opts: {modal: true}
    });
    $.validate({
        form : '#form-crew-user-add'
    });
}
