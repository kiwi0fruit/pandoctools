# cat-md

**cat-md** is a simple CLI tool that concatenates input files or stdin input (joins them with double new lines) and prints to stdout. It can have `stdin` or `-` as one of it's inputs - in this case it reads from stdin.

Usage: `cat-md stdin metadata.yaml`

```
Usage: cat-md [OPTIONS] [INPUT_FILES]

  Joins markdown files with "\n\n" separator and writes
  to stdout. If one of the files is "stdin" or "-" then reads
  it from stdin (can use the same stdin text several times).
  If no markdown files provided then default is 'stdin'.

Options:
  --help   Show this message and exit.
```
