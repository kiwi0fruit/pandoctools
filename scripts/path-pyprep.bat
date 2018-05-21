@echo off
if NOT "%~1"=="" (
    set PATH=%~1;%~1\Scripts;%~1\Library\bin;%PATH%
)
