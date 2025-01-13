# spinali_kicad_libs
For use in kicad8 or greater.

## Steps to use

**Preferences** -> **Configure paths** -> **Environment Variables** -> Add the following entry
|Name            |Path    |
|----------------|--------|
|KICAD_SPINALI |**YourPathTo**/spinali_kicad_libs |

**Preferences** -> **Manage Symbol Libraries** -> **Global Libraries** -> Add the following entry

|Active            |Visible           |Nickname       |Library Path                      | Library Format |
|------------------|------------------|---------------|----------------------------------|----------------|
|:heavy_check_mark:|:heavy_check_mark:|Spinali        |${KICAD_SPINALI}/spinali.kicad_sym| KiCad          |


**Preferences** -> **Manage Footprint Libraries** -> **Global Libraries** -> Add the following entry

|Active            |Nickname       |Library Path                      | Library Format |
|------------------|---------------|----------------------------------|----------------|
|:heavy_check_mark:|Spinali        |${KICAD_SPINALI}/Footprints.pretty| KiCad          |

## Add a new component
1. Add the associated symbol by copying and appending the relevant portions from the `to_be_added.kicad_sym` into `spinali.kicad_sym`
2. Add the `to_be_added.kicad_mod` footprint file to the Footprints.pretty folder.
3. Add any 3D models into root folder.
