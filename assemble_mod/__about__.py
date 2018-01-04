import os.path

__all__ = [
    "__title__", "__summary__", "__uri__", "__version__",
    "__author__", "__email__", "__license__", "__copyright__",
]


try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    base_dir = None


__title__ = "assemble_mod"
__summary__ = "Run/Package Factorio Mod"
__uri__ = ""

# https://www.python.org/dev/peps/pep-0440/
__version__ = "0.1.0a1"

__author__ = "Dustine Camacho"
__email__ = ""

__license__ = "MIT"
__copyright__ = "2018 %s" % __author__
