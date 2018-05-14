# Example conda sripts:
# . "$source" activate the_env_name
# . "$source" deactivate
# Example wrappers that use predefined env settings and conda sripts:
# . "$source" activate-default
# . "$source" deactivate-default
# . "$source" activate-pseudo
. "$import" CLI-Default
. "$source" activate-default
. "$import" Args-Default
. "$import" Pipe-Default
. "$source" deactivate-default
