Update instructions:

1. `_github_markdown.css`: `github-markdown.css` at [sindresorhus/github-markdown-css](https://github.com/sindresorhus/github-markdown-css)
2. `Default.html`:
    * `pandoc --print-default-template=html > Default.html` then transfer `<!-- NEW -->` commented lines from old [Default.html](./Default.html) to new one.
    * `pandoc --print-default-data-file=templates/styles.html > styles.html` then replace `$styles.html()$` with it.
3. `Default.docx` and `Kiwi.docx`: TODO
