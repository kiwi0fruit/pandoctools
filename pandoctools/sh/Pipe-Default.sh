# `panfl sugartex_panfl -t $to` = `sugartex`
# `panfl sugartex_kiwi -t $to` = `sugartex --kiwi`

cat-md stdin | \
pre-knitty "${input_file}" | \
pre-sugartex | \
cat-md "${inputs[@]}" | \
pandoc "${reader_args[@]}" -t json | \
knitty "${input_file}" "${reader_args[@]}" "${writer_args[@]}" | \
sugartex | \
pandoc-crossref "${to}" | \
pandoc -f json "${writer_args[@]}"
