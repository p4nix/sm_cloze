function load_html(content){
  //var global_content = document.getElementById("htmlcontent").innerHTML;
  var global_content = content;
  var global_extractcolor = "purple";
  var global_clozecolor = "darkred";

  document.getElementById("htmlcontent").innerHTML = `
    <textarea id="extractor-tinymce"></textarea>
  `;

  tinymce.init({
    selector: "#extractor-tinymce",
    plugins: 'anchor, link',
    menubar: false,
    resize: false,
    statusbar: false,
    height: '100%',
    width: '100%',
    skin: "oxide-dark",
    forced_root_block : false,
    content_css: "dark",
    //relative_urls: false,
    //remove_script_host: true,
    document_base_url : absolute_base_url,
    toolbar:
      "undo redo | styleselect | bold italic removeformat |"+
      " extractbutton clozebutton",

    content_style:
      ".extractor_cloze {background-color:" +global_clozecolor + ";}"+
      ".extractor_extract {background      :" +global_extractcolor   + ";}",

    setup: (editor) => {
      // function for making extracts
      editor.ui.registry.addButton('extractbutton', {
        text: "Extract",
        tooltip: "Extract selected text.",
        onAction: function(e) {
          do_html_extract();
        }
      });

      // function for making cloze deletions
      editor.ui.registry.addButton('clozebutton', {
        text: "Cloze",
        tooltip: "Cloze selected texts.",
        onAction: function(e) {
          do_html_cloze();
        }
      });

      // set content on initialization
      editor.on('init', function (e) {
        editor.setContent(global_content);
        pycmd("extractor-loaded");
      });
    }
  });
}

function do_html_cloze(){
  var editor = get_editor();
  var selection_content = editor.selection.getContent();

  var bm = editor.selection.getBookmark();

  editor.selection.setContent(
    '{{c::' +
    selection_content +
    '}}'
  );
  var cloze = editor.getContent();

  editor.selection.moveToBookmark(bm);

  editor.insertContent('<span class="extractor_cloze">' + selection_content + '</span>');
  editor.selection.moveToBookmark(bm);
  pycmd("extractor-cloze:"+cloze);
}

function do_html_extract(){
  var editor = get_editor();
  var extract = editor.selection.getContent();
  var bm = editor.selection.getBookmark();

  editor.selection.setContent(
    '<div class="extractor_extract">' +
    editor.selection.getContent() +
    '</div>'
  );
  editor.selection.moveToBookmark(bm);
  pycmd("extractor-extract:"+extract);
}

function get_editor(){
  return tinyMCE.get('extractor-tinymce');
}

function save_text(){
  return get_editor().getContent();
}
