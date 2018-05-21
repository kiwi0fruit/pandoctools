@echo off && chcp 65001 > NUL
%pyprepPATH% "%root_env%"
%source% activate "%env_path%"
set meta=Default
%import% Args-Default
set "stex=%to%" && set "inputs=stdin"
%import% "Pipe-%pipe%"
%source% deactivate
