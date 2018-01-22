@echo off
:: May be useful:
:: %call% setvar scripts %run% where $PATH:panfl.exe
:: set scripts=%scripts:~0,-10%
:: (or use `scripts` var predefined in pandoctools.exe)

:: `panfl sugartex` = `sugartex`
:: `panfl sugartex_kiwi` = `sugartex kiwi`

%run% cat-md %inputs% | ^
%run% pre-knitty %input_file% | ^
%run% pre-sugartex | ^
%run% cat-md %all_inputs% | ^
%run% pandoc %reader_args% -t json | ^
%run% knitty %input_file% %reader_args% %writer_args% | ^
%run% sugartex | ^
%run% pandoc -f json %writer_args%
