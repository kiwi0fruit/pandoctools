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


if        "%out_ext%"=="" (
    set to=markdown

) else if "%out_ext_full:~-2%"=="md" (
    set to=markdown

) else (
    set to=%out_ext%
)


:: stdin from previous operations + Meta-Default.yaml:
set inputs=stdin "%core_config%\Meta-Default.yaml"
set reader_args=-f "%from%"
set writer_args=-t "%to%" --standalone --self-contained
