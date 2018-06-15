python setup.py sdist
chcp 1252 > NUL
set "PYTHONIOENCODING="
twine upload dist/* --skip-existing
chcp 65001 > NUL
set "PYTHONIOENCODING=utf-8"
