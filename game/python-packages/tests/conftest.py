import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# python -m pytest game/python-packages/tests/

# run a test individually:
# python -m pytest game/python-packages/tests/test_chess.py::test_name
# The -m pytest part is what ensures conftest.py is loaded before imports happen.