import os
import platform
import subprocess
import sys
from pathlib import Path, PurePosixPath
from subprocess import Popen, PIPE, STDOUT

operating_system = str(platform.system()).lower()

if "window" in operating_system:
    if 'HOME' in os.environ:
        HOME = os.environ['HOME']
    elif 'HOMEPATH' in os.environ:
        HOME = os.environ['HOMEPATH']
    else:
        HOME = "./"
elif "darwin" in operating_system or "linux" in operating_system:
    HOME = os.environ['HOME']
else:
    HOME = os.environ['HOME']


def replace_all_paths(path):
    if path == "":
        return path
    path = path.replace("$HOME", HOME)
    path = path.replace("~", HOME)
    return path


def cmdline(command):
    if "window" in operating_system:
        command = command.split("\n")
        windows_cmdline(command)
    elif "darwin" in operating_system:
        cmd = command
        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        p.wait()
        output = ""
        for line in p.stdout:
            output += line.decode("utf-8")
        print(output)
    else:
        print("Operating system not supported, please use Mac OS or Windows")
        sys.exit(1)


def windows_cmdline(cmds):
    print("CMDS ARE:")
    print(cmds)
    for i in range(len(cmds)):
        cmds[i] = str(PurePosixPath(cmds[i]))
        if 'cp -r' in cmds[i] and 'Flair\\*' in cmds[i]:
            cmds[i] = cmds[i].split(" ")
            cmds[i][2] = repr(cmds[i][2])
            cmds[i][3] = repr(cmds[i][3])[1:-1]
            cmds[i][2] = cmds[i][2][1:len(cmds[i][2]) - 4] + "/*"
            cmds[i] = " ".join(cmds[i])

    cmds = " & ".join(cmds)
    print("CMDS ARE:")
    print(cmds)
    # os.system(cmds)
    subprocess.run(cmds, shell=True)


def create_windows_executable(path, python_name, react_name, app_name):
    cmds = [
        "cd " + os.path.join(react_name),
        "echo 'Building React App...'",
        "npm run build",
        "cd ..",
        "echo 'Cleaning up old builds...'",
        "rm -rf dist",
        "rm -rf templates",
        "rm -rf static",
        "mkdir templates",
        "cp -r " + react_name + "/build/index.html templates/index.html",
        "cp -r " + react_name + "/build/static static/",
        "echo 'Building exe...'",
        'pyinstaller -w -D -y --add-data "templates;templates" --add-data "static;static" flair.py',
        "rm -rf flair.spec",
    ]
    sh_file = "\n".join(cmds)
    with open(os.path.join(path, python_name, "create_executable.sh"), mode='w') as f:
        f.write(sh_file)
    print("Executable script written, installing pip dependencies")
    cmds = [
        "cd " + os.path.join(path, python_name),
        "chmod +x create_executable.sh",
    ]
    cmdline("\n".join(cmds))


def create_darwin_executables(path, python_name, react_name, app_name):
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
    with open(os.path.join(path, python_name, "create_executable.sh"), mode='w') as f:
        f.write(sh_file)
    print("Executable script written, installing pip dependencies")
    cmds = [
        "cd " + os.path.join(path, python_name),
        "pipenv --three",
        "pipenv install Flask",
        "pipenv install pywebview",
        "pipenv install py2app",
        "pipenv install Flask-Sockets",
        "pipenv install Flask-Cors",
        "chmod +x create_executable.sh",
    ]
    cmdline("\n".join(cmds))


def create_project(path, python_name, react_name, app_name):
    path = replace_all_paths(path)
    react_name = react_name.lower()
    cwd = os.getcwd()
    print("Creating Project Flair Skeleton. May take a couple of minutes...")
    cwd = (str(Path(cwd)))
    print("CWD:", cwd)
    cmds = [
        "cd " + path,
        "mkdir " + python_name,
        "cd " + python_name,
        "npx create-react-app " + react_name,
        "cp -r " + cwd + "/* " + path + "/" + python_name,
        "cd " + path + "/" + python_name,
        "rm -rf project-flair.py dist build",
        "rm -rf " + react_name + "/.git",
        "rm -rf " + react_name + "/.gitignore",
        "rm -rf " + react_name + "/src",
        "rm -rf " + react_name + "/public/index.html",
        "mv rt.py " + react_name + "/rt.py",
        "mv index.html " + react_name + "/public/index.html",
        "cp -r src " + react_name + "/src",
        "cd " + react_name,
        "npm install --save react-router-dom",
        # "npm install --save typescript",
        # "npm install --save @types/node",
        # "npm install --save @types/react",
        # "npm install --save @types/react-dom",
        # "npm install --save @types/jest"
    ]

    cmdline("\n".join(cmds))
    print("Creating Executable Script...")
    if "window" in operating_system:
        create_windows_executable(path, python_name, react_name, app_name)
    elif "darwin" in operating_system or "linux" in operating_system:
        create_darwin_executables(path, python_name, react_name, app_name)
    else:
        print("Operating system not supported, please use Mac OS or Windows")
        sys.exit(1)
    print("Script completed, cd to folder and run create_executable.sh to make app")


def main():
    argl = len(sys.argv)
    if argl < 3:
        print("You must provide path and project name ")
    elif argl > 5:
        print("Too many arguments")
    path = sys.argv[1]  # "~/Documents/PythonProjects"
    python_name = sys.argv[2]  # React+Flask
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
