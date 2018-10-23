. "$pyprepPATH" "${env_path}"

prof=Default
. "$import" Args-Default

cat-md stdin | \
pandoc "${reader_args[@]}" "${writer_args[@]}"
