. "$import" CLI-Default
. "$source" activate-default
. "$import" Args-Default
inputs=("stdin" "${core_config}/Meta-Kiwi.yaml")
. "$import" Pipe-Kiwi
. "$source" deactivate-default
