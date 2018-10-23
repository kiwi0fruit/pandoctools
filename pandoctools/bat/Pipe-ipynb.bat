@echo off
set KNITTY=True

%r% cat-md %inputs% | ^
%r% pre-knitty "%input_file%" | ^
%r% pre-sugartex | ^
%r% cat-md %stdin_plus% | ^
%r% pandoc %reader_args% -t json | ^
%r% knitty "%input_file%" %reader_args% %writer_args% --to-ipynb | ^
%r% sugartex %stex% | ^
%r% pandoc-crossref %to% | ^
%r% pandoc -f json %writer_args% | ^
%r% knotedown --match=in --nomagic | ^
%r% jupyter nbconvert --to notebook --execute --stdin --stdout
