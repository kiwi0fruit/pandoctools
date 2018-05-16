# Uses predefined variables:
#   $source
#   $import
#   ${env_path}

. "$source" activate "${env_path}"
. "$import" Args-Default
. "$import" Pipe-Default
. "$source" deactivate
