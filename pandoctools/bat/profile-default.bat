@echo off
:: conda sripts:
:: %call% activate the_env_name
:: %call% deactivate
:: wrappers that use %conda_env% and %env_path%:
:: %call% activate-default
:: %call% deactivate-default
:: %call% activate-pseudo
%import% defaults
%call% activate-default
%import% args-default
%import% pipe-default
%call% deactivate-default
