echo "Removing build and dist directories."
rm build -r
rm dist -r
echo "Removing .spec file."
rm *.spec
echo "Reinstalling Flair app."
pyinstaller -w -F --add-data "templates;templates" --add-data "static;static"  -y flair.py
echo "Flair.exe created. Navigate to ./dist/ and run flair.exe in pycharm/windows terminal or ./flair.exe in bash to launch the application."
