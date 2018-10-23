. "$pyprepPATH" "${root_env}"
. "$source" activate "${env_path}"

prof=Default
. "$import" Args-Default
pipe=Default
if [ "${out_ext}" == "ipynb" ]; then
    pipe=ipynb
fi

stex="$to"
inputs=(stdin)
# writer_args=("${writer_args[@]}" --toc)
. "$import" "Pipe-$pipe"

. "$source" deactivate
