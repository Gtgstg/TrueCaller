#!/usr/bin/env python
import inspect
import os
import public
import readme_docstring
import readme_generator
import setupcfg

XDG_CONFIG_HOME = os.getenv("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
PYTHON_README_GENERATOR_HOME = os.getenv("PYTHON_README_GENERATOR_HOME", os.path.join(XDG_CONFIG_HOME, "python-readme-generator"))

ORDER = ["install", "classes", "functions"]


@public.add
class Readme(readme_generator.Readme):
    """methods: `getmodules()`, `getclasses()`, `getfunctions()`. methods as sections: `install()`, `classes()`, `functions()`"""
    locations = readme_generator.Readme.locations + [PYTHON_README_GENERATOR_HOME]
    order = ORDER

    def getmodules(self):
        if os.path.exists("setup.cfg"):
            return setupcfg.getmodules()
        return []

    def getclasses(self):
        result = []
        for module in self.getmodules():
            for name, member in inspect.getmembers(module, inspect.isclass):
                if name in getattr(module, "__all__", []):
                    result.append(member)
        return result

    def getfunctions(self):
        result = []
        for module in self.getmodules():
            for name, member in inspect.getmembers(module, inspect.isroutine):
                if name in getattr(module, "__all__", []):
                    result.append(member)
        return result

    def getname(self):
        if os.path.exists("setup.cfg"):
            metadata = setupcfg.load().get("metadata", {})
            return metadata.get("name")
        return os.popen("python setup.py --name").read().strip()

    def pip_install(self):
        if not os.path.exists("setup.py"):
            return
        return """```bash
$ [sudo] pip install %s
```""" % self.getname()

    def install(self):
        return self.pip_install()

    def classes(self):
        classes = self.getclasses()
        if classes:
            return readme_docstring.Classes(classes)

    def functions(self):
        functions = self.getfunctions()
        if functions:
            return readme_docstring.Functions(functions)
