var archive_list = document.getElementsByName('archive');

for (var i = 0; i < archive_list.length; i++) {
    var archive_id = archive_list[i].getAttribute('id');
    var editor = editormd.markdownToHTML(archive_id, {
        htmlDecode: "style,script,iframe",
        emoji: true,
        taskList: true,
        tex: true,  // 默认不解析
        flowChart: true,  // 默认不解析
        sequenceDiagram: true  // 默认不解析
    });
    document.getElementById(archive_id).style.padding = "0px"
}