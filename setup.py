from setuptools import setup, find_namespace_packages

setup(
    name='clib',
    version='1.0.0',
    description='This project is a console application, developed for keeping contact details, notes, '
                'and for searching, editing, and sorting the data.',
    url='https://github.com/InSmartGroup/GoIT_Team_Project',
    author='Yuliia Didenko, Gregory Ostapenko, Kostiantyn Gorishnyi, Taras Barskyi, Maksim Nesterovskyi',
    author_email='yu_lyan@ukr.net, asahitora@gmail.com, ksgorishniy@gmail.com, barskyi69@gmail.com, maxwel842@gmail.com',
    license='MIT',
    include_package_data=True,
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['clib=clib.main:main']}
)
