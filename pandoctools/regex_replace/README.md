# regex-replace

```
Usage: regex-replace [OPTIONS]

  Reads from stdin. Writes to stdout:

  re.sub(pattern, repl_template.format(*strings), stdin, flags=re.DOTALL)

  Where strings is a List[str] got from multiple --filepath options. Like:
  -f xx -f yy (if no filepaths were provided then no formatting is
  attemtpted).

Options:
  -p, --pattern TEXT        [required]
  -t, --repl-template TEXT
  -f, --filepath TEXT
  --help                    Show this message and exit.
```

Usage example:

```bash
regex-replace -p "<head>" -t "<head><style>{}</style>" -f "$tmpdir/fonts.css"
```
