# 负责启动 MAPDL
# 默认：调用16线程
from ansys.mapdl.core import launch_mapdl

def start_mapdl(nproc=16):
    mapdl = launch_mapdl(nproc=nproc)
    print(mapdl)
    return mapdl