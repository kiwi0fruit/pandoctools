@echo off && %setUTF8%
%pyprepPATH% "%root_env%"
%source% activate "%env_path%" && %setUTF8%

set prof=Kiwi
%import% Args-Main

set inputs=stdin
set stdin_plus=stdin %metas%
set reader_args=-f "%from%" %reader_args%
set writer_args=--standalone --self-contained -t "%to%" %writer_args%
set "sugartex=--kiwi"

set pipe=Main
if "%out_ext%"=="ipynb" (
    set pipe=ipynb
)
%import% "Pipe-%pipe%"

%source% deactivate
