:: Usage in Pandoctools profiles (for Meta-Default.yaml):
::   %set_resolve% x Meta-Default.yaml

:: Uses predefined absolute path variables:
::   %core_config% (<...>\site-packages\pandoctools\bat)
::   %user_config% (%APPDATA%\pandoc\pandoctools)

if exist "%user_config%\%~2" (
    set %~1=%user_config%\%~2
) else (
    set %~1=%core_config%\%~2
)
