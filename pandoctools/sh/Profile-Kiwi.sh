. "$pyprepPATH" "${root_env}"
. "$source" activate "${env_path}"

prof=Kiwi
. "$import" Args-Main

inputs=(stdin)
stdin_plus=(stdin "${metas[@]}")
meta_profile="${metas[0]}"
reader_args=(-f "$from" "${reader_args[@]}")
writer_args=(--standalone --self-contained -t "$to" "${writer_args[@]}")
sugartex="--kiwi"

pipe=Main
if [ "${out_ext}" == "ipynb" ]; then
    pipe=ipynb
fi
. "$import" "Pipe-$pipe"

. "$source" deactivate
