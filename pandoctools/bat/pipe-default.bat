@echo off
:: %call% setvar scripts where $PATH:pip.exe
:: set scripts=%scripts:~0,-8%
:: Or use predefined `scripts` that is defined in pandoctools.exe:
:: panfl -d "%scripts%" sugartex == panfl --sys-path sugartex == sugartex
:: panfl -d "%scripts%" sugartex_kiwi == panfl --sys-path sugartex_kiwi == sugartex kiwi
%run% cat-md %inputs% | %run% pre-knitty %input_file% | %run% pre-sugartex | %run% cat-md %all_inputs% | %run% pandoc %reader_args% -t json | %run% knitty %input_file% %reader_args% %writer_args% | %run% sugartex | %run% pandoc -f json %writer_args%
