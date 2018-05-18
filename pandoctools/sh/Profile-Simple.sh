PATH="${env_path}/bin:$PATH"

meta_profile=Default
. "$import" Args-Default

cat-md stdin | \
pandoc "${reader_args[@]}" "${writer_args[@]}"
