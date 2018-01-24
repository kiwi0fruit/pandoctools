@echo off
:: May be useful:
:: %call% setvar scripts %r% where $PATH:panfl.exe
:: set scripts=%scripts:~0,-10%
:: (or use `scripts` var predefined in pandoctools.exe)

:: `panfl sugartex -t %t%` = `sugartex %t%`
:: `panfl sugartex_kiwi` = `sugartex --kiwi`

%r% cat-md %inputs% | ^
%r% pre-knitty %input_file% | ^
%r% pre-sugartex | ^
%r% cat-md %all_inputs% | ^
%r% pandoc %reader_args% -t json | ^
%r% knitty %input_file% %reader_args% %writer_args% | ^
%r% sugartex %t% | ^
%r% pandoc-crossref %t% | ^
%r% pandoc -f json %writer_args%
