# This Python file uses the following encoding: utf-8
from setuptools import setup, find_packages

setup(
    name='vodkas',
    packages=find_packages(),
    version='0.0.1',
    description='Syntactic sugar around Waters LC/IMS/MS pypeline.',
    long_description='A simple, once for all pythonic middle finger in face of Waters. Works under Windows only for now.',
    author='Mateusz Krzysztof Łącki',
    author_email='matteo.lacki@gmail.com',
    url='https://github.com/MatteoLacki/vodkas',
    # download_url='https://github.com/MatteoLacki/MassTodonPy/tree/GutenTag',
    keywords=[
        'Mass Spectrometry',
        'Waters'
        'Symphony Pipeline',
        'Going insane because of a fucking pipeline'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Programming Language :: Python :: 3.6'],
    license="GPL-3.0-or-later",
    install_requires=['pandas',
                      'docstr2argparse'],
    # include_package_data=True,
    # package_data={'data': ['data/contaminants_uniprot_format.fasta']},
    scripts = ["bin/APEX3D",
               "bin/PEPTIDE3D",
               "bin/PLGS"
               ]
)
