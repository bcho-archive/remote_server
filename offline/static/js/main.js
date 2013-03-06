(function() {
    $(document).ready(function() {
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
    });
})();
