Remove-Item -Path .\out\* -Recurse
New-Item -Path 'out\BAT4Blender' -ItemType Directory
Copy-Item .\source\* .\out\BAT4Blender\
Compress-Archive -Path .\out\BAT4Blender\ -DestinationPath .\out\BAT4Blender.zip