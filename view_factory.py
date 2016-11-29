from table_view import TableView
from stats_view import StatsView
from arena_view import ArenaView
from move_stats_view import MoveStatsView
from perception_view import PerceptionView

from util import Error

def view_factory(view_name):
    """Very simple form of factory function   
    Used to decouple other modules from specific view implementations.
    """
    view = None
    if view_name == TableView.__name__:
        view = TableView()
    elif view_name == StatsView.__name__:
        view = StatsView()
    elif view_name == ArenaView.__name__:
        view = ArenaView()
    elif view_name == MoveStatsView.__name__:
        view = MoveStatsView()
    elif view_name == PerceptionView.__name__:
        view = PerceptionView()
    else:
        raise Error('Bad view name!')
    return view
