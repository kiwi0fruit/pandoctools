:: Activates conda environment from predefined defaults.
:: Uses predefined variable:
::   %conda_env%
::   %call%

if not "%conda_env%" == "" (
    %call% activate %conda_env%
)
