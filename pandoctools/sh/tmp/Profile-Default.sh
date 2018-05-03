# conda sripts:
# . "$source" activate the_env_name
# . "$source" deactivate
# wrappers that use $conda_env and $env_path:
# . "$source" activate-default
# . "$source" deactivate-default
# . "$source" activate-pseudo
. "$source" activate-default
. "$import" Args-Default.sh
. "$import" Pipe-Default.sh
. "$source" deactivate-default
