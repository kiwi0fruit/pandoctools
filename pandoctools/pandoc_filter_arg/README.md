# pandoc-filter-arg

* **pandoc-filter-arg** is a CLI interface that prints argument that is passed by Pandoc to it's filters.
* The first argument is Pandoc's `--to` / `-t` / `--write` / `-w` argument.
* Uses Pandoc's default if the first argument is absent or empty.

Usage example: `pandoc-filter-arg markdown-simple_tables` echoes `markdown`
