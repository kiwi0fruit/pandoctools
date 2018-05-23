. "$pyprepPATH" "${env_path}"
meta=Default
. "$import" Args-Default
cat-md stdin | pandoc "${reader_args[@]}" "${writer_args[@]}" --toc
