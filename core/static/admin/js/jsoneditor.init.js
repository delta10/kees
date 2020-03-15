django.jQuery(function () {
    var $ = django.jQuery;

    $("div[data-jsoneditor]").each(function() {
        var fieldName = $(this).data("jsoneditor");
        var dataDiv = $(this).parent().find("textarea[name=" + fieldName + "]")[0];

        var editor = new JSONEditor(this, {
            mode: 'tree',
            modes: ['code', 'tree'],
            onChange: function() {
                dataDiv.value = editor.getText();
            },
            onModeChange: function() {
                editor.aceEditor.setOptions({maxLines: 50})
            }
        });

        try {
            var parsedData = JSON.parse(dataDiv.value);
            editor.set(parsedData);
            editor.expandAll();
        } catch (e) {
            editor.setMode('code');
            editor.setText(dataDiv.value);
        }
    });
});
