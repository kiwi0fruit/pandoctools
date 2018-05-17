# May use predefined variables:
#   ${core_config} (folder)
#   ${user_config} (folder)
#   ${in_ext} (input file extension like "md")
#   ${in_ext_full} (extended input file extension like "py.md" -
#                   everything starting first dot)
#   ${out_ext} (output file extension like "md" or ".r.ipynb")
#   ${out_ext_full} (extended output file extension like "r.ipynb")
#   ${input_file} (input file name with extension)
# May be useful:
#   scripts="$(which panfl)"
#   scripts="${scripts%/*}"
# or use predefined $scripts var (conda environment bin folder).


if   [ "${in_ext}" == "" ]; then
    from=markdown

elif [ "${in_ext}" == "md" ]; then
    from=markdown

else
    from="${in_ext}"
fi


jupymd="markdown-bracketed_spans-fenced_divs-link_attributes-simple_tables-multiline_tables-grid_tables-pipe_tables-fenced_code_attributes-markdown_in_html_blocks-table_captions-smart"
meta="${core_config}\Meta-${meta_prof}.yaml"
stdin_plus=""
t=""
pipe="Default"

if   [ "${out_ext}" == "" ]; then
    to=markdown

elif [ "${out_ext}" == "md" ]; then
    to=markdown

elif [ "${out_ext_full: -7}" == "r.ipynb" ]; then
    to="$jupymd"
    t=markdown
    stdin_plus=("stdin" "$meta" "${core_config}/Meta-ipynb-R.yaml")
    pipe="ipynb"

elif [ "${out_ext}" == "ipynb" ]; then
    to="$jupymd"
    t=markdown
    stdin_plus=("stdin" "$meta" "${core_config}/Meta-ipynb-py3.yaml")
    pipe="ipynb"

else
    to="${out_ext}"
fi

if [ "${stdin_plus}" == "" ]; then; stdin_plus=("stdin" "$meta")
if [ "$t" == "" ]; then; t="$to"


reader_args=(-f "${from}")
writer_args=(-t "${to}" --standalone --self-contained)
