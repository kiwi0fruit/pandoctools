# May be useful:
# scripts="$(which panfl)"
# scripts="${scripts%/*}"
# (or use `scripts` var predefined in pandoctools)

# `panfl sugartex_panfl` = `sugartex`
# `panfl sugartex_kiwi` = `sugartex kiwi`

cat-md "${inputs[@]}" | \
pre-knitty "${input_file}" | \
pre-sugartex | \
cat-md "${all_inputs[@]}" | \
pandoc "${reader_args[@]}" -t json | \
knitty "${input_file}" "${reader_args[@]}" "${writer_args[@]}" | \
sugartex $t | \
pandoc -f json "${writer_args[@]}"
