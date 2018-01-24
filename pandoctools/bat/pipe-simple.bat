@echo off
%r% cat-md %inputs% | ^
%r% pandoc %reader_args% %writer_args%
