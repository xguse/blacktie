from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()


version = '0.2.1'

install_requires = [ 'PyYAML', 'Mako', 'rpy2',
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
]


setup(name='blacktie',
    version=version,
    description="A python wrapper for analysis of RNA-seq data with the popular tophat/cufflinks pipeline.",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='scientific computing RNA-seq tophat cufflinks bowtie CummeRbund',
    author='Augustine Dunn',
    author_email='wadunn83@gmail.com',
    url='https://github.com/xguse/',
    license='GPL 3',
    packages=find_packages('src'),
    package_dir = {'': 'src'},include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['blacktie=blacktie:main',
             'blacktie-encode=blacktie.scripts.encode_mail_li_file:main',
             'blacktie-cummerbund=blacktie.scripts.cummerbund:main']
    }
)
