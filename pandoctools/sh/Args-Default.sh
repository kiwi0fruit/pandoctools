# May use variables predefined in the profile:
#   $prof (profile name)

# May use variables predefined in pandoctools:
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

#   $source (source bash script from PATH but not CWD)
#   $import (try source bash script from pandoctools folder
#            in user data. Then source from pandoctools module)
#   $pyprepPATH (prepend PATH with python environment)
#   ${root_env}
#   ${env_path}

# Exports vars:
#   $from
#   $to
#   $t (argument for filters)
#   ${reader_args}
#   ${writer_args}
#   $metas (additional metadata files)


out_ext_full=".${out_ext_full}"
writer_args=()
reader_args=()
t=""

_meta_prof="$(. "$resolve" Meta-$prof.yaml)"
_meta_ipynb_R="$(. "$resolve" Meta-ipynb-R.yaml)"
_meta_ipynb="$(. "$resolve" Meta-ipynb-py3.yaml)"
_templ_docx="$(. "$resolve" Template-$prof.docx)"


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
metas=("${_meta_prof}")
to="${out_ext}"

if   [ "${out_ext}" == "" ]; then
    to=markdown

elif [ "${out_ext}" == "md" ]; then
    to=markdown

elif [ "${out_ext_full: -8}" == ".r.ipynb" ]; then
    to="${_jupymd}"
    t=markdown
    metas=("${metas[@]}" "${_meta_ipynb_R}")

elif [ "${out_ext}" == "ipynb" ]; then
    to="${_jupymd}"
    t=markdown
    metas=("${metas[@]}" "${_meta_ipynb}")

elif [ "${out_ext}" == "docx" ]; then
    writer_args=(--reference-doc="${_templ_docx}" -o "${output_file}" "${writer_args[@]}")
fi

if [ "$t" == "" ]; then
    t="$to"
fi
