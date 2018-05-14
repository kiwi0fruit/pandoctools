@echo off
:: Example conda sripts:
::   %call% activate the_env_name
::   %call% deactivate
:: Example wrappers that use predefined env settings and conda sripts:
::   %call% activate-default
::   %call% deactivate-default
::   %call% activate-pseudo
%import% CLI-Default
%call% activate-default
%import% Args-Default
%import% Pipe-Default
%call% deactivate-default
