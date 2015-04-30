#!/usr/bin/env python
#
# Peter.Kutschera@ait.ac.at, 2015-04-15
#
# Increment the number in a file
# Return the new number
# Reentrent


import fcntl
import errno
import os
import os.path
import time
import cgi
import cgitb

datadir = "/home/martin/icmm/data/CRISMA/"
datadir = "/icmmdata/CRISMA/"
entities = datadir + "entities/"
ids = datadir + "ids/"


def getInitValue (clazz):
    n = 0
    if os.path.exists (entities + clazz):
        l = os.listdir (entities + clazz)
        for i in l:
            try:
                x = int (i)
                if x > n:
                    n = x
            except Exception as e:
                print e
    return n

def isIdUsed (clazz, id):
    return os.path.exists ("{0}{1}/{2}".format (entities, clazz, id))

def nextIdFromFile (clazz):
    try:
        if not os.path.exists (ids):
            os.mkdir (ids)
        f = open (ids + clazz, "r+")
        fcntl.lockf(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        s = f.readline()
        if len (s) == 0:
            n = getInitValue (clazz)
        else:
            n = int (float (s))
        n += 1
        while isIdUsed (clazz, n):
            n = getInitValue (clazz)
            n += 1
        f.seek (0)
        f.write ("{0}".format (n))
        f.close()
        return n
    except IOError as e:
        if e.errno == errno.ENOENT:
            open (ids + clazz,"a").close()
        return None

def nextId (clazz):
    for i in range (5):
        n = nextIdFromFile (clazz)
        if n != None:
            return n
        time.sleep (i)


if __name__ == "__main__":
    cgitb.enable()
    form = cgi.FieldStorage()
    if ('class' not in form):
        print ("Content-Type: text/plain")
        print ("Status: 501")
        print 
        print ("Missing parameter 'class'")
    else:
        clazz = form["class"].value
        n = nextId (clazz)
        if n == None:
            print ("Content-Type: text/plain")
            print ("Status: 502")
            print 
            print ("Could not generate an new id for 'class'")
        else:
            print ("Content-Type: application/json")
            print 
            print ('{{"class":"{0}","nextId":{1}}}'.format (clazz, n)) 
