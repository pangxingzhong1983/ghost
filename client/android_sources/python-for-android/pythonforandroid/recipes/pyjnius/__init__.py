from pythonforandroid.recipe import CythonRecipe
from pythonforandroid.toolchain import shprint, current_directory, info
from pythonforandroid.patching import will_build
import sh
import sys
from os.path import join, exists
import Cython


class PyjniusRecipe(CythonRecipe):
    version = '1.6.1'
    url = 'https://github.com/kivy/pyjnius/archive/{version}.zip'
    name = 'pyjnius'
    depends = [('genericndkbuild', 'sdl2'), 'six']
    site_packages_name = 'jnius'

    patches = [
        ('genericndkbuild_jnienv_getter.patch', will_build('genericndkbuild')),
    ]

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        # NDKPLATFORM is our switch for detecting Android platform, so can't be None
        env['NDKPLATFORM'] = "NOTNONE"
        return env

    def prebuild_arch(self, arch):
        super().prebuild_arch(arch)
        utils_path = join(self.get_build_dir(arch.arch), 'jnius', 'jnius_utils.pxi')
        if not exists(utils_path):
            return

        with open(utils_path, 'r', encoding='utf-8') as f:
            data = f.read()

        if 'long = int' in data:
            return

        marker = 'cdef parse_definition'
        if marker not in data:
            return

        before, after = data.split(marker, 1)
        before = before.rstrip() + '\n\ntry:\n    long\nexcept NameError:\n    long = int\n\n'
        with open(utils_path, 'w', encoding='utf-8') as f:
            f.write(before + marker + after)

        build_dir = self.get_build_dir(arch.arch)
        config_path = join(build_dir, 'jnius', 'config.pxi')
        if not exists(config_path):
            cython3 = str(Cython.__version__).startswith('3.')
            with open(config_path, 'w', encoding='utf-8') as cfg:
                cfg.write(
                    "DEF JNIUS_PLATFORM = 'android'\n\n"
                    f"DEF JNIUS_CYTHON_3 = {int(cython3)}"
                )

        c_file = join(build_dir, 'jnius', 'jnius.c')
        if not exists(c_file):
            info('Generating C sources for pyjnius')
            with current_directory(build_dir):
                shprint(
                    sh.Command(sys.executable), '-m', 'cython',
                    join('jnius', 'jnius.pyx')
                )

    def postbuild_arch(self, arch):
        super().postbuild_arch(arch)
        info('Copying pyjnius java class to classes build dir')
        with current_directory(self.get_build_dir(arch.arch)):
            shprint(sh.cp, '-a', join('jnius', 'src', 'org'), self.ctx.javaclass_dir)


recipe = PyjniusRecipe()
