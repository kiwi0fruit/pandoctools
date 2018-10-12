::conda install -c defaults -c conda-forge twine
set "script_dir=%~dp0"
cd /d "%script_dir%"

python setup.py sdist
twine upload dist/* --skip-existing
