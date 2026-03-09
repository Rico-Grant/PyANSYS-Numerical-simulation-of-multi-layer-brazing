# boundary_conditions.py

def apply_boundary_conditions(mapdl):
    mapdl.antype("STATIC")
    mapdl.nlgeom("OFF")

    mapdl.nsel("S", "LOC", "X", 0.0)
    mapdl.d("ALL", "UX", 0)

    mapdl.nsel("S", "LOC", "Y", 0.0)
    mapdl.d("ALL", "UY", 0)

    mapdl.nsel("S", "LOC", "X", 0.0)
    mapdl.nsel("R", "LOC", "Y", 0.0)
    mapdl.d("ALL", "UX", 0)
    mapdl.d("ALL", "UY", 0)

    mapdl.allsel()