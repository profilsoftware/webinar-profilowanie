import cProfile
from pstats import SortKey

from talk_python_app import main

cProfile.run('main()', sort=SortKey.CUMULATIVE)
