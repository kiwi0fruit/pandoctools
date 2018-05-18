:: Usage in Pandoctools profiles (for Profile-Default.bat):
::   %import% Profile-Default

:: Uses predefined absolute path variables:
::   %_core_config% (<...>\site-packages\pandoctools\bat)
::   %_user_config% (%APPDATA%\pandoc\pandoctools)

if exist "%_user_config%\%~1.bat" (
    call "%_user_config%\%~1.bat"
) else (
    call "%_core_config%\%~1.bat"
)
