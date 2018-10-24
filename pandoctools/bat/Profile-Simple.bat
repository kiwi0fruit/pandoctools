@echo off && %setUTF8%
%pyprepPATH% "%env_path%"

set prof=Default
%import% Args-Main

set reader_args=-f "%from%" %reader_args%
set writer_args=--standalone --self-contained -t "%to%" %writer_args%

%r% cat-md stdin | ^
%r% pandoc %reader_args% %writer_args%
