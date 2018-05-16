:: Deactivates conda environment if defaults were predefined.
:: Uses predefined variables:
::   %conda_env%
::   %call%

if not "%conda_env%" == "" (
    %call% deactivate
)
