from pythonforandroid.recipe import CythonRecipe


class MsgPackRecipe(CythonRecipe):
    version = '1.0.7'
    url = 'https://files.pythonhosted.org/packages/source/m/msgpack/msgpack-{version}.tar.gz'
    depends = ["setuptools"]
    call_hostpython_via_targetpython = False


recipe = MsgPackRecipe()
