. "$pyprepPATH" "${root_env}"
. "$source" activate "${env_path}"

prof=Kiwi
. "$import" Args-Default
reader_args=("${reader_args[@]}" -f "$from")
writer_args=("${writer_args[@]}" --standalone --self-contained -t "$to")

pipe=Default
if [ "${out_ext}" == "ipynb" ]; then
    pipe=ipynb
fi

sugartex="--kiwi"
inputs=(stdin)
. "$import" "Pipe-$pipe"

. "$source" deactivate
