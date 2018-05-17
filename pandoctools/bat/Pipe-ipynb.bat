@echo off

%r% cat-md stdin | ^
%r% pre-knitty %input_file% | ^
%r% pre-sugartex | ^
%r% cat-md %stdin_plus% | ^
%r% pandoc %reader_args% -t json | ^
%r% knitty %input_file% %reader_args% %writer_args% --to-ipynb | ^
%r% %sugartex% | ^
%r% pandoc-crossref %t% | ^
%r% pandoc -f json %writer_args% | ^
%r% knotedown --match=in --nomagic > "%input_file%.%out_ext_full%"

%r% jupyter nbconvert --to notebook --execute "%input_file%.%out_ext_full%"
