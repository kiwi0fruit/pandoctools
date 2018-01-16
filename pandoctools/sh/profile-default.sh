# conda sripts:
# . "$source" activate the_env_name
# . "$source" deactivate
# wrappers that use $conda_env and $env_path:
# . "$source" activate-default
# . "$source" deactivate-default
# . "$source" activate-pseudo
. "$import" defaults
. "$source" activate-default
. "$import" args-default
. "$import" pipe-default
. "$source" deactivate-default
