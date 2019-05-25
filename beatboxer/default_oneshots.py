from inspect import getsourcefile
from os import path

CUR_DIR = path.dirname(path.abspath(getsourcefile(lambda: 0)))
ROOT = CUR_DIR[:CUR_DIR.rfind(path.sep)]
ONESHOT_PATH = path.join(ROOT, 'beatboxer', 'samples')
