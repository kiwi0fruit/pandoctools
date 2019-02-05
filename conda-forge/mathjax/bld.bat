ren "%SRC_DIR%\MathJax-%PKG_VERSION%" "%SRC_DIR%\mathjax" || exit 1
copy "%SRC_DIR%\mathjax\LICENSE" "%SRC_DIR%\" || exit 1
if not exist "%LIBRARY_LIB%" mkdir "%LIBRARY_LIB%" || exit 1
move "%SRC_DIR%\mathjax" "%LIBRARY_LIB%\" || exit 1
if not exist "%SCRIPTS%" mkdir "%SCRIPTS%" || exit 1
copy "%RECIPE_DIR%\mathjax-conda" "%SCRIPTS%\" || exit 1
copy "%RECIPE_DIR%\mathjax-conda.bat" "%SCRIPTS%\" || exit 1
