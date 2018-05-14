@echo off
%import% CLI-Default
%call% activate-default
%import% Args-Default
set inputs=stdin "%core_config%\Meta-Kiwi.yaml"
%import% Pipe-Kiwi
%call% deactivate-default
