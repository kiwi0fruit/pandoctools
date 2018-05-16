# Example conda sripts:
# . "$source" activate the_env_name
# . "$source" deactivate
# Example wrappers that use predefined env settings and conda sripts:
# . "$source" pdt-activate
# . "$source" pdt-deactivate
# . "$source" pdt-pseudo-activate

. "$source" pdt-defaults
. "$source" pdt-conda-activate
. "$import" Args-Default
. "$import" Pipe-Default
. "$source" pdt-conda-deactivate
