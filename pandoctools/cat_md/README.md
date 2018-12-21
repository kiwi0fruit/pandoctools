# cat-md

**cat-md** is a simple CLI tool that concatenates input files or stdin input (joins them with double new lines) and prints to stdout. It can have `stdin` as one of it's inputs - in this case it reads from stdin.

Usage: `cat-md stdin metadata.yaml`

```
cat-md CLI joins markdown files with "\n\n" separator and writes
to stdout. If one of the files is "stdin" then reads it from stdin
(can use the same stdin text several times).
Also replaces all "\r\n" with "\n" on Unix.

OPTIONS:

--keep-cr    doesn't replace "\r" (carriage return)
--help       shows this message and exits
```
