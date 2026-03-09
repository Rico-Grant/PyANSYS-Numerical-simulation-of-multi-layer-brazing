# config.py

DEFAULT_PARAMS = {
    # 几何尺寸 (mm)
    "L_half": 6.25,
    "H_cc": 5.0,
    "H_agcuti": 0.3,
    "H_w": 0.4,
    "H_ss": 5.0,

    # 温度 (K)
    "T_zero_stress": 1272.15,
    "T_room": 293.15,

    # 材料编号
    "mat_cc": 1,
    "mat_agcuti": 2,
    "mat_w": 3,
    "mat_ss": 4,

    # 单元参数
    "elem_type": 1,
    "real_const": 0,

    # 网格参数
    "nx": 50,
    "ny_cc_bulk": 8,
    "ny_cc_near": 16,
    "ny_ag1": 16,
    "ny_w": 20,
    "ny_ag2": 16,
    "ny_ss_near": 16,
    "ny_ss_bulk": 8,
}