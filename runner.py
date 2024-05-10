#!/usr/bin/env python
import subprocess
import argparse
from os.path import splitext
from os.path import isdir
from os.path import isfile
from os.path import basename
from os.path import join
from os import listdir
from os import getcwd
from platform import system as os
from time import time_ns

class Program:
    source = ""
    verbosity = 1
    cmd = [str]
    def compile(self):
        print("The compilation for this language is not yet implemented")
        exit(12)
    def test(self):
        cwd = getcwd()
        input_dir = join(cwd, "input")
        output_dir = join(cwd, "output")
        if (not isdir(input_dir) or not isdir(output_dir)):
            print("Input folder or output folder are missing")
            exit(10)
        try:
            files = listdir(input_dir)
        except RuntimeError(e):
            print("There was a problem opening your input folder:")
            print(e)
            exit(11)
        total: int = 0
        passed: int = 0
        startTime: int = 0
        subTime: int = 0
        totalTime: int = 0
        print("Testing your program!")
        for file in files:
            input_file = join(input_dir, file)
            output_file = join(output_dir, file)
            if not isfile(input_file) or not isfile(output_file):
                continue
            total += 1
            result: subprocess.CompletedProcess[bytes]
            with open(input_file, "r") as test_file:
                startTime = time_ns()
                result = subprocess.run(
                    self.cmd,
                    stdin=test_file,
                    stdout=subprocess.PIPE)
                subTime = time_ns() - startTime
                totalTime += subTime
            with open(output_file, "rb") as expected_file:
                expected = expected_file.read()
                actual = result.stdout.replace(b"\r", b"")  # Fuck windows
                if expected == actual:
                    passed += 1
                    if self.verbosity >= 2:
                        print("Time to run in ms:", str(subTime / 1_000_000))
                else:
                    if self.verbosity >= 3:
                        print("ERROR IN TEST:", file)
                        print("Expected:")
                        print(expected)
                        print("Actual:")
                        print(actual)
                        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
                    if result.returncode != 0:
                        break
        if total == 0:
            print(files)
            print("no inputs found")
        else:
            if self.verbosity >= 2:
                print(passed, "/", total, " tests passed!", sep="")
                print("Total time in ms:", totalTime / 1_000_000)
            if passed == total:
                print("✅ Every test passed! Congratulations!")
            else:
                print("❌ Some tests failed...")
    def __init__(self, source: str, verbosity: int):
        self.source = source
        self.verbosity = verbosity

class C(Program):
    def compile(self):
        file, ext = splitext(self.source)
        if os() == "Windows":
            result = subprocess.run(
                ["gcc", "-o", file + ".exe", self.source])
        else:
            result = subprocess.run(
                ["gcc", "-O2", "-std=gnu11", "-lm", "-static", "-o", file + ".exe", self.source])
        if result.returncode != 0:
            print(result.stdout)
            print(result.stderr)
            exit(4)
        self.cmd = ["./" + file + ".exe"]

class Cpp(Program):
    def compile(self):
        file, ext = splitext(self.source)
        if os() == "Windows":
            result = subprocess.run(
                ["g++", "-o", file + ".exe", self.source])
        else:
            result = subprocess.run(
                ["g++", "-O2", "-lm", "-o", file + ".exe", self.source])
        if result.returncode != 0:
            print(result.stdout)
            print(result.stderr)
            exit(4)
        self.cmd = ["./" + file + ".exe"]

class Python(Program):
    def compile(self):
        if os() == "Windows":
            self.cmd.append("py")
        else:
            self.cmd.append("python3")
        self.cmd.append(self.source)

class Java(Program):
    def compile(self):
        result = subprocess.run(
            ["javac", self.source])
        if result.returncode != 0:
            print(result.stdout)
            print(result.stderr)
            exit(4)
        self.cmd = ["java", self.source]

class Rust(Program):
    def compile(self):
        file, ext = splitext(self.source)
        result = subprocess.run(
                ["rustc", "-o", file + ".exe", self.source])
        if result.returncode != 0:
            print(result.stdout)
            print(result.stderr)
            exit(4)
        self.cmd = [file + ".exe"]

def main():
    parser = argparse.ArgumentParser(description="Runner build your program and tests it against test inputs (placed in the inputs folder) and their respective outputs (placed in the outputs folder)")
    parser.add_argument(
        "-p",
        "--program",
        help="The main source file of your program",
        required=True
    )
    parser.add_argument(
        "-V",
        "--verbosity",
        help="This program has 3 levels of verbosity. 1 is the default and 3 is the highest",
        type=int,
        required=False,
        default=1,
        choices=range(1,4)
    )
    try:
        args = parser.parse_args()
    except:
        exit(69)
    filename: str = args.program
    _, ext = splitext(filename)
    program: Program = None
    if (ext == ".c"):
        program = C(filename, args.verbosity)
    elif (ext == ".cpp"):
        program = Cpp(filename, args.verbosity)
    elif (ext == ".py"):
        program = Python(filename, args.verbosity)
    elif (ext == ".java"):
        program = Java(filename, args.verbosity)
    elif (ext == ".rs"):
        program = Rust(filename, args.verbosity)
    else:
        print("File extension not supported")
        print("Supported file extensions: .java, .c, .cpp, .py, .rs")
        exit(9)
    program.compile()
    program.test()


if __name__ == "__main__":
    main()
