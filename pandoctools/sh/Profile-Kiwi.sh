. "$source" pandoctools-defaults
. "$source" activate "${env_path}"
. "$import" Args-Default
inputs=("stdin" "${core_config}/Meta-Kiwi.yaml")
. "$import" Pipe-Kiwi
. "$source" deactivate
