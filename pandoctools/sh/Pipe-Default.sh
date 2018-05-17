cat-md "${stdin_plus1[@]}" | \
pre-knitty "${input_file}" | \
pre-sugartex | \
cat-md "${stdin_plus2[@]}" | \
pandoc "${reader_args[@]}" -t json | \
knitty "${input_file}" "${reader_args[@]}" "${writer_args[@]}" | \
"${sugartex[@]}" | \
pandoc-crossref "$to" | \
pandoc -f json "${writer_args[@]}"

# `panfl sugartex_panfl -t $to` = `sugartex`
# `panfl sugartex_kiwi -t $to` = `sugartex --kiwi`
