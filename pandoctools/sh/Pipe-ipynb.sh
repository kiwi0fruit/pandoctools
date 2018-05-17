cat-md "${stdin_plus1[@]}" | \
pre-knitty "${input_file}" | \
pre-sugartex | \
cat-md "${stdin_plus2[@]}" | \
pandoc "${reader_args[@]}" -t json | \
knitty "${input_file}" "${reader_args[@]}" "${writer_args[@]}" --to-ipynb | \
"${sugartex[@]}" | \
pandoc-crossref "$to" | \
pandoc -f json "${writer_args[@]}" | \
knotedown --match=in --nomagic > "${input_file}.${out_ext_full}"

jupyter nbconvert --to notebook --execute "${input_file}.${out_ext_full}"
