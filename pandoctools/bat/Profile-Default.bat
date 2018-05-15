@echo off
:: Example conda sripts:
::   %call% activate the_env_name
::   %call% deactivate
:: Example wrappers that use predefined env settings and conda sripts:
::   %call% pdt-activate
::   %call% pdt-deactivate
::   %call% pdt-pseudo-activate

%import% Defaults
%call% pdt-activate
%import% Args-Default
%import% Pipe-Default
%call% pdt-deactivate
