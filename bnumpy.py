#!/usr/bin/env python
'''
bumpy tensor library
'''

# math
import numpy
import numpy as np
import scipy
from scipy import linalg as la
from scipy import stats
import random as rnd
import cmath,math

class bndarray(object):
    def __init__(self, shape, block_shape, storage = None, dtype = None):
        self.shape = shape
        self.block_shape = block_shape
        if dtype is not None:
            self.dtype = dtype
        elif storage is not None:
            self.dtype = storage.dtype
        else:
            dtype = np.double64 
            
        # example: blocked matrix
        # shape=(3,6)
        # block_shape=((2,4,5),(1,1,4,0,5,6))
        # npshape=(11,17)
        _npshape=npshape(shape, block_shape)
        
        if storage is not None:
            storage = np.asarray(storage, dtype = self.dtype)
            self.storage = storage
        else:
            self.storage = np.empty(_npshape, dtype = self.dtype)

    def __setitem__(self, block_index, item):
        self.storage[npindex(block_index, self.block_shape)] = item
        
    def __getitem__(self, block_index):
        return self.storage[npindex(block_index, self.block_shape)]

def npindex(block_index, block_shape):
    """
    # example: blocked matrix
    shape=(3,6)
    block_shape=((2,4,5),(1,1,4,0,5,6))
    bindex=(0,0)
    assert bnumpy.npindex(bindex, block_shape)==(slice(0,2),slice(0,1))
    bindex=(1,2)
    assert bnumpy.npindex(bindex, block_shape)==(slice(2,4),slice(2,6))
    """
    _npindex = [None] * len(block_index)
    for i, bidxi in enumerate(block_index):
        bstart = sum(block_shape[i][:bidxi])
        bstop = bstart + block_shape[i][bidxi]
        _npindex[i] = slice(bstart, bstop)
    return tuple(_npindex)
    
def npshape(shape, block_shape):
    _npshape = [None] * len(shape)
    for i in xrange(len(shape)):
        _npshape[i] = sum(block_shape[i])
    return tuple(_npshape)

def asarray(ba):
    return ba.storage

def asbarray(a, shape, block_shape):
    return bndarray(shape, block_shape, a)


def empty(shape, block_shape):
    _npshape = npshape(shape, block_shape)
    return bndarray(shape, block_shape, np.empty(_npshape))


def zeros(shape, block_shape):
    _npshape = npshape(shape, block_shape)
    return bndarray(shape, block_shape, np.zeros(_npshape))
    
def eye(N, block_N):
    """
    # example: blocked matrix
    N=4
    block_N=(3,1,2,0)
    shape=(4,4)
    block_shape=((3,1,2,0),(3,1,2,0))
    assert npshape=(6,6)
    """
    assert N == len(block_N)
    shape = [N, N]
    block_shape = (block_N, block_N)
    ba = zeros(shape, block_shape)

    for i in xrange(ba.shape[0]):
        ba[i,i] = np.eye(ba.block_shape[0][i])
    return ba

def copy(ba):
    return bndarray(ba.shape, ba.block_shape, ba.storage) 





if __name__ == '__main__':
    
    print "\nmain test\n"

