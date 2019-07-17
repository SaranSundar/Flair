import os
import sys
from subprocess import Popen, PIPE, STDOUT

HOME = os.environ['HOME']


def replace_all_paths(path):
    if path == "":
        return path
    path = path.replace("$HOME", HOME)
    path = path.replace("~", HOME)
    return path


def cmdline(command):
    cmd = command
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    p.wait()
    output = ""
    for line in p.stdout:
        output += line.decode("utf-8")
    print(output)


def create_executables(path, python_name, react_name, app_name):
    cmds = [
        "cd " + os.path.join(react_name),
        "echo 'Building React App...'",
        "npm run build",
        "cd ..",
        "echo 'Cleaning up old builds...'",
        "rm -rf *.app",
        "rm -rf " + app_name + "_exec",
        "rm -rf dist",
        "rm -rf templates",
        "rm -rf static",
        "mkdir templates",
        "cp -r " + os.path.join(react_name, "build", "index.html") + " templates/index.html",
        "cp -r " + os.path.join(react_name, "build", "static") + " static",
        "echo 'Starting pip environment...'",
        'pipenv run python setup.py py2app',
        "cp -r dist/*.app ./" + app_name + ".app",
        "rm *.spec",
        "rm -rf build",
        "rm -rf dist"
    ]
    sh_file = "\n".join(cmds)
    with open(os.path.join(path, python_name, "create_executables.sh"), mode='w') as f:
        f.write(sh_file)
    print("Exectuable script written, installing pip dependencies")
    cmds = [
        "cd " + os.path.join(path, python_name),
        "pipenv --three",
        "pipenv install Flask",
        "pipenv install pywebview",
        "pipenv install py2app",
        "chmod +x create_executables.sh",
    ]
    cmdline("\n".join(cmds))


def create_project(path, python_name, react_name, app_name):
    path = replace_all_paths(path)
    react_name = react_name.lower()
    cwd = os.getcwd()
    print("Creating Project Flair Skeleton...")
    cmds = [
        "cd " + path,
        "mkdir " + python_name,
        "cd " + python_name,
        "npx create-react-app " + react_name,
        "cp -r " + cwd + "/* ./",
        "rm -rf project-flair.py dist build static templates",
        "rm -rf " + os.path.join(react_name) + "/.git",
        "rm -rf " + os.path.join(react_name) + "/.gitignore",
        "mv /rt.py " + os.path.join(react_name) + "/rt.py",
    ]

    cmdline("\n".join(cmds))
    print("Creating Executable Script...")
    create_executables(path, python_name, react_name, app_name)
    print("Script completed, cd to folder and run create_executables.sh to make app")


def main():
    argl = len(sys.argv)
    if argl < 3:
        print("You must provide path and project name ")
    elif argl > 5:
        print("Too many arguments")
    path = sys.argv[1]  # "~/Documents/PythonProjects"
    python_name = sys.argv[2]  # ~/Documents/PythonProjects
    if argl > 3:
        react_name = sys.argv[3]
    else:
        react_name = "react-ui"
    if argl > 4:
        app_name = sys.argv[4]
    else:
        app_name = python_name
    create_project(path, python_name, react_name, app_name)


if __name__ == '__main__':
    main()
