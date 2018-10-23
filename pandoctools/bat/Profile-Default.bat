@echo off && %setUTF8%
%pyprepPATH% "%root_env%"
%source% activate "%env_path%" && %setUTF8%

set prof=Default
%import% Args-Default
set reader_args=%reader_args% -f "%from%"
set writer_args=%writer_args% --standalone --self-contained -t "%to%"

set pipe=Default
if "%out_ext%"=="ipynb" (
    set pipe=ipynb
)

set "sugartex=%t%"
set inputs=stdin
%import% "Pipe-%pipe%"

%source% deactivate
