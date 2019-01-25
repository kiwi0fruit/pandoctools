mkdir "%LIBRARY_PREFIX%\git-bash"
7za x PortableGit-%PKG_VERSION%-%ARCH%-bit.7z.exe -o"%LIBRARY_PREFIX%\git-bash" -aoa
if errorlevel 1 exit 1

move "%LIBRARY_PREFIX%\git-bash\LICENSE.txt" .\
cd "%LIBRARY_PREFIX%\git-bash"
call post-install.bat
del post-install.bat
del README.portable
IF NOT EXIST _bin mkdir _bin
move bin\git.exe _bin

IF NOT EXIST "%PREFIX%\Menu" mkdir -p "%PREFIX%\Menu"
copy "%RECIPE_DIR%\git-bash.json" "%PREFIX%\Menu\"
copy "%RECIPE_DIR%\git-bash.ico" "%PREFIX%\Menu\"

mkdir -p "%PREFIX%\etc\conda\activate.d"
copy "%RECIPE_DIR%\git-bash.bat" "%PREFIX%\etc\conda\activate.d\"
exit 0
