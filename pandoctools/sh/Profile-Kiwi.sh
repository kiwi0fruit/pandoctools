. "$import" Defaults
. "$source" pdt-activate
. "$import" Args-Default
inputs=("stdin" "${core_config}/Meta-Kiwi.yaml")
. "$import" Pipe-Kiwi
. "$source" pdt-deactivate
