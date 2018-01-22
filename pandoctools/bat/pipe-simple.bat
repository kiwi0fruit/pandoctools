@echo off
%run% cat-md %inputs% | ^
%run% pandoc %reader_args% %writer_args%
