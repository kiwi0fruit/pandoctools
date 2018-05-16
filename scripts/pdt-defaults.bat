:: Imports CLI-Defaults and changes PATH
:: %pdt_GUI% FALSE settings work only with CLI Pandoctools usage.
:: They do not change Atom package behavior.
:: Uses predefined variable:
::   %import%
::   %pdt_GUI% (TRUE if in Atom package mode)
::   %conda_env% (predefined if in Atom package mode)
::   %env_path% (predefined if in Atom package mode)
::   %python_root% (predefined if in Atom package mode)

@echo off
chcp 65001 > NUL
set PYTHONIOENCODING=utf-8

if NOT "%pdt_GUI%"=="TRUE" (
    %import% CLI-Defaults
)

if NOT "%python_root%"=="" (
    set PYTHONPATH=%python_root%
    set PATH=%python_root%;%python_root%\Scripts;%python_root%\Library\bin;%PATH%
)
