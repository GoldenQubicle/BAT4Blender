# BAT4Blender

(tested with Blender 3.6)

## Installing the Add-on
The general gist of it is as follows.
1. download the `source` folder.
2. rename the folder to BAT4Blender and zip it (the files inside the zip should end up inside a BAT4Blender subfolder).
3. open Blender and go to `Edit` -> `Preferences` -> `Add-ons` -> `Install..`
4. navigate to the zip file created in step 2.
5. select `Install Add-on from File..`.
6. the Add-on is now installed and available in the `Properties` context menu in the `Scene` tab.

Notes
- in Blender, print output is sent to system console, not to the Python console. Go to 'Window' -> 'Toggle System Console' to open it.

## Roadmap

- [x] alpha version (camera positioning, LOD creation, rendering of small objects)
- [x] slicing of rendered images if larger than 256 px
- [x] slicing of LODs
- [x] uv-mapping of LODs
- [ ] zoom-dependent LODs
- [ ] renderer settings (lighting/shading/materials/…)
- [ ] nightlights
- [ ] darknite settings
- [x] HD rendering
- [x] conversion of LODs to S3D: Using [fshgen](https://github.com/memo33/fshgen/releases):
  ```
  fshgen import -o output.SC4Model --force --with-BAT-models --format Dxt1 --gid 0xffffffff *.obj *.png
  ```    
- [ ] showing progress while rendering: https://blender.stackexchange.com/a/71830
