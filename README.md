# BAT4Blender

## Running external scripts in Blender
1. download (or copy contents of) link_script.txt 
2. open Blender and switch to scripting layout
3. open the link_script.txt file (or paste the contents)
4. change the strings in the filename to point towards a python script (the experimental.py file is a minimal example)
`filename = os.path.join("DRIVE:/folder/path", "scriptfile.py")`
5. in Blender hit the key combo alt+p to run the script
6. that's it! :) 

Note in Blender print output is send to system console, not the python console.
To open this in Blender go to 'Window' -> 'Toggle System Console' 









