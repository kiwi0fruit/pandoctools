. "$source" activate "${env_path}"

meta_profile=Kiwi
. "$import" Args-Default

stex="--kiwi"
inputs=(stdin)
. "$import" "Pipe-$pipe"

. "$source" deactivate
