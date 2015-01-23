#!/usr/bin/env python
# encoding: utf-8
"""

    wrapper for tarfile
    ~~~~~~~~
    tar.py
"""

import os.path as osp
from zipfile import ZipFile, ZIP_DEFLATED
from tarfile import TarFileCompat, TAR_PLAIN, TAR_GZIPPED



class Tar(object):
    """
    compress files as tar, tgz, zip
    """
    suffix = ('TAR', 'tar')
    comp_map = {
        'tar': TAR_PLAIN,
        'gz' : TAR_GZIPPED,
        'bz2': TAR_GZIPPED,
        'zip': ''
    }
    def __init__(self, dst_file, mode='w', password=None):
        self.__dst_file = dst_file
        __suffix = self.suffix
        __comp = self.comp_map.get(__suffix)
        if __suffix != 'zip':
            self.__tar = TarFileCompat(self.__dst_file, mode=mode, compression=__comp)
        else:
            self.__password = password
            self.__tar = ZipFile(self.__dst_file, mode, ZIP_DEFLATED)
            if isinstance(password, basestring):
                self.__tar.setpassword(password)  #can be only effective when reading
    
    @property
    def suffix(self):
        tmp = self.__dst_file.split('.')[-1].lower()
        if tmp == 'tgz' or self.__dst_file.endswith('.tar.gz'):
            return 'gz'
        if tmp in self.comp_map.keys():
            return tmp
        return 'tar'
    
    @property
    def namelist(self):
        return self.__tar.namelist()
    
    @property
    def infolist(self):
        return self.__tar.infolist()
    
    def getinfo(self, filename):
        return self.__tar.getinfo(filename)

    @property
    def dstfile(self):
        return self.__dst_file
    
    def compress(self, files):
        for filename in files:
            if not filename or not osp.isfile(filename):
                continue
            self.__tar.write(filename, arcname=osp.basename(filename))
        return self.__dst_file

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.__tar.close()

