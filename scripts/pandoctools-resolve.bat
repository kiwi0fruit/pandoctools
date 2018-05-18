:: Usage in Pandoctools profiles (for Meta-Default.yaml):
::   %set_resolve% x Meta-Default.yaml

:: Uses predefined absolute path variables:
::   %_core_config% (<...>\site-packages\pandoctools\bat)
::   %_user_config% (%APPDATA%\pandoc\pandoctools)

if exist "%_user_config%\%~2" (
    set %~1=%_user_config%\%~2
) else (
    set %~1=%_core_config%\%~2
)
