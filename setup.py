from distutils.core import setup

setup(
    name='PassTest',
    version='0.1dev',
    author='Niclas Nilsson',
    packages=['passtest',],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    description='Creates and testes password hashes from file.',
    long_description=open('README.md').read(),
)
