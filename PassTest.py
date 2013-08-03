#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import csv
import os
from hashlib import sha1

FILENAME = os.path.expanduser('~/.PassTest')

class Hashes():
    """Handling hashes in hashes file"""
    class Hash():
        def __init__(self, name=None, hex_hash=None, salt=None):
            self.name = name
            self.hex_hash = hex_hash
            self.salt = salt

        def __unicode__(self):
            return unicode(self.name)

        def __repr__(self):
            return u'<Hash instance: ' + self.__unicode__() + u'>'

        def generate(self, passwd, salt_length=32):
            # Set salt
            self.salt = os.urandom(salt_length)
            
            # Set hash (as hexdigest)
            h = sha1(passwd)
            h.update(self.salt)
            self.hex_hash = h.hexdigest()

        def test_passwd(self, passwd):
            """
            Returns True if password is correct False otherwise.
            """
            h = sha1(passwd)
            h.update(self.salt)
            return h.hexdigest() == self.hex_hash
            
        def get_b64salt(self):
            return base64.b64encode(self.salt)
                     
    def __init__(self):
        self._hashes = {}
        self.load()
    
    def new(self, name, passwd):
        new_hash = self.Hash(name=name)
        new_hash.generate(passwd=passwd)
        self._hashes[name] = (new_hash.hex_hash, new_hash.salt)

    def items(self):
        hash_objs = {}
        for name, data in self._hashes.iteritems():
            hex_hash, salt = data
            hash_obj = self.Hash(name=name, hex_hash=hex_hash, salt=salt)
            hash_objs[name] = hash_obj
        return hash_objs

    def get(self, name):
        if name in self._hashes:
            hex_hash, salt = self._hashes[name]
            return self.Hash(name=name, hex_hash=hex_hash, salt=salt)
        else:
            raise ValueError
            
    def load(self, fname=FILENAME):
        """
        Read in hashes from csv file in format:
        `name, hash, base64 encoded salt`
    
        set self._hashes dict to format `name: (hash, salt)`
        """

        with open(fname, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            for line, row in enumerate(reader, 1):
                if len(row) == 3:
                    name, hex_hash, b64salt = row
                    salt = base64.b64decode(b64salt)
                    self._hashes[name] = (hex_hash, salt)
                else:
                    print u'ERROR: Wrongly formatted line %s.' % (line,)

    def save(self, fname=FILENAME):
        """
        Write hashes to csv file in format:
       `name, hash, base64 encoded salt`
        """
        with open(fname, 'wb') as csvfile:
            writer = csv.writer(csvfile)
            for name, h in self.items().iteritems():
                writer.writerow([name, h.hex_hash, h.get_b64salt()])
