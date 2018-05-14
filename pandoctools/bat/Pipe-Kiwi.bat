@echo off
%r% cat-md stdin | ^
%r% pre-knitty %input_file% | ^
%r% pre-sugartex | ^
%r% cat-md %inputs% | ^
%r% pandoc %reader_args% -t json | ^
%r% knitty %input_file% %reader_args% %writer_args% | ^
%r% sugartex --kiwi | ^
%r% pandoc-crossref %to% | ^
%r% pandoc -f json %writer_args%
