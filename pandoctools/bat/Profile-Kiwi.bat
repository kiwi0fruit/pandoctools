@echo off

%source% pdt-defaults
%source% pdt-conda-activate
%import% Args-Default
set inputs=stdin "%core_config%\Meta-Kiwi.yaml"
%import% Pipe-Kiwi
%source% pdt-conda-deactivate
