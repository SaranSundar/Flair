import os
import sys
from string import Template


def create_react_component_class(component_name):
    template = [
        "import React, {Component} from 'react';",
        "import './$component_name.css';",
        "",
        "class $component_name extends Component {",
        "    constructor(props) {",
        "        super(props);",
        "    }",
        "",
        "    render() {",
        "        return (",
        '            <div className="$component_name">',
        "            </div>",
        "        );",
        "    }",
        "}",
        "",
        "export default $component_name;"
    ]
    css_class = """.$component_name {\n}"""
    template = "\n".join(template)
    template = Template(template).substitute(component_name=component_name)
    css_class = Template(css_class).substitute(component_name=component_name)
    return template, css_class


def create_react_component_function(component_name):
    template = [
        "import React from 'react';",
        "import './$component_name.css';",
        "",
        "function $component_name() {",
        "    return (",
        '        <div className="$component_name">',
        "        </div>",
        "    );",
        "}",
        "",
        "export default $component_name;"
    ]
    css_class = """.$component_name {\n}"""
    template = "\n".join(template)
    template = Template(template).substitute(component_name=component_name)
    css_class = Template(css_class).substitute(component_name=component_name)
    return template, css_class


def create_react_component(component_name, component_type):
    if component_type == "class":
        template, css = create_react_component_class(component_name)
    elif component_type == "function":
        template, css = create_react_component_function(component_name)
    if not os.path.exists("src/components/"):
        os.system("mkdir src/components")
    if not os.path.exists("src/components/" + component_name):
        os.system("mkdir src/components/" + component_name)
    if os.path.exists("src/components/" + component_name + "/" + component_name + ".js"):
        print(component_name + ".js already exists, will not overwrite, aborting operation")
    else:
        with open("src/components/" + component_name + "/" + component_name + ".js", mode='w') as f:
            f.write(template)
    if os.path.exists("src/components/" + component_name + "/" + component_name + ".css"):
        print(component_name + ".css already exists, will not overwrite, aborting operation")
    else:
        with open("src/components/" + component_name + "/" + component_name + ".css", mode='w') as f:
            f.write(css)


def main():
    args = sys.argv
    if len(args) < 2:
        print("Too few arguments")
    elif len(args) > 3:
        print("Too many arguments")
    if not (args[1] == "c" or args[1] == "component" or args[1] == "f" or args[1] == "function"):
        print("Command " + args[1] + " not supported")
    elif args[1] == "c" or args[1] == "component":
        component_type = "class"
    elif args[1] == "f" or args[1] == "function":
        component_type = "function"

    component_name = args[2]
    create_react_component(component_name, component_type)


if __name__ == '__main__':
    main()
