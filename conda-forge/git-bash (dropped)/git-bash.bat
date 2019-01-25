@set "_script_dir=%~dp0"
@set "_prefix=%_script_dir:~0,-22%"
@if "%_prefix%\etc\conda\activate.d\" == "_script_dir" set "PATH=%_prefix%\Library\git-bash\bin;%PATH%"
