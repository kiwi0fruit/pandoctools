:: Usage in Pandoctools profiles (for Profile-Default.bat):
::   %import% Profile-Default

:: Uses predefined absolute path variables:
::   %core_config% (<...>\site-packages\pandoctools\bat)
::   %user_config% (%APPDATA%\pandoc\pandoctools)

if exist "%user_config%\%~1.bat" (
    call "%user_config%\%~1.bat"
) else (
    call "%core_config%\%~1.bat"
)
