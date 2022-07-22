from setuptools import setup, find_packages

setup(
    name="fpvs",
    description="Fast Python Vulnerability Scanner",
    long_description=open("README.md", 'r').read(),
    long_description_content_type='text/markdown',

    author="Klaas van Schelven",
    project_urls={
        "Github": "https://github.com/vanschelven/fpvs/",
    },

    python_requires='>=3.7.*',

    install_requires=[
        "wheel-filename",
        "packaging",
        "pyyaml",
    ],

    packages=find_packages(),

    setup_requires=["setuptools_scm"],
    use_scm_version={
        "write_to": "fpvs/scmversion.py",
        "write_to_template": "__version__ = '{version}'\n",
    },

    include_package_data=True,

    entry_points={
        'console_scripts': [
            'fpvs-scan=fpvs.scripts.scan:main',
        ],
    },

    license="BSD-3-Clause",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
    ],
)
