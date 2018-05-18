@echo off
:: Uses predefined variables:
::   %source%
::   %import%
::   %env_path%

%source% activate "%env_path%"

set meta_profile=Default
%import% Args-Default

set stex=%to%
set inputs=stdin
%import% Pipe-%pipe%

%source% deactivate
