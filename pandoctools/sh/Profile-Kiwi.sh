

. "$source" activate "${env_path}"

meta_prof=Kiwi
. "$import" Args-Default

sugartex=(sugartex --kiwi)
. "$import" "Pipe-$pipe"

. "$source" deactivate
