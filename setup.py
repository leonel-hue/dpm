from setuptools import setup, Extension, find_packages
import os
from distutils.command.build_ext import build_ext
from Cython.Build import cythonize
import subprocess
from pathlib import Path

# [build-system]
# requires = [
#   "setuptools >= 40.9.0",
# ]
# build-backend = "setuptools.build_meta"

class BuildExt(build_ext):
    def build_extension(self, ext):
        # Compile .asm files using NASM (for Windows)
        print('in build')
        print('ext sources: ', ext.sources)

        # Keep track of which sources are compiled manually
        asm_sources = []

        for source in ext.sources:
            print('in sources', source)
            if source.endswith('.asm'):
                print('file: ', source)

                # Get the full path of the .asm file
                asm_file = Path(source).resolve()  # Get absolute path to the .asm file
                print('asm file (absolute path): ', asm_file)
                
                # Define the output object file (.obj)
                obj_file = asm_file.with_suffix('.obj')
                print(f"Compiling assembly file {source}...")

                # NASM command to assemble the .asm file (use win64 format for Windows)
                nasm_command = ["nasm", "-f", "win64", str(asm_file), "-o", str(obj_file)]
                print("nasm command:", ' '.join(nasm_command))  # Print the full command
                
                try:
                    subprocess.check_call(nasm_command)  # Compile the .asm file
                    # Add the object file to extra_objects
                    ext.extra_objects.append(str(obj_file))  # Add the object file to the extension's extra_objects list
                    # Track the asm file as handled manually
                    asm_sources.append(source)
                except subprocess.CalledProcessError as e:
                    print(f"Error during compilation of {source}: {e}")
                    return  # Exit if there is an error in compilation

        # Remove the .asm sources from ext.sources as they are already compiled
        ext.sources = [source for source in ext.sources if source not in asm_sources]

        print('ext sources: ', ext.sources)

        # Call the default build_ext for remaining sources (like .c files)
        super().build_extension(ext)

# asm_module = Extension(
#     name="cache",
#     sources=["cache.c", "cache.asm"],
#     extra_compile_args=['-O3', '-fPIC'],
#     # cmdclass={'build_ext': build_ext_with_asm}
#     # extra_link_args=[],
# )

setup(
    name="dpm",
    version="1.0",
    description="using cache in assembly",
    packages= find_packages(),
    author= "Leonel Taffouo",
    author_email= "leonelbr2001@gmail.com",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    # package_dir={'': 'src'},
    # entry_points={
    #     'console_scripts': [
    #        'cache = dpm.cache:prefetch_function'
    #     ]
    # },
    # ext_modules=cythonize([asm_module]),
    cmdclass={'build_ext': BuildExt},
    ext_modules=[Extension(
    name="cache",
    sources=["cache.asm", "cache.c"],
    extra_compile_args=['-O3', '-fPIC'],
    # extra_link_args=[],
)],
)

# $ gcc -shared -o prefetch.so -fPIC prefetchmodule.c prefetch_iter.o $(python3-config --includes --ldflags) -lkernel32 -m64 -Wl,--subsystem,windows

# gcc -shared -fPIC asmaddmodule.c add.o -I/usr/include/python3.11 -o asmadd.so

# twine upload dist/*
# pip install your_package_name

# "C:\msys\home\dist\dpm-1.0-cp310-cp310-win_amd64.whl"
