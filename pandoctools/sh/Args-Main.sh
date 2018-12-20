# May use variables predefined in the profile:
#   $prof (profile name)

# May use variables predefined in pandoctools:
#   ${in_ext}    (input file extension like "md")
#   ${out_ext}    (output file extension like "md")
#   ${input_file}    (input file path with extension)
#   ${output_file}    (output file path with extension)
#   $from    (pandoc reader format + custom pandoctools formats)
#   $to    (pandoc writer format + custom pandoctools formats)

#   $source    (source bash script from PATH but not CWD)
#   $import    (try source bash script from pandoctools folder
#               in user data. Then source from pandoctools module)
#   $resolve    (echoes resolved path to a file. Searches in 
#                `$HOME/.pandoc/pandoctools` or `%APPDATA%\pandoc\pandoctools`
#                then in `<...>/site-packages/pandoctools/sh` folders)
#   $pyprepPATH    (prepend PATH with python environment)

#   $scripts    (conda? environment bin folder)
#   ${root_env}    (root conda? environment folder)
#   ${env_path}    (conda? environment folder)

# Exports vars:
#   $from    (pandoc reader format without custom formats)
#   $to    (pandoc writer format without custom formats)
#   $t    (argument for pandoc filters)
#   ${reader_args}    (pandoc reader args)
#   ${writer_args}    (pandoc writer args)
#   ${extra_reader_args}    (format specific part of the pandoc reader args)
#   ${extra_writer_args}    (format specific part of the pandoc writer args)

#   $inputs
#   $metadata    (profile metadata file)
#   ${extra_inputs}    (format specific part of the middle inputs -
#                       metadata, other files)
#   ${middle_inputs}   (inputs after preprocess filters and before pandoc)

#   ${nbconvert_args}
#   ${panfl_args}


extra_inputs=()
extra_reader_args=()
extra_writer_args=()


# deal with reader formats:
# ---------------------------
#   predefined $from is always lowercase
if   [ "${in_ext}" == "py" ]; then
    from=markdown
fi


# deal with writer formats:
# ---------------------------
_jupymd="markdown-bracketed_spans-fenced_divs-link_attributes-simple_tables-multiline_tables-grid_tables-pipe_tables-fenced_code_attributes-markdown_in_html_blocks-table_captions-smart"
_meta_ipynb_R="$(. "$resolve" Meta-ipynb-R.yaml)"
_meta_ipynb_py3="$(. "$resolve" Meta-ipynb-py3.yaml)"
_templ_docx="$(. "$resolve" Template-$prof.docx)"

#   predefined $to is always lowercase
#   note custom $to format: r.ipynb
if [ "$to" == "r.ipynb" ] && [ "${out_ext}" == "ipynb" ]; then
    to="${_jupymd}"
    extra_inputs=("${_meta_ipynb_R}" "${extra_inputs[@]}")

elif [ "${out_ext}" == "ipynb" ]; then
    to="${_jupymd}"
    extra_inputs=("${_meta_ipynb_py3}" "${extra_inputs[@]}")

elif [ "${out_ext}" == "docx" ]; then
    extra_writer_args=(--reference-doc "${_templ_docx}" -o "${output_file}" "${extra_writer_args[@]}")
fi


# set other defaults:
# ---------------------
reader_args=(-f "$from" "${extra_reader_args[@]}")
writer_args=(--standalone --self-contained -t "$to" "${extra_writer_args[@]}")
t="$(pandoc-filter-arg "${writer_args[@]}")"

inputs=(stdin)
metadata="$(. "$resolve" Meta-$prof.yaml)"
middle_inputs=(stdin "$metadata" "${extra_inputs[@]}")

nbconvert_args=(--to notebook --execute --stdin --stdout)
panfl_args=(-t "$t" sugartex)
