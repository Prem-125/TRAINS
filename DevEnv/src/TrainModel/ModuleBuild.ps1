#entering the virtual environment
..\..\Scripts\Activate.ps1


#installing py
pyinstaller --name="MyApplication" --windowed --onefile src/TrainModelMain.py

#stackoverflow step
cp -recurse -force ..\..\lib\site-packages\PyQt6\Qt\plugins\platforms .\dist