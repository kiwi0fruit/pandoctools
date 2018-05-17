# May use predefined variables:
#   ${core_config} (folder)
#   ${user_config} (folder)
#   ${in_ext} (input file extension like "md")
#   ${in_ext_full} (extended input file extension like "py.md" -
#                   everything starting first dot)
#   ${out_ext} (output file extension like "md" or ".r.ipynb")
#   ${out_ext_full} (extended output file extension like "r.ipynb")
#   ${input_file} (input file name with extension)
# Exports vars:
#   ${reader_args}
#   ${writer_args}
#   ${stdin_plus}
#   $to
#   $pipe
# May be useful:
#   scripts="$(which panfl)"
#   scripts="${scripts%/*}"
# or use predefined $scripts var (conda environment bin folder).


if   [ "${in_ext}" == "" ]; then
    _from=markdown

elif [ "${in_ext}" == "md" ]; then
    _from=markdown

else
    _from="${in_ext}"
fi
reader_args=(-f "${_from}")


_jupymd="markdown-bracketed_spans-fenced_divs-link_attributes-simple_tables-multiline_tables-grid_tables-pipe_tables-fenced_code_attributes-markdown_in_html_blocks-table_captions-smart"
_meta="$(source "$getpath" Meta-${meta_prof}.yaml)"
stdin_plus=("stdin" "${_meta}")
pipe="Default"
to=""

if   [ "${out_ext}" == "" ]; then
    _to=markdown

elif [ "${out_ext}" == "md" ]; then
    _to=markdown

elif [ "${out_ext_full: -7}" == "r.ipynb" ]; then
    _to="${_jupymd}"
    to=markdown
    stdin_plus=("stdin" "${_meta}" "$(source "$getpath" Meta-ipynb-R.yaml)")
    pipe="ipynb"

elif [ "${out_ext}" == "ipynb" ]; then
    _to="${_jupymd}"
    to=markdown
    stdin_plus=("stdin" "${_meta}" "$(source "$getpath" Meta-ipynb-py3.yaml)")
    pipe="ipynb"

else
    _to="${out_ext}"
fi

if [ "$to" == "" ]; then; to="${_to}"
writer_args=(-t "${_to}" --standalone --self-contained)
