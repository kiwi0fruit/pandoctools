@echo off
%source% activate "%env_path%"
%import% Args-Default
set inputs=stdin "%core_config%\Meta-Kiwi.yaml"
%import% Pipe-Kiwi
%source% deactivate
