@echo off

%source% activate "%env_path%"

set meta_profile=Kiwi
%import% Args-Default

set stex=--kiwi
set inputs=stdin
%import% Pipe-%pipe%

%source% deactivate
