. "$pyprepPATH" "${root_env}"
. "$source" activate "${env_path}"

prof=Default
. "$import" Args-Main
# (see docs on available and used env vars there)

# ---- Can be overriden: ----
# inputs=(stdin)
# stdin_plus=(stdin "${metas[@]}")
# meta_profile="${meta_profile}"
# reader_args=(-f "$from" "${reader_args[@]}")
# writer_args=(--standalone --self-contained -t "$to" "${writer_args[@]}")
# nbconvert_args=(--to notebook --execute --stdin --stdout)
# panfl_args=(-t "$t" sugartex)

pipe=Main
if [ "${out_ext}" == "ipynb" ]; then
    pipe=ipynb
fi
. "$import" "Pipe-$pipe"

. "$source" deactivate
