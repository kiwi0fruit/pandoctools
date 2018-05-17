

cat-md stdin | \
pre-knitty "${input_file}" | \
pre-sugartex | \
cat-md "${stdin_plus[@]}" | \
pandoc "${reader_args[@]}" -t json | \
knitty "${input_file}" "${reader_args[@]}" "${writer_args[@]}" --to-ipynb | \
"${sugartex[@]}" | \
pandoc-crossref "$t" | \
pandoc -f json "${writer_args[@]}"

# `panfl sugartex_panfl -t $t` = `sugartex`
# `panfl sugartex_kiwi -t $t` = `sugartex --kiwi`
