#! /usr/bin/env python3

import subprocess
import os
import sys
import re
import yaml

GREEN = '\033[92m'
RED = '\033[91m'
BOLD = "\033[1m"
ENDC = '\033[0m'

FNULL = open(os.devnull, 'w')
FILE_REGEX = re.compile(".*\.s")

def default_comparator(content, expected):
    return content == expected

def yaml_comparator(content, expected):
    yc = yaml.load(content)
    ye = yaml.load(expected)
    if len(yc) != len(ye):
        return False
    if set(yc.keys()) != set(ye.keys()):
        return False

    for k, v in yc.items():
        if isinstance(v, list):
            cs = sorted(v, key=lambda dic: dic["name"])
            es = sorted(ye[k], key=lambda dic: dic["name"])
            if cs != es:
                return False
        else:
            if v != ye[k]:
                return False
    return True

# (test_category_name, expected_return_code, flags, check_stdout, check_stderr)
TEST_DIRS = [
        ("good", 0, "", False, False, [], default_comparator),
        ("good", 0, "-A", True, False, [], default_comparator),
        ("good", 0, "-e", False, False, ["pop-m", "pop-r", "pop-t", "jno",
                                         "jns", "jne", "jnz", "jnb", "jae",
                                         "jnc", "ja", "jnbe", "jge", "jnl",
                                         "jle", "jng", "jg", "jngle", "jnp",
                                         "jmp", "leave", "call", "ret",
                                         "ret-i"],
                                         default_comparator),
        ("cpu", 0, "-Y", True, False, [], yaml_comparator),
        ]

def print_good(string):
    print(BOLD + GREEN + string + ENDC)

def print_fail(string):
    print(BOLD + RED + string + ENDC)

def print_bold(string):
    print(BOLD + string + ENDC)

def read_file(path):
    with open(path, 'r') as my_file:
        return my_file.read()

class test:
    def __init__(self, name, file_name, test_dir):
        self.name = name
        self.full_file_name = test_dir + file_name
        self.expected_out = None
        self.expected_err = None
        self.expected_ret = None

        out_path = "{0}{1}.out".format(test_dir, name)
        if os.path.exists(out_path):
            self.expected_out = read_file(out_path)

        err_path = "{0}{1}.err".format(test_dir, name)
        if os.path.exists(err_path):
            self.expected_err = read_file(err_path)

        ret_path = "{0}{1}.ret".format(test_dir, name)
        if os.path.exists(ret_path):
            self.expected_ret = read_file(ret_path)

    def run(self, flags, check_out = False, check_err = False,
                  comparator = default_comparator):
        sub = None
        if flags != "":
            sub = subprocess.Popen(["./bin/nolimix86", flags,
                                   self.full_file_name], stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   universal_newlines=True)
            sub.wait()
            (pstdout, pstderr) = sub.communicate()
        else:
            sub = subprocess.Popen(["./bin/nolimix86", self.full_file_name],
                                   stdout=FNULL, stderr=FNULL,
                                   universal_newlines=True)
            sub.wait()

        out_ko = check_out and self.expected_out and not(comparator(self.expected_out, pstdout))
        err_ko = check_err and self.expected_err and self.expected_err != pstderr
        ret_ko = self.expected_ret and self.expected_ret != sub.returncode

        return (out_ko, err_ko, ret_ko, sub.returncode)

class suite:
    def __init__(self):
        self.failed = 0
        self.passed = 0

    def call_on_dir(self, test_dir, expected_ret, flag, check_out, check_err,
                    ignore, comparator):
        for file_name in sorted(filter(FILE_REGEX.match, os.listdir(test_dir))):
            # Normalize the names.
            test_name = os.path.splitext(file_name)[0]
            if test_name in ignore:
                continue

            # Create and run the test.
            new_test = test(test_name, file_name, test_dir)
            (out_ko, err_ko, ret_ko, ret) = new_test.run(flag, check_out,
                                                         check_err, comparator)
            # Output results.
            if out_ko:
                print_fail("{0}\t-- OUT".format(test_name))
                self.failed += 1
            elif err_ko:
                print_fail("{0}\t-- ERR".format(test_name))
                self.failed += 1
            elif ret_ko:
                print_fail("{0}\t-- RET : {1}".format(test_name, ret))
                self.failed += 1
            elif ret != expected_ret:
                print_fail("{0}\t-- RET : {1}".format(test_name, ret))
                self.failed += 1
            else:
                print_good(test_name)
                self.passed += 1

def normalize(path):
    if path[len(path) - 1] != '/':
        path += '/'

    return path

if __name__ == '__main__':
    tests_dir = normalize(sys.argv[1])
    tests = suite()

    for test_dir in TEST_DIRS:
        print_bold(
                "\nCategory: {0}\nFlag: {1}\nExpected return code: {2}\n"
                .format(test_dir[0], test_dir[2], test_dir[1]))
        tests.call_on_dir(tests_dir + test_dir[0] + "/",
                          test_dir[1], test_dir[2], test_dir[3], test_dir[4],
                          test_dir[5], test_dir[6])

    print("Tests: " + BOLD + " "
          + str(tests.passed) + " / " + str(tests.passed + tests.failed) + ENDC)

    if tests.failed > 0:
        sys.exit(1)
    else:
        sys.exit(0)
