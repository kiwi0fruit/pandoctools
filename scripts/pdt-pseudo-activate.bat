:: Simply adds conda environment to PATH.
:: Uses predefined variables:
::   %conda_env%
::   %python_path%
::   %env_path%

if not "%conda_env%" == "" (
    set pypath=%env_path%
    if %env_path% == "" if not "%python_path%" == "" (
        set pypath=%python_path%\envs\%conda_env%
    )
    if not "%pypath%" == "" (
        set PATH=%pypath%;%pypath%\Scripts;%pypath%\Library\bin;%PATH%
    )
)
