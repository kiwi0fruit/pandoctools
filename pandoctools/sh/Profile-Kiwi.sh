. "$pyprepPATH" "${root_env}"
. "$source" activate "${env_path}"

prof=Kiwi
. "$import" Args-Main

panfl_args=(-t "$t" sugartex.kiwi)

pipe=Main
if [ "${out_ext}" == "ipynb" ]; then
    pipe=ipynb
fi
. "$import" "Pipe-$pipe"

. "$source" deactivate
