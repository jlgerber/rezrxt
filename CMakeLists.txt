cmake_minimum_required(VERSION 2.8)
#
# simplest install ever. Since all we want is to have the package.py
# copied over to the install directory....
include(RezBuild)

file(GLOB_RECURSE py_files "python/*.py")
rez_install_python(
    py
    FILES ${py_files}
    DESTINATION .
)

file(GLOB bin_files "bin/*")
rez_install_files(
    ${bin_files}
    DESTINATION .
    EXECUTABLE
)
