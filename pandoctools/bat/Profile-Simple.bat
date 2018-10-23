@echo off && %setUTF8%
%pyprepPATH% "%env_path%"

set prof=Default
%import% Args-Default
set reader_args=%reader_args% -f "%from%"
set writer_args=%writer_args% --standalone --self-contained -t "%to%"

%r% cat-md stdin | ^
%r% pandoc %reader_args% %writer_args%
