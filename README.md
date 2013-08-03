PassTest
========

This is a simple beginning for some kind of library which saves
password hashes in a relativly secure fashion. It actually saves a csv
with a name (could be username or other identifier) and a sha1 hash
and some salt.

When the class `Hashes` is initialized you have an object which
relates to a csv file (by default ~/.PassTest).

With this object you can store, retrieve and test passwords.

Usage
-----

### Initialize

    >>> from PassTest import Hashes
    >>> hashes = Hashes()

### Create a few entries in the csv file

    >>> hashes.new('SomeIdentifier', 'SomePassword')
    >>> hashes.new('AnotherIdentifier', 'AnotherPassword')
    >>> hashes.save()
    
### Show me what you got

    >>> hashes.items()
    {'AnotherIdentifier': <Hash instance: AnotherIdentifier>, 'SomeIdentifier': <Hash instance: SomeIdentifier>}

### Test a pass

    >>> another_identifier = hashes.get('AnotherIdentifier')
    >>> another_identifier.test_passwd('HelloWorld')  # Ouupps, wrong password
    False
    >>> another_identifier.test_passwd('AnotherPassword')  # Got it right this time
    True

Example csv file
----------------

    $ cat ~/.PassTest 
    AnotherIdentifier,5719c3ea07686676b7805fe31d2d5da85d40ee30,J6+AZ2eUlY+m5h0KMyd2RhY9Zr4AMGCKooSaKLU6utw=
    SomeIdentifier,e404592eb910ba65e7e7faae66910f0e9c786d5e,61KycIDKTwmVzEiCU2/sKM0Ws3TqDq9Zuj3i5x83XTY=
