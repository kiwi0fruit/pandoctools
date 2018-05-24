@echo off && %setUTF8%
%pyprepPATH% "%env_path%"
set prof=Default
%import% Args-Default
%r% cat-md stdin | ^
%r% pandoc %reader_args% %writer_args% --toc
