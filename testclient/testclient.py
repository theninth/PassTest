#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from getpass import getpass
from passtest import Hashes

# Create main object for passtest
hashes = Hashes()

def test_passwd(name):
    passwd = getpass()
    h = hashes.get(name)
    if h.test_passwd(passwd):
        print 'Yeah! That was the right password baby'
    else:
        print 'Sorry, that was not the right password!'

def add_passwd(name):
    while True:
        passwd1 = getpass()
        passwd2 = getpass('Again: ')  # Confirmation
        if passwd1 == passwd2:
            hashes.new(name, passwd1)
            hashes.save()
            break
        else:
            print '\nPassword mismatch. Try again...\n'

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Test app for passtest')
    parser.add_argument('-a', '--add', help='Adds an entry in database', action='store_true')
    parser.add_argument('-n','--name', help='Identifier for password')
    parser.add_argument('-l','--list', help='List passwd id:s', action='store_true')
    parser.add_argument('-t', '--test', help='Tests if password matches hash', action='store_true')

    args = vars(parser.parse_args())

    # Run list argument
    if args['list']:
        for name in hashes.items():
            print name

    # run test argument
    elif args['test']:
        if args['name']:
            try:
                test_passwd(args['name'])
            except ValueError:
                print 'Hash not found!'
        else:
            print 'This option is only available with the --name argument'

    # run add argument
    elif args['add']:
        if args['name']:
            add_passwd(args['name'])
        else:
            print 'This option is only available with the --name argument'

if __name__ == '__main__':
    main()
