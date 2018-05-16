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


if   [ "${out_ext}" == "" ]; then
    to=markdown

elif [ "${out_ext_full: -2}" == "md" ]; then
    to=markdown

else
    to="${out_ext}"
fi


# stdin from previous operations + Meta-Default.yaml:
inputs=("stdin" "${core_config}/Meta-Default.yaml")
reader_args=(-f "${from}")
writer_args=(-t "${to}" --standalone --self-contained)
