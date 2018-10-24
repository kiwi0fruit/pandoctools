@echo off
set KNITTY=True

%r% cat-md %inputs% | ^
%r% pre-knitty "%input_file%" | ^
%r% pre-sugartex | ^
%r% cat-md %stdin_plus% | ^
%r% pandoc %reader_args% -t json | ^
%r% knitty "%input_file%" %reader_args% %writer_args% | ^
%r% sugartex %sugartex% | ^
%r% pandoc-crossref %t% | ^
%r% pandoc -f json %writer_args%

:: panfl sugartex -t %t% == sugartex %t% == sugartex 
:: panfl sugartex_kiwi -t %t% == sugartex --kiwi
