import numpy

class bndarray(object):
    def __init__(self,shape,block_shape,storage=None):
        self.shape=shape
        self.block_shape=block_shape

        # example: blocked matrix
        # shape=(3,6)
        # block_shape=((2,4,5),(1,1,4,0,5,6))
        # npshape=(11,17)
        _npshape=npshape(shape, block_shape)
        
        if storage is not None:
            self.storage=storage
        else:
            self.storage=numpy.empty(_npshape)

    def __setitem__(self,block_index,item):
        self.storage[npindex(block_index,self.block_shape)]=item
        
    def __getitem__(self,block_index):
        return self.storage[npindex(block_index,self.block_shape)]

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
    _npindex=[None]*len(block_index)
    for i in range(len(block_index)):
        bstart=sum(block_shape[i][:block_index[i]])
        bstop=bstart+block_shape[i][block_index[i]]
        _npindex[i]=slice(bstart,bstop)
    return tuple(_npindex)
    
def npshape(shape, block_shape):
    _npshape = [None]*len(shape)
    for i in range(len(shape)):
        _npshape[i]=sum(block_shape[i])
    return tuple(_npshape)

def asarray(ba):
    return ba.storage

def asbarray(a, shape, block_shape):
    return bndarray(shape, block_shape, a)

def zeros(shape, block_shape):
    _npshape=npshape(shape, block_shape)
    return bndarray(shape, block_shape, numpy.zeros(_npshape))
    
def eye(N, block_N):
    """
    # example: blocked matrix
    N=4
    block_N=(3,1,2,0)
    shape=(4,4)
    block_shape=((3,1,2,0),(3,1,2,0))
    assert npshape=(6,6)
    """
    shape=[N,N]
    block_shape=(block_N,block_N)
    ba=zeros(shape,block_shape)

    for i in range(ba.shape[0]):
        ba[i,i]=numpy.eye(ba.block_shape[0][i])
    return ba
