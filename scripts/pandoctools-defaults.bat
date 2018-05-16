:: Imports Defaults and changes PATH
:: Uses predefined variable:
::   %import%
::   %env_path% (always autocalculated by python app)
::   %python_root_auto% (autocalculated by python app if python/envs/env_name else "")
::   %python_root% (predefined if differs from autocalculated)

@echo off
chcp 65001 > NUL
set PYTHONIOENCODING=utf-8

%import% Defaults

if "%python_root%"=="" (
    set python_root=%python_root_auto%
)

if NOT "%python_root%"=="" (
    set PYTHONPATH=%python_root%
    set PATH=%python_root%;%python_root%\Scripts;%python_root%\Library\bin;%PATH%
)
