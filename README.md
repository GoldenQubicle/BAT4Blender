# BAT4Blender

## Running external python scripts in Blender
1. download (or copy contents of) link_script.txt 
2. open Blender and switch to scripting layout
3. open the link_script.txt file in the text editor (or paste the contents in a new file)
4. change the strings in the filename to point towards a python script (the experimental.py file is a minimal example)
`filename = os.path.join("DRIVE:/folder/path", "scriptfile.py")`
5. while in the Blender text editor hit the key combo alt+p to run the script
6. use an IDE / text editor of choice to edit pythons scripts, save, and re-run the script in Blender
7. That's it :) 

Note: in Blender print output is send to system console, not the python console.
To open the system console in Blender go to 'Window' -> 'Toggle System Console' 









