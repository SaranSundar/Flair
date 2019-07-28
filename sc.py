import json
import pathlib
import sys

import requests


def main():
    if len(sys.argv) < 4 or len(sys.argv) > 6:
        print(
            "Wrong amount of arguments. Should pass in <UserName> <RepoName> <path-to-component>"
            " <download-path> <token-if-repo-is-private>")
        print("Ex. python sc.py SaranSundar TestGUI src/components/NoMatch token-here")
        return

    url = f"https://api.github.com/repos/{sys.argv[1]}/{sys.argv[2]}/contents/{sys.argv[3]}"
    token = f"token {sys.argv[5]}" if len(sys.argv) == 6 else ""
    headers = {
        'Authorization': token,
        'Accept': "application/vnd.github.v3.raw",
        'Cache-Control': "no-cache",
        'Host': "api.github.com",
        'accept-encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers)
    base_path = sys.argv[4] if len(sys.argv) >= 5 else "./"
    if base_path[0] == "/":
        base_path = base_path[1:]
    if base_path[-1] != "/":
        base_path += "/"
    try:
        files = json.loads(response.text)
        for file in files:
            if file['type'] == 'file':
                fr = requests.get(file['download_url'])
                pathlib.Path(base_path).mkdir(parents=True, exist_ok=True)
                with open(base_path + file['name'], 'w') as f:
                    f.writelines(fr.text)
    except Exception as e:
        file = response.text
        if file == '{"message":"Not Found","documentation_url":"https://developer.github.com/v3/repos' \
                   '/contents/#get-contents"}':
            print("Incorrect path, File does not exist")
            return
        file_name = url.split("/")[-1]
        pathlib.Path(base_path).mkdir(parents=True, exist_ok=True)
        with open(base_path + file_name, mode='w') as f:
            f.writelines(file)


if __name__ == '__main__':
    main()
