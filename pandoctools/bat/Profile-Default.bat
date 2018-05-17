@echo off
:: Uses predefined variables:
::   %source%
::   %import%
::   %env_path%

%source% activate "%env_path%"

set meta_prof=Default
%import% Args-Default

set sugartex=sugartex
set stdin_plus1=stdin
%import% Pipe-%pipe%

%source% deactivate
