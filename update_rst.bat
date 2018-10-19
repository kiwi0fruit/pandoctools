set "script_dir=%~dp0"
cd /d "%script_dir%"

chcp 65001 > NUL
pandoc README.md -o README.rst
