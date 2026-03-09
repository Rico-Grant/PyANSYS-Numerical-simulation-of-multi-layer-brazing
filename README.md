# PyANSYS-Numerical-simulation-of-multi-layer-brazing

## 项目功能

本项目实现了以下功能：

- 启动并连接 MAPDL
- 参数化定义模型几何
- 材料属性设置
- 网格划分
- 边界条件与载荷施加
- 求解分析
- 提取中线应力等结果
- 计算关键评价指标
- 单工况运行
- 多工况参数扫描
- 导出 CSV 结果
- 在 Jupyter Notebook 中进行交互式调用与可视化

---

## 项目结构

```text
project/
├─ config.py                  # 全局参数配置
├─ mapdl_utils.py             # MAPDL 启动与通用工具
├─ materials.py               # 材料定义
├─ geometry.py                # 几何建模
├─ meshing.py                 # 网格划分
├─ boundary_conditions.py     # 边界条件与载荷
├─ solver.py                  # 求解
├─ postprocess.py             # 后处理与结果提取
├─ metrics.py                 # 指标计算
├─ run_single_case.py         # 单工况运行入口
├─ main_scan.py               # 参数扫描主程序
├─ run_all.ipynb              # Jupyter Notebook 运行示例
└─ README.md                  # 项目说明文档
```

---

## 运行环境

### 1. Python

建议使用：

- Python 3.10 / 3.11

### 2. 必要依赖

请先安装以下 Python 包：

```bash
pip install ansys-mapdl-core pandas matplotlib numpy jupyter
```

如在 VSCode 中使用 Notebook，请确认已安装：

- Python 扩展
- Jupyter 扩展

### 3. ANSYS 要求

本项目依赖本地可用的 **ANSYS MAPDL**。请确保：

- 本机已安装 ANSYS
- MAPDL 可被 PyMAPDL 正常调用
- License 可正常使用

---

## 如何运行

---

## 方式一：在 Jupyter Notebook 中运行（推荐）

如果你使用 VSCode，并且内置了 Jupyter Notebook，推荐采用这种方式。

### 第一步：进入项目目录

确保 `run_all.ipynb` 与所有 `.py` 文件位于同一项目目录下。

### 第二步：在 Notebook 中导入模块

```python
%load_ext autoreload
%autoreload 2
%matplotlib inline

import os
import pandas as pd
import matplotlib.pyplot as plt

from mapdl_utils import start_mapdl
from run_single_case import run_single_case
```

### 第三步：启动 MAPDL

```python
mapdl = start_mapdl(nproc=16)
```

### 第四步：运行单个工况

```python
result = run_single_case(
    mapdl,
    user_params={"H_w": 0.4},
    outdir="results/test_case"
)
```

### 第五步：查看结果

```python
print(result["metrics"])
df_mid = result["df_mid"]
df_mid.head()
```

### 第六步：批量参数扫描

```python
hw_list = [0.2, 0.4, 0.6, 0.8, 1.0]
summary = []

for hw in hw_list:
    print(f"正在计算 H_w = {hw:.3f} mm")
    result = run_single_case(
        mapdl,
        user_params={"H_w": hw},
        outdir=f"results/tw_{hw:.3f}"
    )
    summary.append(result["metrics"])

df_summary = pd.DataFrame(summary)
df_summary
```

### 第七步：保存结果

```python
df_summary.to_csv("results/summary.csv", index=False, encoding="utf-8-sig")
```

### 第八步：关闭 MAPDL

```python
mapdl.exit()
```

---

## 方式二：直接运行参数扫描脚本

如果你已经在 `main_scan.py` 中写好了主入口函数，则可以直接在终端运行：

```bash
python main_scan.py
```

如果 `main_scan.py` 采用如下结构：

```python
if __name__ == "__main__":
    main()
```

则运行后会自动完成参数扫描并输出汇总结果。

---

## 输出结果

程序运行后，通常会在 `results/` 目录下生成以下内容：

```text
results/
├─ test_case/
│  ├─ midline_stress.csv
│  └─ ...
├─ tw_0.200/
├─ tw_0.400/
├─ tw_0.600/
├─ tw_0.800/
├─ tw_1.000/
└─ summary.csv
```

其中：

- `midline_stress.csv`：某个工况的中线应力结果
- `summary.csv`：所有扫描工况的汇总指标

---

## 建议的开发流程

推荐按照以下顺序使用本项目：

1. 先在 Notebook 中测试单工况
2. 检查模型是否成功建立、求解与后处理
3. 确认结果输出格式正确
4. 再进行批量参数扫描
5. 最后将汇总数据导出并绘图分析

---

## 常见问题

### 1. Notebook 中修改了 `.py` 文件，但运行结果没有更新

请在 Notebook 开头启用自动重载：

```python
%load_ext autoreload
%autoreload 2
```

---

### 2. 找不到模块

请确认：

- Notebook 与 `.py` 文件位于同一目录
- 当前工作目录正确

可以在 Notebook 中检查：

```python
import os
os.getcwd()
```

必要时切换目录：

```python
os.chdir(r"D:\your_project_path")
```

---

### 3. MAPDL 无法启动

请检查：

- ANSYS 是否正确安装
- License 是否可用
- PyMAPDL 是否安装成功
- `start_mapdl()` 中的路径和参数是否正确

---

### 4. 重复运行后出现多个 MAPDL 进程

请在每次运行结束后关闭实例：

```python
mapdl.exit()
```

---

## 可扩展方向

本项目后续可以继续扩展为：

- 多参数联合扫描
- 自动绘制结果曲线
- 自动导出图片与报告
- 不同材料或几何配置对比
- 优化设计与参数敏感性分析
- 封装为更完整的工程计算框架

---
