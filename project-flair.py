import os
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
        "cd " + os.path.join(path, python_name, react_name),
        "npm run build",
        "cd ..",
        "rm -rf *.app",
        "rm -rf " + app_name + "_exec",
        "rm -rf dist",
        "rm -rf templates",
        "rm -rf static",
        "rm *.spec",
        "mkdir templates",
        "cp -r " + os.path.join(path, python_name, react_name, "build", "index.html") + " templates/index.html",
        "cp -r " + os.path.join(path, python_name, react_name, "build", "static") + " static",
        'pyinstaller -w -F --add-data "templates:templates" --add-data "static:static" flair.py',
        "cp -r dist/flair.app ./" + app_name + ".app",
        "cp -r dist/flair.app/Contents/MacOS/flair" + " ./" + app_name + "_exec",
        "rm *.spec",
        "rm -rf build",
        "rm -rf dist"
    ]
    sh_file = "\n".join(cmds)
    with open(os.path.join(path, python_name, "create_executables.sh"), mode='w') as f:
        f.write(sh_file)
    cmdline(sh_file)
    cmds = [
        "cd " + os.path.join(path, python_name),
        "chmod +x create_executables.sh"
    ]
    cmdline("\n".join(cmds))


def create_project(path, python_name, react_name, app_name):
    path = replace_all_paths(path)
    react_name = react_name.lower()
    cwd = os.getcwd()
    cmds = [
        "cd " + path,
        "mkdir " + python_name,
        "cd " + python_name,
        "npx create-react-app " + react_name,
        "cd " + react_name,
        "npm run build",
        "cd ..",
        "cp -r " + react_name + "/build/static static",
        "mkdir templates",
        "cp -r " + react_name + "/build/index.html templates/index.html",
        "cp " + cwd + "/*.py " + os.path.join(path, python_name) + "/",
        ""
    ]

    cmdline("\n".join(cmds))
    create_executables(path, python_name, react_name, app_name)


def main():
    path = "~/Documents/PythonProjects"
    python_name = "React+Flask"
    react_name = "react-ui"
    app_name = "React+Flask"
    create_project(path, python_name, react_name, app_name)


if __name__ == '__main__':
    main()
