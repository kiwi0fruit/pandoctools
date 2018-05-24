@echo off && %setUTF8%
%pyprepPATH% "%root_env%"
%source% activate "%env_path%" && %setUTF8%
set prof=Kiwi
%import% Args-Default
set "stex=--kiwi"
set "inputs=stdin"
set writer_args=%writer_args% --toc
%import% "Pipe-%pipe%"
%source% deactivate
