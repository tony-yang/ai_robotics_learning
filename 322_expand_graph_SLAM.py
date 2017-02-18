# Based on https://github.com/vicapow/udacity-ai-solutions/blob/master/kalman-matrices-unit2-32.py
# Changed some implementation details
# For Sebastian's Kalman Filter class exercise

from math import *

class matrix:
    def __init__(self, value=[[]]):
        self.value = value
        self.dimx = len(value)
        self.dimy = len(value[0])
        if value == [[]]:
            self.dimx = 0

    def zero(self, dimx, dimy):
        if dimx < 1 or dimy < 1:
            raise ValueError("Invalid size of matrix")
        else:
            self.dimx = dimx
            self.dimy = dimy
            self.value = [[0 for row in range(dimy)] for col in range(dimx)]

    def identity(self, dim):
        if dim < 1:
            raise ValueError("Invaolid size of matrix")
        else:
            self.zero(dim, dim)
            for i in range(dim):
                self.value[i][i] = 1

    def show(self):
        for i in range(self.dimx):
            print(self.value[i])

    def __add__(self, other):
        if self.dimx != other.dimx or self.dimy != other.dimy:
            raise ValueError("Matrices must be of equal dimensions to add")
        else:
            res = matrix([[]])
            res.zero(self.dimx, self.dimy)
            for i in range(self.dimx):
                for j in range(self.dimy):
                    res.value[i][j] = self.value[i][j] + other.value[i][j]
            return res

    def __sub__(self, other):
        if self.dimx != other.dimx or self.dimy != other.dimy:
            raise ValueError("Matrices must be of equal dimensions to add")
        else:
            res = matrix([[]])
            res.zero(self.dimx, self.dimy)
            for i in range(self.dimx):
                for j in range(self.dimy):
                    res.value[i][j] = self.value[i][j] - other.value[i][j]
            return res

    def __mul__(self, other):
        if self.dimy != other.dimx:
            raise ValueError("The column dimension of the first matrix must match the row dimension of the second matrix. (m*n and n*p)")
        else:
            res = matrix([[]])
            res.zero(self.dimx, other.dimy)
            for i in range(self.dimx):
                for j in range(other.dimx):
                    for k in range(other.dimy):
                        res.value[i][k] += self.value[i][j] * other.value[j][k]
            return res

    def take(self, list1, list2 = []):
        if list2 == []:
            list2 = list1
        if len(list1) > self.dimx or len(list2) > self.dimy:
            raise ValueError("list invalid in take()")

        res = matrix()
        res.zero(len(list1), len(list2))
        for i in range(len(list1)):
            for j in range(len(list2)):
                res.value[i][j] = self.value[list1[i]][list2[j]]
        return res

    def expand(self, dimx, dimy, list1, list2 = []):
        if list2 == []:
            list2 = list1
        if len(list1) > self.dimx or len(list2) > self.dimy:
            raise ValueError("list invalid in expand()")

        res = matrix()
        res.zero(dimx, dimy)
        for i in range(len(list1)):
            for j in range(len(list2)):
                res.value[list1[i]][list2[j]] = self.value[i][j]
        return res

    def transpose(self):
        res = matrix([[]])
        res.zero(self.dimy, self.dimx)
        for i in range(self.dimx):
            for j in range(self.dimy):
                res.value[j][i] = self.value[i][j]
        return res

    # Section directly copied from the source code
    def Cholesky(self, ztol=1.0e-5):
        # Computes the upper triangular Cholesky factorization of
        # a positive definite matrix.
        res = matrix([[]])
        res.zero(self.dimx, self.dimx)

        for i in range(self.dimx):
            S = sum([(res.value[k][i])**2 for k in range(i)])
            d = self.value[i][i] - S
            if abs(d) < ztol:
                res.value[i][i] = 0.0
            else:
                if d < 0.0:
                    raise ValueError("Matrix not positive-definite")
                res.value[i][i] = sqrt(d)
            for j in range(i+1, self.dimx):
                S = sum([res.value[k][i] * res.value[k][j] for k in range(self.dimx)])
                if abs(S) < ztol:
                    S = 0.0
                res.value[i][j] = (self.value[i][j] - S)/res.value[i][i]
        return res

    def CholeskyInverse(self):
        # Computes inverse of matrix given its Cholesky upper Triangular
        # decomposition of matrix.
        res = matrix([[]])
        res.zero(self.dimx, self.dimx)

        # Backward step for inverse.
        for j in reversed(range(self.dimx)):
            tjj = self.value[j][j]
            S = sum([self.value[j][k]*res.value[j][k] for k in range(j+1, self.dimx)])
            res.value[j][j] = 1.0/tjj**2 - S/tjj
            for i in reversed(range(j)):
                res.value[j][i] = res.value[i][j] = -sum([self.value[i][k]*res.value[k][j] for k in range(i+1, self.dimx)])/self.value[i][i]
        return res

    def inverse(self):
        aux = self.Cholesky()
        res = aux.CholeskyInverse()
        return res

    def __repr__(self):
        return repr(self.value)


def doit(init, move1, move2, Z0, Z1, Z2):
    Omega = matrix([
        [1., 0., 0.],
        [0., 0., 0.],
        [0., 0., 0.]
    ])
    Xi = matrix([[init], [0.], [0.]])

    Omega += matrix([
        [1., -1., 0.],
        [-1., 1., 0.],
        [0., 0., 0.]
    ])
    Xi += matrix([[-move1], [move1], [0.]])

    Omega += matrix([
        [0., 0., 0.],
        [0., 1., -1.],
        [0., -1., 1.]
    ])
    Xi += matrix([[0.], [-move2], [move2]])

    # omega_inverse = Omega.inverse()
    # omega_inverse.show()
    # res = omega_inverse * Xi
    # res.show()
    Omega = Omega.expand(4, 4, [0, 1, 2], [0, 1, 2])
    Xi = Xi.expand(4, 1, [0,1, 2], [0])

    Omega += matrix([
        [1., 0., 0., -1.],
        [0., 0., 0., 0],
        [0., 0., 0., 0],
        [-1., 0., 0., 1.],
    ])
    Xi += matrix([[-Z0], [0.], [0.], [Z0]])

    Omega += matrix([
        [0., 0., 0., 0.],
        [0., 1., 0., -1],
        [0., 0., 0., 0],
        [0., -1., 0., 1.],
    ])
    Xi += matrix([[0.], [-Z1], [0.], [Z1]])

    Omega += matrix([
        [0., 0., 0., 0],
        [0., 0., 0., 0],
        [0., 0., 5., -5.],
        [0., 0., -5., 5.],
    ])
    Xi += matrix([[0.], [0.], [-Z2 * 5], [Z2 * 5]])

    res = Omega.inverse() * Xi
    res.show()

doit(-3, 5, 3, 10, 5, 1)
