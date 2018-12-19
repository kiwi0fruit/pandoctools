export KNITTY=True

cat-md "${inputs[@]}" | \
pre-knitty "${input_file}" --yaml "${meta_profile}" | \
pre-sugartex | \
cat-md "${stdin_plus[@]}" | \
pandoc "${reader_args[@]}" -t json | \
knitty "${input_file}" "${reader_args[@]}" "${writer_args[@]}" --to-ipynb | \
panfl "${panfl_args[@]}" | \
pandoc-crossref "$t" | \
pandoc -f json "${writer_args[@]}" | \
knotedown --match=in --nomagic | \
jupyter nbconvert "${nbconvert_args[@]}"
