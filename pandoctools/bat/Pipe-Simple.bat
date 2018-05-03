@echo off
%r% cat-md stdin | ^
%r% pandoc %reader_args% %writer_args%
