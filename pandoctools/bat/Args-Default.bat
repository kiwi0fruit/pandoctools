@echo off
:: May use predefined variables:
::   %core_config%
::   %user_config%
::   %in_ext%
::   %out_ext%
::   %input_file%
:: May be useful:
::   %call% setvar scripts %r% where $PATH:panfl.exe
::   set scripts=%scripts:~0,-10%
:: or use predefined %scripts% var (conda env Scripts folder).


if        "%in_ext%"=="" (
    set from=markdown

) else if "%in_ext%"=="md" (
    set from=markdown

) else (
    set from=%in_ext%
)


if        "%out_ext%"=="" (
    set to=markdown

) else if "%out_ext%"=="md" (
    set to=markdown

) else (
    set to=%out_ext%
)


:: stdin from previous operations + Meta-Default.yaml:
set inputs=stdin "%core_config%\Meta-Default.yaml"
set reader_args=-f "%from%"
set writer_args=-t "%to%" --standalone --self-contained
