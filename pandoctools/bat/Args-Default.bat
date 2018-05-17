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
:: Exports vars:
::   %reader_args%
::   %writer_args%
::   %stdin_plus2%
::   %to%
::   %pipe%
:: May be useful:
::   %source% setvar scripts %r% where $PATH:panfl.exe
::   set scripts=%scripts:~0,-10%
:: or use predefined %scripts% var (conda environment Scripts folder).


if        "%in_ext%"=="" (
    set _from=markdown

) else if "%in_ext%"=="md" (
    set _from=markdown

) else (
    set _from=%in_ext%
)
set reader_args=-f "%_from%"


set _jupymd=markdown-bracketed_spans-fenced_divs-link_attributes-simple_tables-multiline_tables-grid_tables-pipe_tables-fenced_code_attributes-markdown_in_html_blocks-table_captions-smart
%set_resolve% _meta Meta-%meta_prof%.yaml
set stdin_plus2=stdin "%_meta%"
set pipe=Default
set "to="

if        "%out_ext%"=="" (
    set _to=markdown

) else if "%out_ext%"=="md" (
    set _to=markdown

) else if "%out_ext_full:~-7%"=="r.ipynb" (
    set _to=%_jupymd%
    set to=markdown
    set pipe=ipynb
    
    %set_resolve% _meta2 Meta-ipynb-R.yaml
    set stdin_plus2=stdin "%_meta%" "%_meta2%"

) else if "%out_ext%"=="ipynb" (
    set _to=%_jupymd%
    set to=markdown
    set pipe=ipynb

    %set_resolve% _meta2 Meta-ipynb-py3.yaml
    set stdin_plus2=stdin "%_meta%" "%_meta2%"

) else (
    set _to=%out_ext%
)

if "%to%" == "" set to=%_to%
set writer_args=-t "%_to%" --standalone --self-contained
