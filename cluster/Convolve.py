import itertools as it
import numpy as np
from scipy import ndimage

def convolve(A, B):
    '''Returns the convolution of A and B where

    A, B are numpy.ndarrays of equal dimension

    Their convolution, C, is an ndarray. If we interpret A and B as tensors
    which hold the coefficients of some multivariate polynomial, C is a tensor
    which holds the coefficients for their polynomial product.

    This version of convolve is backed by the convolution function found in
    ndimage (with some adjustments to get the edges to work right).
    It is _by far_ the faster of the two
    '''
    assert len(A.shape) == len(B.shape),\
            "Input A has dimension %d but B has dimension %d." % (len(A.shape), len(B.shape))

    for i, l in enumerate(A.shape):
        assert l > 0, "A has length 0 in its %d dimension" % i

    for i, l in enumerate(B.shape):
        assert l > 0, "B has length 0 in its %d dimension" % i

    out_shape = tuple( i + j - 1 for (i, j) in zip(A.shape, B.shape) )
    A_pad = np.zeros(out_shape, dtype=A.dtype)
    A_pad_slices = tuple(slice(b-1,None) for b in B.shape)
    A_pad[A_pad_slices] += A
    filter_offset = tuple((b-1) // 2 for b in B.shape)
    return ndimage.convolve(A_pad, B, mode='constant', cval=0, origin=filter_offset)

def convolve_py(A, B):
    '''Returns the convolution of A and B where

    A, B are numpy.ndarrays of equal dimension

    Their convolution, C, is an ndarray. If we interpret A and B as tensors
    which hold the coefficients of some multivariate polynomial, C holds the
    coefficients for their polynomial product.

    This version of convolve is naive - it is entirely python code.
    It is pretty slow, and we just wrote it because it is easier to understand,
    so it can be used to test the numpy-backed convolution
    '''
    assert len(A.shape) == len(B.shape),\
            "Input A has dimension %d but B has dimension %d." % (len(A.shape), len(B.shape))

    for i, l in enumerate(A.shape):
        assert l > 0, "A has length 0 in its %d dimension" % i

    for i, l in enumerate(B.shape):
        assert l > 0, "B has length 0 in its %d dimension" % i

    out_shape = tuple( i + j - 1 for (i, j) in zip(A.shape, B.shape) )
    O = np.ndarray(out_shape, dtype=A.dtype)
    N = len(A.shape)

    for O_indices in it.product(*[xrange(i) for i in O.shape]):
        accum = 0
        for A_indices in it.product(*[xrange(max(0,o-(b-1)),min(a,o+1)) for a,b,o in zip(A.shape, B.shape, O_indices)]):
            B_indices = tuple(B_i - A_i for A_i, B_i in zip(A_indices, O_indices))
            # print 'Ai: %s, Bi: %s, Oi: %s' % (A_indices, B_indices, O_indices)
            accum += A[A_indices] * B[B_indices]
        O[O_indices] = accum
    return O

# This is acutally unused, but left here in case it is needed in the future
def natural_number_sum(n, s):
    '''Returns a generator which yields all tuples of n natural numbers which
    sum to s (0 is a natural number)'''
    numbers = [0 for i in xrange(n)]
    numbers[0] = s
    while True:
        yield tuple(numbers)
        carry = numbers[n-1]
        numbers[n-1] = 0
        done = True
        for i in xrange(n-2,-1,-1):
            if numbers[i] != 0:
                numbers[i] -= 1
                numbers[i+1] = carry + 1
                done = False
                break
        if done:
            return

def run_tests():
    print 'Running tests ...'
    A = np.array([1, 2])
    B = np.array([4, 2])
    C = np.array([4, 5, 6, 7])
    D = np.array([[1,1],
                  [1,1]])
    E = np.array([[1,2],
                  [1,1]])
    def check(A, B):
        assert (convolve(A, B) == np.convolve(A,B)).all()
        check2(A, B)
    def check2(A, B):
        assert (convolve_py(A, B) == convolve(A, B)).all()
    check2(D, E)
    check(A, B)
    check(B, A)
    check(A, C)
    check(C, A)
    check(B, C)
    check(C, B)
    print 'Done with tests!'

if __name__ == '__main__':
    run_tests()
