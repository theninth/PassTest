#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import wx
from getpass import getpass
from passtest import Hashes

# Create main object for passtest
hashes = Hashes()

# GUI Stuff
class MainFrame(wx.Frame):
    """Handles a GUI password tester"""
    def __init__(self, name, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.label = wx.StaticText(self, -1, "")
        self.panel = wx.Panel(self, -1)
        self.ok_button = wx.Button(self, -1, "OK")

        # Build layout and set properties of frame
        self.SetTitle("PassTest")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.label, 0, wx.EXPAND, 0)
        sizer.Add(self.panel, 1, wx.EXPAND, 0)
        sizer.Add(self.ok_button, 0, wx.EXPAND, 0)
        self.SetSizer(sizer)
        sizer.Fit(self)
        self.Layout()

        # Bindings
        self.Bind(wx.EVT_BUTTON, self.OnExitApp, self.ok_button)
        self.Bind(wx.EVT_CLOSE, self.OnExitApp)

        # Password dialog
        box = wx.PasswordEntryDialog(None, 'Please type the password for: ' + name,
                                 'Password')
        
        # On Password box OK
        if box.ShowModal() == wx.ID_OK:
            passwd = box.GetValue()
            h = hashes.get(name)
            
            # Correct password
            if h.test_passwd(passwd):
                self.label.SetLabel('Correct!')
            # Incorrect password
            else:
                self.label.SetLabel('Incorrect!')
            box.Destroy()
        
        # On Password box cancel
        else:
            self.Destroy()
            sys.exit(0)

    def OnExitApp(self, event):  
        self.Destroy()
        sys.exit(0)


# Generic functions
def test_passwd(name):
    passwd = getpass()
    h = hashes.get(name)
    if h.test_passwd(passwd):
        print 'Yeah! That was the right password baby'
    else:
        print 'Sorry, that was not the right password!'

def gui_test_passwd(name):
    app = wx.App(0)
    frame = MainFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()

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
    parser.add_argument('-g', '--guitest', help='GUI Test if password matches hash - EXPERIMENTAL', action='store_true')

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

    # run gui test argument
    elif args['guitest']:
        if args['name']:
            app = wx.App(0)
            frame = MainFrame(args['name'], parent=None, id=-1)
            frame.Show()
            app.MainLoop()
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
