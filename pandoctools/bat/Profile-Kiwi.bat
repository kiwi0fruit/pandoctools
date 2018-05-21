@echo off && chcp 65001 > NUL
%pyprepPATH% "%root_env%"
%source% activate "%env_path%"
set meta=Kiwi
%import% Args-Default
set "stex=--kiwi" && set "inputs=stdin"
%import% Pipe-%pipe%
%source% deactivate
