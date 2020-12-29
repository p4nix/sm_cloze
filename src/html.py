text_front = """
<!--DO NOT MODIFY, THIS IS NOT YOUR TERRITORY! -->
<div id="source">
		{{edit:Source}}
</div>

<div id="text">
  		{{Text}}
</div>
{{Extra}}
"""

cloze_front = """
<!--DO NOT MODIFY, THIS IS NOT YOUR TERRITORY! -->
{{#%s}}
	<div id="cloze" data-card="{{Card}}">
		{{%s}}
	</div>
	<script>
		%s
	</script>
{{/%s}}
"""

cloze_back = """
<!--DO NOT MODIFY, THIS IS NOT YOUR TERRITORY! -->
<div id="back" id="answer">
{{FrontSide}}
</div>

<br><br><br>
<div id="edit_field">{{edit:%s}}</div>
{{Extra}}
"""

css = """
<!--DO NOT MODIFY, THIS IS NOT YOUR TERRITORY! -->
#source {
	font-size: 13px;
}
p {margin: 0; padding: 0;}
#edit_field{
	font-size: 20px;
	border: 1px solid white;
	border-radius: 5px;
	padding: 10px;
}
.card {
	font-size: 20px;
	text-align: center;
	padding: 10px;
}
#text {
    height: 90vh;
	text-align: justify;
}
.smcloze {
	color: violet !important;
}
.current-cloze {
  color: #99f;
  font-weight: bold;
}
"""

text_back = """
<!--DO NOT MODIFY, THIS IS NOT YOUR TERRITORY! -->
Schedule accordingly!<br>
Usually handled by add-on!
"""

js = """
var expEl = document.getElementById("cloze");
var card = expEl.getAttribute("data-card");


// Format of cloze when there is no hint.
var blanksFormat = "[{blanks}]";
var hintFormat = "[{hints}]";


// Identify characters in content that will not be replaced with blanks.
var charKeepRegex = /(`.+?`)/
var charKeepGlobalRegex = /(`.+?`)/g

// Regex used to split on spaces so spaces can be preserved.
var spaceSplit = /\s+/;

// Matches diacritics so we can remove them for length computation purposes.
var combiningDiacriticMarks = /[\u0300-\u036f]/g;

// Wraps the content in a span with given classes so we can apply CSS to it.
function wrap_span(content, classes) {
  return "<span class=" + classes + ">" + content + "</span>";
}

var disable_special_cloze_function = false;


// Performs string replacement of tokens in a {token} format.  For example, {hint} in the format
// will be replaced with the value of the hint key in the dictionary.
function string_format(format, d) {
  return format.replace(/\{([a-z]+)\}/g, function(match, key) {
    return d[key];
  });
}

function strip_keep_chars(content) {
  return content.replace(charKeepGlobalRegex, function(p) {
    return p.slice(1, p.length - 1);
  });
}

// Generates the replacement for the given content and hint.  The result is wrapped in a span
// with the given classes.
function replace_content(content, hint, classes) {
  var contentReplacement = null;
  if (hint) {
    contentReplacement = "[" + hint + "]"
  }
  else {
    contentReplacement = "[...]"
  }
  return wrap_span(contentReplacement, classes);
}

var cardMatch = card.match(/[^\d]+(\d+)$/);
var isBack = !!document.getElementById("back");
if (cardMatch && !disable_special_cloze_function) {
  var expContent = expEl.innerHTML;

  expEl.innerHTML = expContent.replace(/\{\{c::(.+?\)*)\}\}/g,function(match, content) {
    var contentSplit = content.split(/::/)
    var contentHint = null;

    if (contentSplit.length == 2) {
      contentHint = contentSplit[1];
      content = contentSplit[0]
    }
    var result = null;
    if (isBack) { result = wrap_span(strip_keep_chars(content), "current-cloze"); }
    else { result = replace_content(content, contentHint, "current-cloze"); }

    return result;
  });
}
"""
