@echo off && %setUTF8%
%pyprepPATH% "%root_env%"
%source% activate "%env_path%" && %setUTF8%
set meta=Kiwi
%import% Args-Default
set "stex=--kiwi" && set "inputs=stdin"
%import% "Pipe-%pipe%"
%source% deactivate