#!/bin/sh
# This script imitates work of the Atom Pandoctools
# package that converts "${name}.md" file to ".md.md".


# Taken from Atom Pandoctools package settings: 
python_path="${LOCALAPPDATA}/Miniconda"
conda_env="env_name"
profile="profile-default"
out_ext="md"


# Taken from current opened file:
name="$(basename "$BASH_SOURCE")"; name="${name%.*}.md"


# Derive Pandoctools module directory path:
pypath="${python_path}"
if [ "${pypath}" == "" ] && [ "${PYTHONPATH}" != "" ]; then
    pypath="${PYTHONPATH}"
fi
if [ "${pypath}" != "" ]; then
    if [ "${conda_env}" != "" ]; then
        pypath="${pypath}/envs/${conda_env}"
    fi
    pandoctools_dir="${pypath}/Lib/site-packages/pandoctools"
else
    pandoctools_dir="$(pandoctools-dir)"
fi


# pandoctools:
# ------------------------
# stdin: input file source
# arguments:
#   $1: profile script
#   $2: input file path + ".ext" (output extension)
#   $3: conda environment name
#       "" is a special case when activate/deactivate scripts are not called
#   $4: python path (optional)
# stdout: converted source
# example: source pandoctools profile input.md.md "" "/c/python"
cat "${name}" | source "${pandoctools_dir}/bash/pandoctools" "${profile}" "${name}.${out_ext}" "${conda_env}" "${python_path}" > "${name}.${out_ext}"
