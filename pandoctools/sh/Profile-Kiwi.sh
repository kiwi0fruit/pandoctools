. "$pyprepPATH" "${root_env}"
. "$source" activate "${env_path}"

prof=Kiwi
. "$import" Args-Default
pipe=Default
if [ "${out_ext}" == "ipynb" ]; then
    pipe=ipynb
fi

stex="--kiwi"
inputs=(stdin)
# writer_args=("${writer_args[@]}" --toc)
. "$import" "Pipe-$pipe"

. "$source" deactivate
