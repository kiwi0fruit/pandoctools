set "script_dir=%~dp0"
cd /d "%script_dir%"

python setup.py sdist
:: sdist is a source distribution
:: it can be changed to binary wheel
chcp 1252 && set "PYTHONIOENCODING="
twine upload dist/* --skip-existing
chcp 65001 && set "PYTHONIOENCODING=utf-8"
