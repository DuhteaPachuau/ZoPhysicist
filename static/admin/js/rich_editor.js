(function () {
  function editableTextareas() {
    return document.querySelectorAll("#id_full_content, #id_question, #id_solution");
  }

  function run(command, value) {
    document.execCommand(command, false, value || null);
  }

  function insertBlock(html) {
    document.execCommand("insertHTML", false, html);
  }

  function createButton(label, title, action) {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = label;
    button.title = title;
    button.addEventListener("click", action);
    return button;
  }

  function init() {
    editableTextareas().forEach((textarea) => {
      if (!textarea || textarea.dataset.zpEditorReady === "true") return;
      textarea.dataset.zpEditorReady = "true";

      const shell = document.createElement("div");
      shell.className = "zp-editor-shell";

      const toolbar = document.createElement("div");
      toolbar.className = "zp-editor-toolbar";

      const editor = document.createElement("div");
      editor.className = "zp-editor-area";
      editor.contentEditable = "true";
      editor.innerHTML = textarea.value || "<h2>Section title</h2><p>Write your content here...</p>";

      const help = document.createElement("div");
      help.className = "zp-editor-help";
      help.textContent = "Use H2 and H3 for lesson sections. In lessons, those headings become the public Contents dropdown.";

      toolbar.append(
      createButton("H2", "Section heading used in Contents", () => run("formatBlock", "h2")),
      createButton("H3", "Subheading used in Contents", () => run("formatBlock", "h3")),
      createButton("P", "Paragraph", () => run("formatBlock", "p")),
      createButton("B", "Bold", () => run("bold")),
      createButton("I", "Italic", () => run("italic")),
      createButton("List", "Bulleted list", () => run("insertUnorderedList")),
      createButton("Link", "Insert link", () => {
        const url = window.prompt("Paste the link URL");
        if (url) run("createLink", url);
      }),
      createButton("Formula", "Insert centered formula block", () => insertBlock('<div class="formula">E = mc^2</div><p><br></p>')),
      createButton("Code", "Insert code block", () => insertBlock("<pre><code>write code or steps here</code></pre><p><br></p>")),
      createButton("Image", "Insert image by URL", () => {
        const url = window.prompt("Paste image URL");
        if (url) insertBlock('<img src="' + url.replaceAll('"', "&quot;") + '" alt="">');
      }),
      createButton("HTML", "Show saved HTML in textarea", () => {
        textarea.style.display = textarea.style.display === "none" ? "" : "none";
      })
    );

      shell.append(toolbar, editor, help);
      textarea.parentNode.insertBefore(shell, textarea);
      textarea.style.display = "none";

      function sync() {
        textarea.value = editor.innerHTML.trim();
      }

      editor.addEventListener("input", sync);
      textarea.form?.addEventListener("submit", sync);
    });
  }

  document.addEventListener("DOMContentLoaded", init);
})();
