:: Usage in Pandoctools profiles (for Meta-Default.yaml):
::   %setpath% x  Meta-Default.yaml

:: Uses predefined absolute path variables:
::   %core_config% (<...>\site-packages\pandoctools\bat)
::   %user_config% (%APPDATA%\pandoc\pandoctools)

if exist "%user_config%\%~2.bat" (
    set %~1=%user_config%\%~2.bat
) else (
    set %~1=%core_config%\%~2.bat
)
