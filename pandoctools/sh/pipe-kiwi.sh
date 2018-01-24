cat-md "${inputs[@]}" | \
pre-knitty "${input_file}" | \
pre-sugartex | \
cat-md "${all_inputs[@]}" | \
pandoc "${reader_args[@]}" -t json | \
knitty "${input_file}" "${reader_args[@]}" "${writer_args[@]}" | \
sugartex --kiwi | \
pandoc-crossref $t | \
pandoc -f json "${writer_args[@]}"
