from table_view import TableView
from stats_view import StatsView
from arena_view import ArenaView

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
    else:
        print('Bad view name!')
    # TODO: will add exception handling later to propagate a "bad view name"
    # error to the caller
    return view
    