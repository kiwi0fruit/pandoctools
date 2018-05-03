@echo off
:: conda sripts:
:: %call% activate the_env_name
:: %call% deactivate
:: wrappers that use %conda_env% and %env_path%:
:: %call% activate-default
:: %call% deactivate-default
:: %call% activate-pseudo
%call% activate-default
%import% Args-Default
%import% Pipe-Default
%call% deactivate-default
