import unittest

from bwo.main import _generate_new_position


class test_all(unittest.TestCase):
    def test_generate_new_position(self) -> None:
        # case with just dof
        dof = 10
        p = _generate_new_position(dof=dof)
        self.assertEqual(len(p), dof)
        for v in p:
            self.assertLess(v, 1)
            self.assertGreater(v, -1)

        # case with just x0
        x0 = [2.0, 3.0, 10.5]
        p = _generate_new_position(x0=x0)
        self.assertEqual(len(p), len(x0))
        for v in p:
            self.assertLessEqual(v, v + 1)
            self.assertGreaterEqual(v, v - 1)

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


if __name__ == "__main__":
    unittest.main()
