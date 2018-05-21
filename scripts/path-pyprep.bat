@echo off
set "_pypath=%~1"
if NOT "%_pypath%"=="" (
    set "PATH=%_pypath%;%_pypath%\Scripts;%_pypath%\Library\bin;%PATH%"
)
