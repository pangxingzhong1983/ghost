from pythonforandroid.recipe import CompiledComponentsPythonRecipe


class PyuvRecipe(CompiledComponentsPythonRecipe):
    version = '1.4.0'
    url = 'https://pypi.python.org/packages/source/p/pyuv/pyuv-{version}.tar.gz'
    site_packages_name = 'pyuv'
    depends = ['python3']
    call_hostpython_via_targetpython = False
    patches = [
        'android-target-platform.patch',
        'py311-refcnt.patch',
    ]

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        env['PYUV_TARGET_PLATFORM'] = 'android'
        return env


recipe = PyuvRecipe()
