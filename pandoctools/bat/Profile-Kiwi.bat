@echo off

%source% activate "%env_path%"

set meta_prof=Kiwi
%import% Args-Default

set sugartex=sugartex --kiwi
%import% Pipe-%pipe%

%source% deactivate
