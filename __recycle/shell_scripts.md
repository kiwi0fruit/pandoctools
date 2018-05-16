**Filters pipes shell scripts** (bash/batch) as interface to Panflute Pandoc filters and python text filters. Users write a shell script that specifies filters and Pandoc options. Then they use it to convert the particular document or to convert any document of choise in the same manner.

Actually it's some pre-written scripts, some standards of writing shell scripts and one new command line application that makes these scripts shorter.


:: sugartex == panfl sugartex -d "%f%" == python "%f%\sugartex.py"
:: sugartex kiwi == python "%f%\sugartex.py" kiwi == panfl sugartex_kiwi -d "%f%" == python "%f%\sugartex_kiwi.py"

pip install git+file:///C:/Users/User/GitSpace/Dropbox/Python/ResearchProjects/pandoctools#egg=pandoctools
pip install git+file:///D:/BACKUP/GitHub/pandoctools#egg=pandoctools


panfl filter1 filter2 -d %f% --dir folder --sys-path --data-dir

Написать что новые команды работают во всех операционных системах

написать, что setmeta работает в случаях когда нужно отсутствия искажения

написать, что дефолтный ямл можно задать подав вторую переменную в скрипт - ибо typemd читает несколько файлов

Написать, что скрипт может как внутри себя задать переменные ридера и райтера, так и использовать уже заданные атомом

Написать что скрипты для атома и для запуска напрямую разные. Привести примеры

написать, что скрипты не должны менять stdin stdout в неположенных местах

panfl - у него список фильтров. либо просто названия без расширений - внутри питоновского модуля. либо пути к файлам. если ./file или file.py - то уже точно просто файл
а file - дефолтный
фильтры панфлюта, так что им параметры не нужны

# New commands:

## set-meta

`set-meta metadatakey list of arguments` – useful for setting Panflute filters arguments from command line.

## cat-md

<...>

# Useful commands:

если хочется не открытый файл первым, то надо
```
cat-md meta.yaml stdin
```

`pandoc --metadata key=val -t json`

`cat-md %*` – type all script arguments.

`python -c "import sys; sys.stdout.write('text')"`

`echo some text > tmp.txt`
`del tmp.txt`

`set name=%name:~0,-3%`

`set /p var=<tmp.txt`

можно создать папку с временными файлами (и потом её удалить):
```
set t=__temp\
if not exist %t% mkdir %t%

<...>

rmdir %t% /s /q
```

а можно создать один временный файл:
```
echo text > _temp

<...>

del _temp
```

`echo > NUL`

# Example scrpts:

script for converting _ExampleDoc.md to markdown


call /?

...

%* in a batch script refers to all the arguments (e.g. %1 %2 %3
    %4 %5 ...)

Substitution of batch parameters (%n) has been enhanced.  You can
now use the following optional syntax:

    %~1         - expands %1 removing any surrounding quotes (")
    %~f1        - expands %1 to a fully qualified path name
    %~d1        - expands %1 to a drive letter only
    %~p1        - expands %1 to a path only
    %~n1        - expands %1 to a file name only
    %~x1        - expands %1 to a file extension only
    %~s1        - expanded path contains short names only
    %~a1        - expands %1 to file attributes
    %~t1        - expands %1 to date/time of file
    %~z1        - expands %1 to size of file
    %~$PATH:1   - searches the directories listed in the PATH
                   environment variable and expands %1 to the fully
                   qualified name of the first one found.  If the
                   environment variable name is not defined or the
                   file is not found by the search, then this
                   modifier expands to the empty string

The modifiers can be combined to get compound results:

    %~dp1       - expands %1 to a drive letter and path only
    %~nx1       - expands %1 to a file name and extension only
    %~dp$PATH:1 - searches the directories listed in the PATH
                   environment variable for %1 and expands to the
                   drive letter and path of the first one found.
    %~ftza1     - expands %1 to a DIR like output line

In the above examples %1 and PATH can be replaced by other
valid values.  The %~ syntax is terminated by a valid argument
number.  The %~ modifiers may not be used with %*
