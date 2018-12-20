# pandoc-filter-arg

**pandoc-filter-arg** is a CLI interface that prints argument that is passed by Pandoc to it's filters.

Usage example: `pandoc-filter-arg -t markdown-simple_tables` echoes `markdown`

```
Usage: pandoc-filter-arg [OPTIONS]

  CLI interface that prints argument that is passed by Pandoc to it's
  filters. Uses Pandoc's defaults. Ignores extra arguments.

Options:
  -o, --output TEXT           Pandoc writer option.
  -w, -t, --write, --to TEXT  Pandoc writer option.
  --help                      Show this message and exit.
```
