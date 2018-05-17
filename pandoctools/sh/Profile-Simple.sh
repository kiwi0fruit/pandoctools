

PATH="${env_path}/bin:$PATH"

meta_prof=Default
. "$import" Args-Default

cat-md stdin | \
pandoc "${reader_args[@]}" "${writer_args[@]}"
