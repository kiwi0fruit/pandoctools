::conda install -c defaults -c conda-forge twine
set "script_dir=%~dp0"
cd /d "%script_dir%"

chcp 1252 && set "PYTHONIOENCODING="
python setup.py sdist
twine upload dist/* --skip-existing
chcp 65001 && set "PYTHONIOENCODING=utf-8"
