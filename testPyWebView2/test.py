import webview


def write_to_file(message):
    with open("tester.txt", mode="a+") as f:
        f.writelines(message + "\n")


write_to_file("Start load window")
webview.create_window('Hello World', 'https://pywebview.flowrl.com/')
webview.start()
write_to_file("Window exited")

