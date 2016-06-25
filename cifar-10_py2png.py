# This script converts the cifar-10 dataset from python format to png
# This script also generates two text files (one for the training set and another for the test set)
# containing the correct label of each image

# Example:
#       python2.7 cifar-10_py2png.py cifar-10-batches-py

# author: Tiago Santana de Nazare (tiagosn92 [at] gmail [dot] com)

import os
import sys
import cPickle
import cv2

# source of unpickle function: https://www.cs.toronto.edu/~kriz/cifar.html
def unpickle(file):
    fo = open(file, 'rb')
    dict = cPickle.load(fo)
    fo.close()

    return dict

def array2im(a):
    r = a[0:1024].reshape((32,32))
    g = a[1024:2048].reshape((32,32))
    b = a[2048:3072].reshape((32,32))

    return cv2.merge((b,g,r))

def convetBatch(batch, dsFolder, batchFolder, textFile):
    batchPath = dsFolder + '/' + batchFolder
    print batchPath
    if not os.path.isdir(batchPath):
        print 'aaaaaaa'
        os.makedirs(batchFolder)

    for j in xrange(0, batch['data'].shape[0]):
        im = array2im(batch['data'][j])
        imFile = batchPath + '/' + batch['filenames'][j]
        cv2.imwrite(imFile, im)

        imRelativePath =  batchFolder + '/' + batch['filenames'][j]
        textFile.write(imRelativePath + ' ' + str(batch['labels'][j]) + '\n')

    return

folder = sys.argv[1] # original (python format) cifar-10 folder

dsFolder = 'cifar-10_png' # new dataset (png format) folder

if not os.path.isdir('cifar-10_png'):
    os.makedirs('cifar-10_png')

textFile = open('cifar-10_png/train_cifar-10.txt', 'w')
for i in xrange(1, 6):
    batch = unpickle(folder + '/data_batch_' + str(i))
    batchFolder = 'png_data_batch_' + str(i)
    convetBatch(batch, dsFolder, batchFolder, textFile)
textFile.close()

textFile = open('cifar-10_png/test_cifar-10.txt', 'w')
batch = unpickle(folder + '/test_batch')
batchFolder = 'png_test_batch'
convetBatch(batch, dsFolder, batchFolder, textFile)
textFile.close()
