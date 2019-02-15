# BAT4Blender

## Running external python scripts in Blender
1. download (or copy contents of) link_script.txt 
2. open Blender and switch to scripting layout
3. open the link_script.txt file in the text editor (or paste the contents in a new file)
4. change the strings in the filename to point towards a python script (the experimental.py file is a minimal example)
`filename = os.path.join("DRIVE:/folder/path", "scriptfile.py")`
5. while in the Blender text editor hit the key combo alt+p to run the script
6. use an IDE / text editor of choice to edit pythons files, save, and re-run the link script in Blender
7. That's it :) 

Notes
- in Blender print output is send to system console, not to the python console. Go to 'Window' -> 'Toggle System Console' to open it.  

## Installing the add-on
The current project structure is not well suited yet to accomodate this.
However the general gist of it is as follows.
1. download `__init__.py` and `BAT4Blender.py`
2. put the two in a folder, and zip said folder.
3. open Blender and go to 'Edit' -> 'Preferences' -> 'Install..' 
4. navigate to the zip file created in step 2 
5. select 'Install Add-on from File..' 
6. the Add-on is now installed and available in the output context menu. 
7. disable / enable the Add-on to delete sun and camera objects

Notes
- the render path is currently not set and consequently rendering the camera views will fail. 
- disabling / enabling the Add-on only reloads code from `__init__.py` 
  - i.e. changes made to `BAT4Blender.py` will only take effect after a full restart of Blender. 








