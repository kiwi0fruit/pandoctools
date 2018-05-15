# `panfl sugartex_panfl -t $t` = `sugartex`
# `panfl sugartex_kiwi -t $t` = `sugartex kiwi`

cat-md stdin | \
pre-knitty "${input_file}" | \
pre-sugartex | \
cat-md "${inputs[@]}" | \
pandoc "${reader_args[@]}" -t json | \
knitty "${input_file}" "${reader_args[@]}" "${writer_args[@]}" | \
sugartex "${to}" | \
pandoc-crossref "${to}" | \
pandoc -f json "${writer_args[@]}"
