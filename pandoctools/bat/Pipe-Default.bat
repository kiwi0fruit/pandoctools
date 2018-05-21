@echo off
%r% cat-md %inputs% | ^
%r% pre-knitty "%input_file%" | ^
%r% pre-sugartex | ^
%r% cat-md %stdin_plus% | ^
%r% pandoc %reader_args% -t json | ^
%r% knitty "%input_file%" %reader_args% %writer_args% | ^
%r% sugartex %stex% | ^
%r% pandoc-crossref %to% | ^
%r% pandoc -f json %writer_args%

:: panfl sugartex -t %to% == sugartex %to% == sugartex 
:: panfl sugartex_kiwi -t %to% == sugartex --kiwi