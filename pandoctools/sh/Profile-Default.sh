# Uses predefined variables:
#   $source
#   $import
#   ${env_path}


. "$source" activate "${env_path}"

meta_prof=Default
. "$import" Args-Default

sugartex=(sugartex)
. "$import" "Pipe-$pipe"

. "$source" deactivate
