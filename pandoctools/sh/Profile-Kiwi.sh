. "$pyprepPATH" "${root_env}"
. "$source" activate "${env_path}"

prof=Kiwi
. "$import" Args-Default

inputs=(stdin)
stdin_plus=(stdin "${metas[@]}")
reader_args=(-f "$from" "${reader_args[@]}")
writer_args=(--standalone --self-contained -t "$to" "${writer_args[@]}")
sugartex="--kiwi"

pipe=Default
if [ "${out_ext}" == "ipynb" ]; then
    pipe=ipynb
fi
. "$import" "Pipe-$pipe"

. "$source" deactivate
