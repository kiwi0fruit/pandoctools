:: These settings work only with CLI Pandoctools usage.
:: They do not change Atom package behavior.
:: Uses predefined variable:
::   %GUI% (TRUE if in Atom package mode)

@echo off
chcp 65001 > NUL
set PYTHONIOENCODING=utf-8
if NOT "%GUI%"=="TRUE" (
    set "conda_env="
    set "env_path="
    set "python_path="
)
