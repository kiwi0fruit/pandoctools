@echo off

%source% activate "%env_path%"

set meta_prof=Kiwi
%import% Args-Default

set sugartex=sugartex --kiwi
set stdin_plus1=stdin
%import% Pipe-%pipe%

%source% deactivate
