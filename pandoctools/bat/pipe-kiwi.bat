@echo off
%run% cat-md %inputs% | %run% pre-knitty %input_file% | %run% pre-sugartex | %run% cat-md %all_inputs% | %run% pandoc %reader_args% -t json | %run% knitty %input_file% %reader_args% %writer_args% | %run% sugartex kiwi | %run% pandoc -f json %writer_args%
