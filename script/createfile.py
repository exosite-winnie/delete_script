#!/usr/bin/env python
import os
import sys

class create_file(object):
    def create_specified_size_file(self, fileName, size):
      base = 1024
      s = size[-2:]
      if s == "KB":
        byte = int(size[:1])*pow(base,1)
      if s == "MB":
        byte = int(size[:1])*pow(base,2)
      if s == "GB":
        byte = int(size[:1])*pow(base,3)
      file = "/Users/winnie/Desktop/{}".format(fileName, byte)
      f = open(file, "wb")
      f.write(os.urandom(int(byte)))
      f.close()
      print 'size: ' + str(os.stat(file).st_size)

fileName = sys.argv[1]
size = sys.argv[2]
create_file().create_specified_size_file(fileName, size)