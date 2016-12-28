var editor = editormd.markdownToHTML('content_body', {
    htmlDecode: "style,script,iframe",
    emoji: true,
    taskList: true,
    tex: true,  // 默认不解析
    flowChart: true,  // 默认不解析
    sequenceDiagram: true  // 默认不解析
});
document.getElementById('content_body').style.padding = "0px";

var d = document, s = d.createElement('script');
s.src = '//blog-ansheng-me.disqus.com/embed.js';
s.setAttribute('data-timestamp', +new Date());
(d.head || d.body).appendChild(s);