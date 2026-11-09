import io
import unittest
from contextlib import redirect_stdout

from bwo import minimize
from bwo.main import _generate_new_position


def _sphere(x: list[float]) -> float:
    return sum(v * v for v in x)


class TestBWO(unittest.TestCase):
    def test_generate_new_position(self) -> None:
        # case with just dof
        dof = 10
        p = _generate_new_position(dof=dof)
        self.assertEqual(len(p), dof)
        for v in p:
            self.assertLessEqual(v, 1.0)
            self.assertGreaterEqual(v, -1.0)

        # case with just x0
        x0 = [2.0, 3.0, 10.5]
        p = _generate_new_position(x0=x0)
        self.assertEqual(len(p), len(x0))
        for x_i, v in zip(x0, p, strict=True):
            self.assertLessEqual(v, x_i + 1.0)
            self.assertGreaterEqual(v, x_i - 1.0)

        # case with just bounds
        bounds = [(-5.0, 5.0), (-4.0, 4.0), (10.0, 11.0)]
        p = _generate_new_position(bounds=bounds)
        self.assertEqual(len(p), len(bounds))
        for b, v in zip(bounds, p, strict=True):
            self.assertLessEqual(v, b[1])
            self.assertGreaterEqual(v, b[0])

        # case with x0 and bounds
        p = _generate_new_position(x0=x0, bounds=bounds)
        self.assertEqual(len(p), len(x0))
        for i, v in enumerate(p):
            self.assertLessEqual(v, bounds[i][1])
            self.assertGreaterEqual(v, bounds[i][0])

        # case with no arguments
        with self.assertRaises(ValueError):
            _generate_new_position()

    def test_minimize_sphere_dof(self) -> None:
        fbest, xbest = minimize(_sphere, dof=3, npop=20, maxiter=30, seed=42)
        self.assertEqual(len(xbest), 3)
        self.assertAlmostEqual(fbest, _sphere(xbest))
        self.assertLess(fbest, 1e-2)

    def test_minimize_dof_1(self) -> None:
        fbest, xbest = minimize(_sphere, x0=[2.5], npop=15, maxiter=30, seed=7)
        self.assertEqual(len(xbest), 1)
        self.assertLess(fbest, 1e-2)

    def test_minimize_bounds_enforced(self) -> None:
        bounds = [(-5.0, -4.0), (10.0, 11.0), (1.0, 2.0)]
        fbest, xbest = minimize(_sphere, bounds=bounds, npop=15, maxiter=25, seed=123)
        self.assertEqual(len(xbest), len(bounds))
        for (low, high), val in zip(bounds, xbest, strict=True):
            self.assertGreaterEqual(val, low)
            self.assertLessEqual(val, high)
        # minimum of x^2 on [-5, -4] x [10, 11] x [1, 2] is (-4)^2 + 10^2 + 1^2 = 117
        self.assertAlmostEqual(fbest, 117.0, places=1)

    def test_minimize_seed_reproducibility(self) -> None:
        res1 = minimize(_sphere, dof=4, npop=12, maxiter=15, seed=99)
        res2 = minimize(_sphere, dof=4, npop=12, maxiter=15, seed=99)
        self.assertEqual(res1, res2)

    def test_minimize_early_stopping(self) -> None:
        # constant function never improves, so patience=3 should stop after 3 epochs
        buf = io.StringIO()
        with redirect_stdout(buf):
            minimize(
                lambda _: 1.0,
                dof=2,
                npop=6,
                maxiter=50,
                tol=1e-4,
                patience=3,
                disp=True,
                seed=1,
            )
        lines = [line for line in buf.getvalue().splitlines() if line.strip()]
        self.assertEqual(len(lines), 3)

    def test_minimize_validation(self) -> None:
        with self.assertRaises(TypeError):
            minimize(_sphere, dof=2, disp="yes")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            minimize(_sphere, dof=2, npop=True)
        with self.assertRaises(ValueError):
            minimize(_sphere, dof=2, npop=1)
        with self.assertRaises(TypeError):
            minimize(_sphere, dof=2, maxiter=10.5)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            minimize(_sphere, dof=2, maxiter=0)
        with self.assertRaises(TypeError):
            minimize(_sphere, x0=(1.0, 2.0))  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            minimize(_sphere, dof="2")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            minimize(_sphere, bounds=((-1.0, 1.0),))  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            minimize(_sphere)
        with self.assertRaises(ValueError):
            minimize(_sphere, x0=[0.0], bounds=[(-1.0, 1.0), (-1.0, 1.0)])
        with self.assertRaises(ValueError):
            minimize(_sphere, dof=2, pp=0.0)
        with self.assertRaises(ValueError):
            minimize(_sphere, dof=2, cr=1.5)
        with self.assertRaises(ValueError):
            minimize(_sphere, dof=2, pm=-0.1)
        with self.assertRaises(ValueError):
            minimize(_sphere, dof=2, tol=-1.0)
        with self.assertRaises(TypeError):
            minimize(_sphere, dof=2, patience=True)
        with self.assertRaises(ValueError):
            minimize(_sphere, dof=2, patience=0)
        with self.assertRaises(TypeError):
            minimize(_sphere, dof=2, seed="42")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            minimize(_sphere, bounds=[[-1.0, 1.0]])  # type: ignore[list-item]
        with self.assertRaises(ValueError):
            minimize(_sphere, bounds=[(2.0, -1.0)])
        with self.assertRaises(ValueError):
            minimize(_sphere, dof=0)


if __name__ == "__main__":
    unittest.main()
