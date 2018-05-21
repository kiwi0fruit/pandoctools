. "$pyprepPATH" "${root_env}"
. "$source" activate "${env_path}"
meta=Kiwi
. "$import" Args-Default
stex="--kiwi"; inputs=(stdin)
. "$import" "Pipe-$pipe"
. "$source" deactivate
