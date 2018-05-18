. "$source" activate "${env_path}"
meta=Default
. "$import" Args-Default
stex="$to"; inputs=(stdin)
. "$import" "Pipe-$pipe"
. "$source" deactivate
