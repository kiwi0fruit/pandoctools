@echo off
set "script_dir=%~dp0"
REM   == <envroot>\Scripts\
set "mathjax=%script_dir:~0,-9%\Library\lib\mathjax\MathJax.js"
if exist "%mathjax%" (
    set "script=%script_dir%echo-mathjax-path"
    echo @echo %mathjax% > "%script%.bat"
    echo #!/bin/bash > "%script%"
    echo cygpath "%mathjax%" >> "%script%"
) else (
    echo Error: %mathjax% file was not found 1>&2
    exit 1
)
