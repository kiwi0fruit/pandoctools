. "$pyprepPATH" "${root_env}"
. "$source" activate "${env_path}"

prof=Default
. "$import" Args-Main
# (see docs on available and used env vars there)

inputs=(stdin)
stdin_plus=(stdin "${metas[@]}")
meta_profile = "${metas[0]}"
reader_args=(-f "$from" "${reader_args[@]}")
writer_args=(--standalone --self-contained -t "$to" "${writer_args[@]}")
sugartex="$t"

pipe=Main
if [ "${out_ext}" == "ipynb" ]; then
    pipe=ipynb
fi
. "$import" "Pipe-$pipe"

. "$source" deactivate
