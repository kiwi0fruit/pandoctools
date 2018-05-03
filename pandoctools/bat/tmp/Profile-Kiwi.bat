@echo off
%call% activate-default
%import% Args-Default
set inputs=stdin "%config%\Meta-Kiwi.yaml"
%import% Pipe-Kiwi
%call% deactivate-default
