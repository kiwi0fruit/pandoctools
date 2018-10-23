# May use predefined variables:
#   $prof (profile name)
#   $resolve (echoes resolved path to a file.
#             Searches in $HOME/.pandoc/pandoctools
#             then in <...>/site-packages/pandoctools/sh folders)
#   ${in_ext} (input file extension like "md")
#   ${in_ext_full} (extended input file extension like "py.md" -
#                   everything starting first dot)
#   ${out_ext} (output file extension like "md")
#   ${out_ext_full} (extended output file extension like "r.ipynb")
#   ${input_file} (input file path with extension)
#   ${output_file} (output file path with extension)
#   $scripts (conda environment bin folder)
# Exports vars:
#   ${reader_args}
#   ${writer_args}
#   ${stdin_plus}
#   $to

out_ext_full=".${out_ext_full}"


if   [ "${in_ext}" == "" ]; then
    _from=markdown

elif [ "${in_ext}" == "md" ]; then
    _from=markdown

elif [ "${in_ext}" == "py" ]; then
    _from=markdown

else
    _from="${in_ext}"
fi
reader_args=(-f "${_from}")


_jupymd="markdown-bracketed_spans-fenced_divs-link_attributes-simple_tables-multiline_tables-grid_tables-pipe_tables-fenced_code_attributes-markdown_in_html_blocks-table_captions-smart"
stdin_plus=("stdin" "$(. "$resolve" Meta-$prof.yaml)")
to=""
_to="${out_ext}"
writer_args=(--standalone --self-contained)

if   [ "${out_ext}" == "" ]; then
    _to=markdown

elif [ "${out_ext}" == "md" ]; then
    _to=markdown

elif [ "${out_ext_full: -8}" == ".r.ipynb" ]; then
    _to="${_jupymd}"
    to=markdown
    stdin_plus=("${stdin_plus[@]}" "$(. "$resolve" Meta-ipynb-R.yaml)")

elif [ "${out_ext}" == "ipynb" ]; then
    _to="${_jupymd}"
    to=markdown
    stdin_plus=("${stdin_plus[@]}" "$(. "$resolve" Meta-ipynb-py3.yaml)")

elif [ "${out_ext}" == "docx" ]; then
    writer_args=("${writer_args[@]}" --reference-doc="$(. "$resolve" Template-$prof.docx)" -o "${output_file}")
fi

if [ "$to" == "" ]; then
    to="${_to}"
fi
writer_args=("${writer_args[@]}" -t "${_to}")
