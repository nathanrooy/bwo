import sys
from collections.abc import Callable, Sequence
from copy import deepcopy
from random import choice, random, sample, uniform

sys.tracebacklimit = 0


def _generate_new_position(
    x0: Sequence[float] | None = None,
    dof: int | None = None,
    bounds: Sequence[tuple[float, float]] | None = None,
) -> list[float]:
    """GENERATE NEW POSITION

    Parameters
    ----------
    dof : int
    x0 : list
    bounds : list of tuples [(x1_min, x1_max),...,(xn_min, xn_max)]

    Returns
    -------
    list

    Notes
    -----
    There are several ways in which an initial position can be generated.
    Outlined below are all possible scenarios and outputs.

    nomenclature:
        "dof" = "degrees of freedom" = "dimensions" = "d"
        p = new initial position vector of length d

    just bounds:
        for each position i in bounds,  p[i] = random value in [i_min, i_max]]

    just x0:
        for each position i in x0: p[i] = x0[i] + random value in [-1, 1]

    just dof:
        for each position i from 0 to d,  p[i] = random value in [-1, 1]

    dof + x0:
        since dof and x0 are redundent from a dimensionality perspective,
        this situation will defer to the case above "just x0".

    dof + bounds:
        since dof and bounds are redundent from a dimensionality perspective,
        this situation wll defer to the case above "just bounds"

    x0 + bounds:
        for each position i in x0:
            p[i] = x0[i] + random value in [-1, 1] constrained by bounds[i].min
            and bounds[i].max

    dof + x0 + bounds:
        see case: "x0 + bounds" above

    All this boils down to four cases (ordered by information gain from user):
    1) x0 and bounds
    2) bounds
    3) x0
    4) dof
    """
    if x0 and bounds:
        return [
            min(max(uniform(-1, 1) + x0[i], bounds[i][0]), bounds[i][1])
            for i in range(len(x0))
        ]

    if bounds:
        return [uniform(bounds[i][0], bounds[i][1]) for i in range(len(bounds))]

    if x0:
        return [x_i + uniform(-1, 1) for x_i in x0]

    if dof:
        return [uniform(-1, 1) for _ in range(dof)]

    raise ValueError("Must specify at least one of the following: x0, dof, or bounds")


def minimize(
    func: Callable[[list[float]], float],
    x0: list[float] | None = None,
    dof: int | None = None,
    bounds: list[tuple[float, float]] | None = None,
    pp: float = 0.6,
    cr: float = 0.44,
    pm: float = 0.4,
    npop: int = 10,
    disp: bool = False,
    maxiter: int = 50,
) -> tuple[float, list[float]]:
    """
    Parameters
    ----------
    x0 : list
        initial guess
    pp : float
        procreating percentage
    cr : float
        cannibalism rate. A cr of 1 results in all children surviving. A cr of 0
        results in no children surviving
    pm : float
        mutation rate

    Returns
    -------
    float : solution at global best
    list : position at global best

    References
    ----------
    """
    # do some basic checks before going any further
    assert isinstance(disp, bool), "parameter: disp -> must be of type: bool"
    assert isinstance(npop, int), "parameter: npop -> must be of type: int"
    assert isinstance(maxiter, int), "parameter: maxiter -> must be of type int"
    if x0 is not None:
        assert isinstance(x0, list), "x0 must be of type: list"
    if dof is not None:
        assert isinstance(dof, int), "parameter: dof -> must be of type: int"
    if bounds is not None:
        assert isinstance(bounds, list), "parameter: bounds -> must be of type list"
    assert x0 is not None or dof is not None or bounds is not None, (
        "must specify at least one of the following: x0, dof, or bounds"
    )
    if x0 and bounds:
        assert len(bounds) == len(x0), "x0 and bounds must have same number of elements"
    assert 0 < pp <= 1, 'procreating percentage "pp" must be: 0 < pp <= 1'
    assert 0 <= cr <= 1, 'cannibalism rate "cr" must be: 0 < cr <= 1'
    assert 0 <= pm <= 1, 'mutation rate "pm" must be: 0 < pm <= 1'
    assert maxiter > 0, "maxiter must be greater than zero."

    # check bounds specification if necessary
    if bounds:
        assert isinstance(bounds, list), "bounds must be of type: list"
        for b in bounds:
            assert isinstance(b, tuple), (
                "element in bounds is not of type: tuple. "
                "every element must be a tuple as specified (v_min, v_max)"
            )
            assert b[0] < b[1], (
                "element in bounds specified incorrectly. must be (xi_min, xi_max)"
            )

    # constants
    if x0 is not None:
        dof = len(x0)
    elif bounds is not None:
        dof = len(bounds)
    assert dof is not None
    assert dof > 0, "dof must be greater than zero."

    nr = max(int(npop * pp), 2)  # number of reproduction
    nm = int(npop * pm)  # number of mutation children
    spacer = len(str(npop))  # for logging only

    # initialize population
    pop = [_generate_new_position(x0, dof, bounds) for _ in range(npop)]
    gbest: list[float] = pop[0]

    # main loop
    for epoch in range(maxiter):
        # initialize epoch
        pop = sorted(pop, key=lambda x: func(x), reverse=False)
        pop1 = deepcopy(pop[:nr])
        pop2: list[list[float]] = []
        pop3: list[list[float]] = []
        gbest = pop[0]

        # print something useful
        if disp:
            print(f"> ITER: {epoch + 1:>{spacer}} | GBEST: {func(gbest):0.6f}")

        # procreation and cannibalism
        for _ in range(nr):
            # 1. pick two distinct parents from pop1
            p1, p2 = sample(pop1, 2)

            # 2. cannibalism: fitter parent is mother, weaker (father) discarded
            mother = p1 if func(p1) <= func(p2) else p2

            # 3. procreation: generate offspring using equation (1)
            children: list[list[float]] = []
            for _ in range(max(dof // 2, 1)):
                alpha = [random() for _ in range(dof)]
                c1 = [
                    (a * v1) + ((1.0 - a) * v2)
                    for a, v1, v2 in zip(alpha, p1, p2, strict=True)
                ]
                c2 = [
                    (a * v2) + ((1.0 - a) * v1)
                    for a, v1, v2 in zip(alpha, p1, p2, strict=True)
                ]
                children.append(c1)
                children.append(c2)

            # 4. sibling cannibalism + matriphagy: combine mother and children,
            # sort by fitness, and keep top survivors
            family = [deepcopy(mother), *children]
            family.sort(key=func)
            n_survivors = max(int(len(family) * cr), 1)

            pop2.extend(family[:n_survivors])

        # mutation
        for _ in range(nm):
            # pick a random solution from pop1 and copy it
            m = choice(pop1).copy()

            # pick two distinct chromosome positions and swap them (or perturb in 1D)
            if dof >= 2:
                cp1, cp2 = sample(range(dof), 2)
                m[cp1], m[cp2] = m[cp2], m[cp1]
            else:
                m = _generate_new_position(x0=m, dof=dof, bounds=bounds)

            # persist
            pop3.append(m)

        # assemble final population
        pop2.extend(pop3)
        pop = deepcopy(pop2)

    # return global best position and func value at global best position
    return func(gbest), gbest
