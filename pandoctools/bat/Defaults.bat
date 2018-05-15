:: These settings work only with CLI Pandoctools usage.
:: They do not change Atom package behavior.
:: Uses predefined variable:
::   %GUI% (TRUE if in Atom package mode)
::   %conda_env% (predefined if in Atom package mode)
::   %env_path% (predefined if in Atom package mode)
::   %python_path% (predefined if in Atom package mode)

@echo off
chcp 65001 > NUL
set PYTHONIOENCODING=utf-8

if NOT "%GUI%"=="TRUE" (
    :: Define python settings here:
    set "conda_env="
    set "env_path="
    set "python_path="
)

if NOT "%python_path%"=="" (
    set PYTHONPATH=%python_path%
    set PATH=%python_path%;%python_path%\Scripts;%python_path%\Library\bin;%PATH%
)
