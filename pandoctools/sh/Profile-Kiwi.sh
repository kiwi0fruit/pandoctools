. "$source" activate "${env_path}"

meta_prof=Kiwi
. "$import" Args-Default

sugartex=(sugartex --kiwi)
stdin_plus1=(stdin)
. "$import" "Pipe-$pipe"

. "$source" deactivate
