from original_larva import OriginalLarva
from new_larva import NewLarva

from util import Error

def larva_factory(larva_name, location, velocity):
    """Very simple form of factory function   
    Used to decouple other modules from specific view implementations.
    """
    larva = None
    if larva_name == OriginalLarva.__name__:
        larva = OriginalLarva(location, velocity)
    elif larva_name == NewLarva.__name__:
        larva = NewLarva(location, velocity)
    else:
        raise Error('Bad larva name!')
    return larva
