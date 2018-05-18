@echo off

set PATH=%env_path%;%env_path%\Scripts;%env_path%\Library\bin;%PATH%

set meta_profile=Default
%import% Args-Default

%r% cat-md stdin | ^
%r% pandoc %reader_args% %writer_args%
