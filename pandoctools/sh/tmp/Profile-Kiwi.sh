. "$source" activate-default
. "$import" Args-Default.sh
inputs=("stdin" "${config}/Meta-Kiwi.yaml")
. "$import" Pipe-Kiwi.sh
. "$source" deactivate-default
