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

%set_resolve% _meta_prof "Meta-%prof%.yaml"
%set_resolve% _meta_ipynb_R "Meta-ipynb-R.yaml"
%set_resolve% _meta_ipynb "Meta-ipynb-py3.yaml"
%set_resolve% _templ_docx "Template-%prof%.docx"


if "%in_ext%"=="" (
    set from=markdown

) else if "%in_ext%"=="md" (
    set from=markdown

) else if "%in_ext%"=="py" (
    set from=markdown

) else (
    set "from=%in_ext%"
)


set "_jupymd=markdown-bracketed_spans-fenced_divs-link_attributes-simple_tables-multiline_tables-grid_tables-pipe_tables-fenced_code_attributes-markdown_in_html_blocks-table_captions-smart"
set stdin_plus=stdin "%_meta_prof%"
set "to=%out_ext%"

if        "%out_ext%"=="" (
    set to=markdown

) else if "%out_ext%"=="md" (
    set to=markdown

) else if "%out_ext_full:~-8%"==".r.ipynb" (
    set "to=%_jupymd%"
    set t=markdown
    set stdin_plus=%stdin_plus% "%_meta_ipynb_R%"

) else if "%out_ext%"=="ipynb" (
    set "to=%_jupymd%"
    set t=markdown
    set stdin_plus=%stdin_plus% "%_meta_ipynb%"

) else if "%out_ext%"=="docx" (
    set writer_args=%writer_args% --reference-doc="%_templ_docx%" -o "%output_file%"
)

if "%t%" == "" set "t=%to%"
