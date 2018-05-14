:: setvar varname cmd
:: Set VARNAME to the output of CMD
:: Triple escape pipes, eg:
:: setvar x  dir c:\ ^^^| sort
:: https://stackoverflow.com/a/25954264/9071377
:: -----------------------------

@echo off
SETLOCAL

:: Get command from argument
for /F "tokens=1,*" %%a in ("%*") do set cmd=%%b

:: Get output and set var
for /F "usebackq delims=" %%a in (`%cmd%`) do (
     ENDLOCAL
     set %1=%%a
)

:: Show results
::SETLOCAL EnableDelayedExpansion
::echo %1=!%1!
