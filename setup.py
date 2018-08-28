from distutils.core import setup
from distutils import sysconfig
from distutils.extension import Extension
from Cython.Build import cythonize

ldshared = sysconfig.get_config_var("LDSHARED")
sysconfig._config_vars["LDSHARED"] = ldshared.replace(" -g ", "  ")

ext = [
  Extension(
    "voicesep.separators.neural.chord_level."
    "features.assignments_generator.__init__",
    [
      "voicesep/separators/neural/chord_level/"
      "features/assignments_generator/__init__.pyx",

      "voicesep/separators/neural/chord_level/"
      "features/assignments_generator/cassignments_generator.cpp"
    ],

    language="c++",
    extra_compile_args=["-std=c++11", "-O2", "-g0"],
  ),

  Extension(
    "voicesep.separators.neural.chord_level.features.levels.*",
    ["voicesep/separators/neural/chord_level/features/levels/*.pyx"],
    language="c++",
    extra_compile_args=["-std=c++11", "-O2", "-g0"],
  ),

  Extension(
    "voicesep.separators.neural.chord_level.features.__init__",
    ["voicesep/separators/neural/chord_level/features/__init__.pyx"],
    language="c++",
    include_dirs=[
      "voicesep/separators/neural/chord_level/features/assignments_generator"
    ],
    extra_compile_args=["-std=c++11", "-O2", "-g0"],
  ),
]

setup(
  ext_modules = cythonize(ext)
)
