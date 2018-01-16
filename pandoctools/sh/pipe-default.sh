# scripts="$(which pip)"
# scripts="${scripts%/*}"
# Or use predefined `scripts` that is defined in pandoctools:
# panfl -d "$scripts" sugartex == panfl --sys-path sugartex == sugartex
# panfl -d "$scripts" sugartex_kiwi == panfl --sys-path sugartex_kiwi == sugartex kiwi
cat-md "${inputs[@]}" | pre-knitty "${input_file}" | pre-sugartex | cat-md "${all_inputs[@]}" | pandoc "${reader_args[@]}" -t json | knitty "${input_file}" "${reader_args[@]}" "${writer_args[@]}" | sugartex | pandoc -f json "${writer_args[@]}"
