. "$pyprepPATH" "${root_env}"
. "$source" activate "${env_path}"
meta=Kiwi
. "$import" Args-Default
stex="--kiwi"; inputs=(stdin)
writer_args=("${writer_args[@]}" --toc)
. "$import" "Pipe-$pipe"
. "$source" deactivate
