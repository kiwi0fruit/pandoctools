. "$pyprepPATH" "${root_env}"
. "$source" activate "${env_path}"

prof=Default
. "$import" Args-Main
# (see docs on available and used env vars there)

# Defaults preset or set in Args-Main.sh can be overriden:
# -----------------------------------------------------
# t, reader_args, writer_args,
# inputs, metadata, middle_inputs,
# nbconvert_args, panfl_args
# input_file, output_file

pipe=Main
if [ "${out_ext}" == "ipynb" ]; then
    pipe=ipynb
fi
. "$import" "Pipe-$pipe"

. "$source" deactivate
