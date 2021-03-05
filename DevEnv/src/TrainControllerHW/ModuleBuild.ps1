#entering the virtual environment
..\..\Scripts\Activate.ps1


#installing py
pyinstaller --name="TrainControllerHW-GUI" --windowed --onefile src/TrainControllerHW-GUI.py

#stackoverflow step
cp -recurse -force ..\..\lib\site-packages\PyQt6\Qt\plugins\platforms .\dist
