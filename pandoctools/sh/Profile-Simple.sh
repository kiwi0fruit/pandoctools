. "$pyprepPATH" "${env_path}"

prof=Default
. "$import" Args-Default
reader_args=("${reader_args[@]}" -f "$from")
writer_args=("${writer_args[@]}" --standalone --self-contained -t "$to")

cat-md stdin | \
pandoc "${reader_args[@]}" "${writer_args[@]}"
