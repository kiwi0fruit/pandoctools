. "$pyprepPATH" "${env_path}"

prof=Default
. "$import" Args-Main

reader_args=(-f "$from" "${reader_args[@]}")
writer_args=(--standalone --self-contained -t "$to" "${writer_args[@]}")

cat-md stdin | \
pandoc "${reader_args[@]}" "${writer_args[@]}"
