:: Usage in Pandoctools profiles:
::   %r% program
::   (%r% contains absolute path)
:: General usage:
::   call path-run program

:: Runs program ONLY from %PATH%
:: In order to run program from CWD use: .\program

@echo off
set "full_path="
set "all_but_first="

SETLOCAL
for /F "usebackq delims=" %%a in (`^^^"%WINDIR%\System32\where.exe^^^" $PATH:%1`) do (
    ENDLOCAL
    set "full_path=%%a"
    GOTO :break1
)

:break1
for /F "tokens=1,*" %%a in ("%*") do set "all_but_first=%%b"

"%full_path%" %all_but_first%
