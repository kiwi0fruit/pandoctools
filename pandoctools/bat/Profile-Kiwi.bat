@echo off

%import% Defaults
%call% pdt-activate
%import% Args-Default
set inputs=stdin "%core_config%\Meta-Kiwi.yaml"
%import% Pipe-Kiwi
%call% pdt-deactivate
