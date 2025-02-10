set -e

echo INSTALL PYTHON DEPENDENCY
pip install -r requirements_test.txt


echo MYPY CHECKS
mypy -m etls
cd etls

echo FLAKE8 CHECKS
flake8 -v

echo COVERAGE PYTEST/UNITTEST
coverage erase
coverage run --source . -m pytest -vv tests/test_*.py
coverage xml