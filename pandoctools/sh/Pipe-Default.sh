

cat-md stdin | \
pre-knitty "${input_file}" | \
pre-sugartex | \
cat-md "${stdin_plus[@]}" | \
pandoc "${reader_args[@]}" -t json | \
knitty "${input_file}" "${reader_args[@]}" "${writer_args[@]}" | \
"${sugartex[@]}" | \
pandoc-crossref "$to" | \
pandoc -f json "${writer_args[@]}"

# `panfl sugartex_panfl -to $t` = `sugartex`
# `panfl sugartex_kiwi -to $t` = `sugartex --kiwi`
