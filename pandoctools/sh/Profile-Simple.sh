PATH="${env_path}/bin:$PATH"
meta=Default
. "$import" Args-Default
cat-md stdin | pandoc "${reader_args[@]}" "${writer_args[@]}"
