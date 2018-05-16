:: Simply adds conda environment to PATH.
:: First arg is provided env path.

set pypath=%~1
set PATH=%pypath%;%pypath%\Scripts;%pypath%\Library\bin;%PATH%
