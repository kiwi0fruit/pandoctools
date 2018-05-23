@echo off && %setUTF8%
%pyprepPATH% "%root_env%"
%source% activate "%env_path%" && %setUTF8%
set meta=Default
%import% Args-Default
set "stex=%to%" && set "inputs=stdin"
set writer_args=%writer_args% --toc
%import% "Pipe-%pipe%"
%source% deactivate
