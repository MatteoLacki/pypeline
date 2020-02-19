# This Python file uses the following encoding: utf-8
from setuptools import setup, find_packages

setup(
    name='vodkas',
    packages=find_packages(),
    version='0.0.2',
    description='Syntactic sugar around Waters LC/IMS/MS pypeline.',
    long_description='A simple, once for all pythonic middle finger in face of Waters. Works under fucking Windows only.',
    author='Mateusz Krzysztof Łącki',
    author_email='matteo.lacki@gmail.com',
    url='https://github.com/MatteoLacki/vodkas',
    keywords=[  'Mass Spectrometry',
                'Waters'
                'Symphony Pipeline',
                'fucking pipeline'],
    classifiers=[   'Development Status :: 1 - Planning',
                    'License :: OSI Approved :: BSD License',
                    'Intended Audience :: Science/Research',
                    'Topic :: Scientific/Engineering :: Chemistry',
                    'Programming Language :: Python :: 3.6',
                    'Programming Language :: Python :: 3.7',
                    'Programming Language :: Python :: 3.8'],
    license="GPL-3.0-or-later",
    install_requires=['pandas',
                      'docstr2argparse',
                      'fs_ops',
                      'waters'],
    # include_package_data=True,
    # package_data={'data': ['data/contaminants_uniprot_format.fasta']},
    scripts = ["bin/APEX3D.py",
               "bin/PEPTIDE3D.py",
               "bin/PLGS.py",
               "bin/REDO_SEARCH.py",
               "bin/PLGS_2.py",]
)
