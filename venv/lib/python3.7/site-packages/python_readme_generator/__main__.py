#!/usr/bin/env python
"""generate README.md"""
import click
import os
import python_readme_generator
import sys

MODULE_NAME = "python_readme_generator"
PROG_NAME = 'python -m %s' % MODULE_NAME
USAGE = 'python -m %s [location ...]' % MODULE_NAME


@click.command()
@click.argument('locations', nargs=-1, required=True)
def _cli(locations):
    readme = python_readme_generator.Readme()
    for path in locations:
        if not os.path.exists(path):
            sys.exit("ERROR: %s NOT EXISTS")
        readme.load(path)
    string = readme.render()
    if string:
        print(string)


if __name__ == '__main__':
    _cli(prog_name=PROG_NAME)
