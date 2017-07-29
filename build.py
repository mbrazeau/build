#!/usr/bin/env python

import  sys, os, getopt, multiprocessing, platform, shutil
from subprocess import call

class Chdir:
    def __init__(self, newdir):
        self.origdir = os.getcwd()
        print(newdir)
        os.chdir(newdir)

    def __del__(self):
        print(self.origdir)
        os.chdir(self.origdir)

def run(cmd, split=True):
    print(cmd)
    if (split == True):
        cmds = cmd.split(" ")
    else:
        cmds = cmd
    if (call(cmds)):
        sys.exit(1)

def delBuildTree(delDir):
    retries = 0
    while (os.path.exists(delDir) == True):
        shutil.rmtree(delDir, True)
        retries += 1
        if (retries > 10):
            break
    return not os.path.exists(delDir)

def makeNcl(baseDir, buildDebug, buildClean, buildVerbose, buildJobs):
    cwd = Chdir(baseDir)
    if (buildClean == True):
        run("make clean")
    run("./bootstrap.sh")
    debug = ""
    if (buildDebug == True):
        debug = " --enable-debugging"
    run("./configure --prefix=" + os.path.abspath("../install") + debug)
    run("make install -j" + buildJobs)

def cmakeBuildType(buildDebug):
    buildType = "Release"
    if (buildDebug == True):
        buildType = "Debug"
    return buildType

def cmakeBuildPosix(buildDebug, buildVerbose, buildJobs):
    cmake = "cmake .. -DCMAKE_BUILD_TYPE=" + cmakeBuildType(buildDebug)
    make = "make -j " + buildJobs + " install"
    if (buildVerbose == True):
        make += " VERBOSE=1"
    run(cmake)
    run(make)

def cmakeBuildWindows(buildDebug, buildVerbose, buildJobs):
    if ("VISUALSTUDIOVERSION" in os.environ):
        msvsVer = os.environ["VISUALSTUDIOVERSION"]
        msvsVer = msvsVer[:msvsVer.find('.')]
        if (msvsVer == "10"):
            gen = "Visual Studio 10 2010"
        elif (msvsVer == "11"):
            gen = "Visual Studio 11 2012"
        elif (msvsVer == "12"):
            gen = "Visual Studio 12 2013"
        elif (msvsVer == "14"):
            gen = "Visual Studio 14 2015"
        cmake = "cmake .. -G"
        make = "cmake --build . --target install --config " + cmakeBuildType(buildDebug)
        cmake = cmake.split(" ")
        cmake.append(gen)
        run(cmake, False)
        run(make)
    else:
        print("Unable to find VISUALSTUDIOVERSION in env, please run from MSVS command prompt")
        sys.exit(1)

def cleanTarget(buildTarget, buildClean):
    if (buildClean == True):
        delBuildTree(buildTarget)
    if (os.path.exists(buildTarget) == False):
        os.makedirs(buildTarget)

def cmakeBuild(buildDebug, buildClean, buildVerbose, buildJobs):
    buildTarget = "build/"
    cleanTarget(buildTarget, buildClean)
    c = Chdir(buildTarget)
    if (platform.system() == "Windows"):
        cmakeBuildWindows(buildDebug, buildVerbose, buildJobs)
    else:
        cmakeBuildPosix(buildDebug, buildVerbose, buildJobs)

def usage():
    print("Build the morphy software suite")
    print(" -d --debug")
    print(" -r --release")
    print(" -v --verbose")
    print(" -c --clean")
    print(" -j#")
    print(" --ncl")
    os._exit(1)

def main(argv):
    buildJobs = str(multiprocessing.cpu_count())
    buildClean = False
    buildVerbose = False
    buildDebug = False
    buildNcl = False
    args = ["help", "debug", "release", "clean", "verbose", "ncl"]
    try:
        opts, args = getopt.getopt(argv, "hdrcvj:", args)
    except getopt.GetoptError as e:
        print("Error: " + str(e))
        usage()
    for opt, arg in opts:
        if (opt in ('-h', '--help')):
            usage()
        if (opt in ('-d', '--debug')):
            buildDebug = True
        if (opt in ('-r', '--release')):
            pass
        if (opt in ('-c', '--clean')):
            buildClean = True
        if (opt in ('-v', '--verbose')):
            buildVerbose = True
        if (opt in ('-j')):
            buildJobs = arg
        if (opt in ('--ncl')):
            buildNcl = True

    if (buildClean == True):
        delBuildTree("../install")
    if ((buildNcl == True) or (os.path.exists("../install") == False)):
        makeNcl("../ncl", buildDebug, buildClean, buildVerbose, buildJobs)
    cmakeBuild(buildDebug, buildClean, buildVerbose, buildJobs)

if __name__ == "__main__":
    main(sys.argv[1:])

