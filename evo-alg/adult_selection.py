from utils import f


def full_generational_replacement(old_population, children, **kwargs):
    return children


def over_production(old_population, children, m, **kwargs):
    return sorted(children, key=f, reverse=True)[:m]


def generational_mixing(old_population, children, m, **kwargs):
    return sorted(old_population + children, key=f, reverse=True)[:m]


ADULT_SELECTION_METHODS = (full_generational_replacement, over_production, generational_mixing)