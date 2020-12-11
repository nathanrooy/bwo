from random import uniform
from random import choice
from random import random
from random import randint
from copy import deepcopy


def generate_initial_position(nvar=None, x0=None, bounds=None):
    if bounds is None: return [uniform(-1,1) for _ in range(0, nvar)]
        # if bounds is not None:
        #     self.position = [
        #         uniform(bounds[i][0], bounds[i][1]) for i, x in enumerate(x0)]
        # self.func = func
        # self.cost = self.func(self.position)
    # pass


def minimize(func, x0, bounds=None, npop=10, maxiter=50):

    # constants
    nvar = len(x0)
    pp = 0.8                # procreating percentage
    cr = 0.5                # cannibalism rate
    pm = 0.4                # mutation rate

    nr = int(npop * pp)     # number of reproduction
    nm = int(npop * pm)     # number of mutation children

    spacer = len(str(npop))

    print('pp:', pp)
    print('pm:', pm)
    print('cr:', cr)

    print('npop:', npop)
    print('nr:', nr)
    print('nm:', nm)

    # initialize and sort population
    pop = [generate_initial_position(nvar=nvar) for _ in range(0, npop)]
    pop = sorted(pop, key=lambda x: func(x), reverse=False)
    hist = []

    # initialize outputs
    gbest = pop[0]
    
    # main loop
    for epoch in range(0, maxiter):

        pop = sorted(pop, key=lambda x: func(x), reverse=False)
        gbest = pop[0]
        print(f'   > ITER: {epoch:>{spacer}} | GBEST: {func(gbest):0.6f}')
        hist.append(gbest)

        pop1 = deepcopy(pop[:nr])
        pop2 = []
        pop3 = []

        # procreation and cannibalism
        for i in range(0, nr):

            # randomly pick two parents
            i1, i2 = randint(0, len(pop1)-1), randint(0, len(pop1)-1)
            p1, p2 = pop1[i1], pop1[i2]

            # crossover
            children = []
            for j in range(0, int(nvar/2)):

                # generate two new children using equation (1)
                alpha = random()
                c1 = [(alpha * v1) + ((1 - alpha)*v2) for v1, v2 in zip(p1, p2)]
                c2 = [(alpha * v2) + ((1 - alpha)*v1) for v1, v2 in zip(p1, p2)]

                # persist new children to temp population
                children.append(c1)
                children.append(c2)

            # cannibalism - destroy weakest parent
            if func(p1) > func(p2): pop2.append(p1)
            else: pop2.append(p2)

            # cannibalism - destroy some children
            children = sorted(children, key=lambda x: func(x), reverse=False)
            children = children[:int(len(children) * cr)]

            # add surviving children to pop2
            pop2.extend(children)

        # mutation
        for i in range(0, nm):

            # pick a random child
            m = choice(pop2)

            # pick two random chromosome positions
            cp1, cp2 = randint(0, nvar-1), randint(0, nvar-1)

            # swap chromosomes
            m[cp1], m[cp2] = m[cp2], m[cp1]

            # persist
            pop3.append(m)

        # assemble final population
        pop2.extend(pop3)
        pop = deepcopy(pop2)

    return hist
