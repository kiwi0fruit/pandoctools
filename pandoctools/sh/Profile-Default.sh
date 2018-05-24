. "$pyprepPATH" "${root_env}"
. "$source" activate "${env_path}"
prof=Default
. "$import" Args-Default
stex="$to"
inputs=(stdin)
writer_args=("${writer_args[@]}" --toc)
. "$import" "Pipe-$pipe"
. "$source" deactivate
