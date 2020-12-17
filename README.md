# Black Widow Optimization

[![gh-actions-ci](https://img.shields.io/github/workflow/status/nathanrooy/bwo/CI?style=flat-square)](https://github.com/nathanrooy/bwo/actions?query=workflow%3Aci)
[![GitHub license](https://img.shields.io/github/license/nathanrooy/bwo?style=flat-square)](https://github.com/nathanrooy/bwo/blob/master/LICENSE)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/bwo.svg?style=flat-square)](https://pypi.org/pypi/bwo/)
[![PyPi Version](https://img.shields.io/pypi/v/bwo.svg?style=flat-square)](https://pypi.org/project/bwo)

<b>From the abstract</b>:
    ...a novel meta-heuristic algorithm suitable for continuous nonlinear optimization problems. The proposed method, Black Widow Optimization Algorithm (BWO), is inspired by the unique mating behavior of black widow spiders. This method includes an exclusive stage, namely, cannibalism. Due to this stage, species with inappropriate fitness are omitted from the circle, thus leading to early convergence. BWO algorithm is evaluated on 51 various benchmark functions to verify its efficiency in obtaining the optimal solutions for the problems. The obtained results indicate that the proposed algorithm has numerous advantages in different aspects such as early convergence and achieving optimized fitness value compared to other algorithms.

### Installation
```
pip install bwo
```
or 
```
pip install git+https://github.com/nathanrooy/bwo
```

### Usage
As a simple example, let's find the minimum of the single objective <a target="_blank" href="https://github.com/nathanrooy/landscapes#sphere-function">sphere</a> function availabel in the <a target="_blank" href="https://github.com/nathanrooy/landscapes">Landscapes</a> Python package.

```
pip install landscapes
```
Next, let's import everything we need.
```
from bwo import minimize
from landscapes.single_objective import sphere
```
Now, we just need to call the minimize function. For this particular example, let's optimize across 5 degrees of freedom.
```
fbest, xbest = minimize(sphere, dof=5)
```
Where `fbest` is the best function value achieved during optimization, and `xbest` is the function input which yielded `fbest`.

You can also minimize a function given boundry constraints, represented by a list of tuples. Each tuple must follow the (min, max) format.
```
bounds = [(-1,1),(-2,2), (-3,3), (-4,4), (-5,5)]
fbest, xbest = minimize(sphere, bounds=bounds, disp=False)
```

### Options
<b>minimize</b>(func, x0=None, dof=None, bounds=None, pp=0.6, cr=0.44, pm=0.4, npop=10, disp=False, maxiter=50)

- `func` (callable) : The objective function to be minimized.
- `x0` (list) : Initial guess (optional).
- `dof` (int) : degrees of freedom (optional)
- `bounds`(list of tuples) : boundary constraints as specified as a list of (xi_min, xi_max) tuples.
- `pp` (float) : procreating percentage [0, 1].
- `cr` (float) : cannibalism rate [0, 1]. 
- `pm` (float) : mutation rate [0, 1].
- `maxiter` (int) : maximum number of iterations.
- `disp` (bool) : output intermediate results at each iteration.

### References

    @article{article,
    author = {Hayyolalam, Vahideh and Pourhaji Kazem, Ali Asghar},
    year = {2019},
    month = {10},
    pages = {103249},
    title = {Black Widow Optimization Algorithm: A novel meta-heuristic approach for solving engineering optimization problems ✩},
    volume = {87},
    journal = {Engineering Applications of Artificial Intelligence},
    doi = {10.1016/j.engappai.2019.103249}
    }
