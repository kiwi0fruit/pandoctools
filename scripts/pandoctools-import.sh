# Usage in Pandoctools profiles (for Profile-Default.sh):
#   . "$import" Profile-Default

# Uses predefined absolute path variables:
#   ${core_config} (<...>/site-packages/pandoctools/sh)
#   ${user_config} ($HOME/.pandoc/pandoctools)

if [ exist "%user_config%\%~1.bat" ]; then
    source "%user_config%\%~1.bat"
else
    source "%core_config%\%~1.bat"
fi

