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
#   $from
#   $to
#   $t (argument for filters)
#   ${reader_args}
#   ${writer_args}
#   ${stdin_plus}

out_ext_full=".${out_ext_full}"
writer_args=()
reader_args=()
t=""


if   [ "${in_ext}" == "" ]; then
    from=markdown

elif [ "${in_ext}" == "md" ]; then
    from=markdown

elif [ "${in_ext}" == "py" ]; then
    from=markdown

else
    from="${in_ext}"
fi


_jupymd="markdown-bracketed_spans-fenced_divs-link_attributes-simple_tables-multiline_tables-grid_tables-pipe_tables-fenced_code_attributes-markdown_in_html_blocks-table_captions-smart"
stdin_plus=("stdin" "$(. "$resolve" Meta-$prof.yaml)")
to="${out_ext}"

if   [ "${out_ext}" == "" ]; then
    to=markdown

elif [ "${out_ext}" == "md" ]; then
    to=markdown

elif [ "${out_ext_full: -8}" == ".r.ipynb" ]; then
    to="${_jupymd}"
    t=markdown
    stdin_plus=("${stdin_plus[@]}" "$(. "$resolve" Meta-ipynb-R.yaml)")

elif [ "${out_ext}" == "ipynb" ]; then
    to="${_jupymd}"
    t=markdown
    stdin_plus=("${stdin_plus[@]}" "$(. "$resolve" Meta-ipynb-py3.yaml)")

elif [ "${out_ext}" == "docx" ]; then
    writer_args=("${writer_args[@]}" --reference-doc="$(. "$resolve" Template-$prof.docx)" -o "${output_file}")
fi

if [ "$t" == "" ]; then
    t="$to"
fi
