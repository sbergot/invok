from distutils.core import setup

setup(
    name='Invok',
    version='0.1.0',
    author='Simon Bergot',
    author_email='simon.bergot+invok@gmail.com',
    packages=['invok', 'invok.test'],
    url='http://pypi.python.org/pypi/Invok/',
    license='LICENSE.txt',
    description='Minimalist dependency injection for python',
    long_description=open('README.md').read(),
)
