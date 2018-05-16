:: Imports Defaults and changes PATH
:: Uses predefined variable:
::   %import%
::   %env_path% (always autocalculated by python app)
::   %root_env_auto% (autocalculated by python app if python/envs/env_name else "")
::   %root_env% (predefined if differs from autocalculated)

@echo off
chcp 65001 > NUL
set PYTHONIOENCODING=utf-8

set "root_env="
if exist "%user_config%\Defaults.ini" (
    set defs=%user_config%\Defaults.ini
) else (
    set defs=%core_config%\Defaults.ini
)
for /f "delims=" %%x in ("%defs%") do (
    set "%%x"
)

if "%root_env%"=="" (
    set root_env=%root_env_auto%
)

if NOT "%root_env%"=="" (
    set PYTHONPATH=%root_env%
    set PATH=%root_env%;%root_env%\Scripts;%root_env%\Library\bin;%PATH%
)
