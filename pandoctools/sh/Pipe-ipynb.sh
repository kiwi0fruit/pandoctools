cat-md "${inputs[@]}" | \
pre-knitty "${input_file}" | \
pre-sugartex | \
cat-md "${stdin_plus[@]}" | \
pandoc "${reader_args[@]}" -t json | \
knitty "${input_file}" "${reader_args[@]}" "${writer_args[@]}" --to-ipynb | \
sugartex "$stex" | \
pandoc-crossref "$to" | \
pandoc -f json "${writer_args[@]}" | \
knotedown --match=in --nomagic > "${output_file}"
jupyter nbconvert --to notebook --execute "${output_file}"
