(function() {
    $(document).ready(function() {
        $('hr.sep').show();
        $('div.sep').hide();
        $('abbr.timeago').timeago();

        /* replace @ with anchor */
        $('.tweet p').each(function(i, e) {
            var content = $(e).html(),
                pattern = /@(\w+)/,
                match;
            if ((match = pattern.exec(content))) {
              $(e).html(content.replace(pattern, '<a href="#">' + match[0] + '</a>'));
            }
        });

        /* new tweet pooling */
        setInterval(function() {
            var last_id = $('div.tweet').attr('data-id');
            $.ajax({
                url: 'http://127.0.0.1:1234/api/tweet/update/' + last_id,
                method: 'GET'
            }).done(function(resp) {
                if (resp.last_id > last_id) {
                    $('hr.sep').hide();
                    $('div.sep').show();
                } else {
                    $('hr.sep').show();
                    $('div.sep').hide();
                }
            });
        }, 3000);

        /* mention auto complete */
        $('#compose-form textarea').bind('input propertychange', function(e) {
            var content = $('#compose-form textarea').val(),
                bot_name = '3bugs',
                index;

            index = content.lastIndexOf('@');
            if (index != -1 && index === content.length - 1) {
                content += bot_name + ' ';
                $('#compose-form textarea').focus().val('').val(content);
            }
        });
    });
})();
