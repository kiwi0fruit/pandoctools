cat-md "${inputs[@]}" | \
pandoc "${reader_args[@]}" "${writer_args[@]}"
