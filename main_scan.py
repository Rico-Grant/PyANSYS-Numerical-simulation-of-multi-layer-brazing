# main_scan.py

import os
import pandas as pd

from mapdl_utils import start_mapdl
from run_single_case import run_single_case


def main():
    mapdl = start_mapdl(nproc=16)

    hw_list = [0.2, 0.4, 0.6, 0.8, 1.0]
    summary = []

    os.makedirs("results", exist_ok=True)

    for hw in hw_list:
        print(f"\n========== 当前计算: H_w = {hw:.3f} mm ==========")

        case_dir = os.path.join("results", f"tw_{hw:.3f}")
        result = run_single_case(
            mapdl,
            user_params={"H_w": hw},
            outdir=case_dir
        )

        summary.append(result["metrics"])

    df_summary = pd.DataFrame(summary)
    df_summary.to_csv("results/summary.csv", index=False, encoding="utf-8-sig")

    print("\n===== 扫描汇总结果 =====")
    print(df_summary)

    mapdl.exit()


if __name__ == "__main__":
    main()