. "$pyprepPATH" "${root_env}"
. "$source" activate "${env_path}"

prof=Default
. "$import" Args-Main
# (see docs on available and used env vars there)

# Defaults preset or set in Args-Main can be overriden:
# -----------------------------------------------------
# from, to, t, reader_args, writer_args,
# inputs, meta_profile, metas, stdin_plus,
# nbconvert_args, panfl_args
# input_file, output_file

pipe=Main
if [ "${out_ext}" == "ipynb" ]; then
    pipe=ipynb
fi
. "$import" "Pipe-$pipe"

. "$source" deactivate
