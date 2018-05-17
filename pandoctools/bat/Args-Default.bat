@echo off
:: May use predefined variables:
::   %core_config% (folder)
::   %user_config% (folder)
::   %in_ext% (input file extension like "md")
::   %in_ext_full% (extended input file extension like "py.md" -
::                  everything after first dot)
::   %out_ext% (output file extension like "md")
::   %out_ext_full% (extended output file extension like "r.ipynb")
::   %input_file% (input file name with extension)
:: May be useful:
::   %source% setvar scripts %r% where $PATH:panfl.exe
::   set scripts=%scripts:~0,-10%
:: or use predefined %scripts% var (conda environment Scripts folder).


if        "%in_ext%"=="" (
    set from=markdown

) else if "%in_ext%"=="md" (
    set from=markdown

) else (
    set from=%in_ext%
)


set jupymd=markdown-bracketed_spans-fenced_divs-link_attributes-simple_tables-multiline_tables-grid_tables-pipe_tables-fenced_code_attributes-markdown_in_html_blocks-table_captions-smart
set meta=%core_config%\Meta-%meta_prof%.yaml
set "stdin_plus="
set "t="
set pipe=Default

if        "%out_ext%"=="" (
    set to=markdown

) else if "%out_ext%"=="md" (
    set to=markdown

) else if "%out_ext_full:~-7%"=="r.ipynb" (
    set to=%jupymd%
    set t=markdown
    set stdin_plus=stdin "%meta%" "%core_config%\Meta-ipynb-R.yaml"
    set pipe=ipynb

) else if "%out_ext%"=="ipynb" (
    set to=%jupymd%
    set t=markdown
    set stdin_plus=stdin "%meta%" "%core_config%\Meta-ipynb-py3.yaml"
    set pipe=ipynb

) else (
    set to=%out_ext%
)

if "%stdin_plus%" == "" set stdin_plus=stdin "%meta%"
if "%t%" == "" set t=%to%


set reader_args=-f "%from%"
set writer_args=-t "%to%" --standalone --self-contained
