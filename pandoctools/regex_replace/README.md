# regex-replace

```
Usage: regex-replace [OPTIONS]

  Reads from stdin. Writes to stdout:

  re.sub(pattern, repl_template.format(*repls), stdin, flags=re.DOTALL)

  Where repls is a List[str] got from multiple options: either --string
  directly or read from --filepath. Like: -s xxx -s yyy

Options:
  -p, --pattern TEXT        [required]
  -t, --repl-template TEXT
  -s, --string TEXT
  -f, --filepath TEXT
  --help                    Show this message and exit.
```

Usage example:

```bash
regex-replace -p "<head>" -t "<head><style>{}</style>" -f "$tmpdir/fonts.css"
```
