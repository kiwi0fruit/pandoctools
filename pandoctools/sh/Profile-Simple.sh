. "$pyprepPATH" "${env_path}"

prof=Default
. "$import" Args-Main

cat-md stdin | pandoc "${reader_args[@]}" "${writer_args[@]}"
