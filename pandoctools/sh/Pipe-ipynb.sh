export KNITTY=True

cat-md "${inputs[@]}" | \
pre-knitty "${input_file}" --yaml "$metadata" | \
pre-sugartex | \
cat-md "${middle_inputs[@]}" | \
pandoc "${reader_args[@]}" -t json | \
knitty "${input_file}" "${reader_args[@]}" "${writer_args[@]}" --to-ipynb | \
panfl "${panfl_args[@]}" | \
pandoc-crossref "$t" | \
pandoc -f json "${writer_args[@]}" | \
post-knitty --to-ipynb | \
jupyter nbconvert "${nbconvert_args[@]}"
