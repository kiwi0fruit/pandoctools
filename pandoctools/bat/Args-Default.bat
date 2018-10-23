@echo off
:: May use predefined variables:
::   %prof% (profile name)
::   %set_resolve% (sets var to a resolved path to a file.
::                  Searches in %APPDATA%\pandoc\pandoctools
::                  then in <...>\site-packages\pandoctools\bat folders)
::   %in_ext% (input file extension like "md")
::   %in_ext_full% (extended input file extension like "py.md" -
::                  everything after first dot)
::   %out_ext% (output file extension like "md")
::   %out_ext_full% (extended output file extension like "r.ipynb")
::   %input_file% (input file path with extension)
::   %output_file% (output file path with extension)
::   %scripts% (conda environment Scripts folder).
:: Exports vars:
::   %from%
::   %to%
::   %t% (argument for filters)
::   %reader_args%
::   %writer_args%
::   %stdin_plus%
:: May be useful:
::   %source% setvar v echo hello

set "out_ext_full=.%out_ext_full%"
set "reader_args= "
set "writer_args= "
set "t="


if "%in_ext%"=="" (
    set from=markdown

) else if "%in_ext%"=="md" (
    set from=markdown

) else if "%in_ext%"=="md" (
    set from=markdown

) else (
    set "from=%in_ext%"
)


set "_jupymd=markdown-bracketed_spans-fenced_divs-link_attributes-simple_tables-multiline_tables-grid_tables-pipe_tables-fenced_code_attributes-markdown_in_html_blocks-table_captions-smart"
%set_resolve% _meta "Meta-%prof%.yaml"
set stdin_plus=stdin "%_meta%"
set "to=%out_ext%"

if        "%out_ext%"=="" (
    set to=markdown

) else if "%out_ext%"=="md" (
    set to=markdown

) else if "%out_ext_full:~-8%"==".r.ipynb" (
    set "to=%_jupymd%"
    set t=markdown
    %set_resolve% _meta Meta-ipynb-R.yaml
    set stdin_plus=%stdin_plus% "%_meta%"

) else if "%out_ext%"=="ipynb" (
    set "to=%_jupymd%"
    set t=markdown
    %set_resolve% _meta Meta-ipynb-py3.yaml
    set stdin_plus=%stdin_plus% "%_meta%"

) else if "%out_ext%"=="docx" (
    %set_resolve% _temp "Template-%prof%.docx"
    set writer_args=%writer_args% --reference-doc="%_temp%" -o "%output_file%"
)

if "%t%" == "" set "t=%to%"
