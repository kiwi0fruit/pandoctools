# Uses predefined variables:
#   $source
#   $import
#   ${env_path}

. "$source" activate "${env_path}"

meta_profile=Default
. "$import" Args-Default

stex="$to"
inputs=(stdin)
. "$import" "Pipe-$pipe"

. "$source" deactivate
