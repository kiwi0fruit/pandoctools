@echo off
set "_script_dir=%~dp0"
REM <pyroot>\Scripts\
set "_mathjax=%_script_dir:~0,-9%\Library\lib\mathjax\MathJax.js"
set "_script_dir="
if exist "%_mathjax%" (
    echo %_mathjax%
    set "_mathjax="
) else (
    echo "Error: file '%_mathjax%' was not found." 1>&2
    set "_mathjax="
    exit 1
)
