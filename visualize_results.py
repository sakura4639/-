#!/usr/bin/env python3
import os
import sys

def ensure_dependencies():
    """确保所有依赖已安装"""
    try:
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns
        import numpy as np
        return True
    except ImportError as e:
        print(f"缺少依赖: {e}")
        print("请运行: make setup")
        return False

def generate_sample_data():
    """生成示例数据"""
    print("生成示例性能数据...")
    
    # 创建结果目录
    os.makedirs("results", exist_ok=True)
    
    # 简单的示例数据
    sample_data = """optimization,algorithm,size,time,correct
-O0,QuickSort_Recursive,1000,0.001234,Yes
-O0,QuickSort_Iterative,1000,0.001567,Yes
-O0,MergeSort_Parallel,1000,0.000891,Yes
-O0,MergeSort_Sequential,1000,0.001123,Yes
-O1,QuickSort_Recursive,1000,0.000945,Yes
-O1,QuickSort_Iterative,1000,0.001034,Yes
-O1,MergeSort_Parallel,1000,0.000678,Yes
-O1,MergeSort_Sequential,1000,0.000892,Yes
-O2,QuickSort_Recursive,5000,0.005432,Yes
-O2,QuickSort_Iterative,5000,0.005789,Yes
-O2,MergeSort_Parallel,5000,0.003456,Yes
-O2,MergeSort_Sequential,5000,0.004321,Yes"""
    
    with open("results/performance_results.csv", "w") as f:
        f.write(sample_data)
    
    print("示例数据生成完成!")

def create_simple_visualization():
    """创建简单的可视化"""
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # 设置样式
    plt.style.use('default')
    sns.set_palette("husl")
    
    # 读取数据
    df = pd.read_csv("results/performance_results.csv")
    
    # 创建图表
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # 图表1: 不同优化级别的性能对比
    pivot_data = df.pivot_table(values='time', index='optimization', columns='algorithm', aggfunc='mean')
    pivot_data.plot(kind='bar', ax=axes[0,0])
    axes[0,0].set_title('不同优化级别下的算法性能')
    axes[0,0].set_ylabel('执行时间 (秒)')
    axes[0,0].tick_params(axis='x', rotation=45)
    
    # 图表2: 数据规模对性能的影响
    for algo in df['algorithm'].unique():
        algo_data = df[df['algorithm'] == algo]
        axes[0,1].plot(algo_data['size'], algo_data['time'], 'o-', label=algo, markersize=6)
    axes[0,1].set_title('数据规模对性能的影响')
    axes[0,1].set_xlabel('数据规模')
    axes[0,1].set_ylabel('执行时间 (秒)')
    axes[0,1].legend()
    axes[0,1].grid(True, alpha=0.3)
    
    # 图表3: 热力图
    heatmap_data = df.pivot_table(values='time', index='optimization', columns='algorithm', aggfunc='mean')
    sns.heatmap(heatmap_data, annot=True, fmt='.4f', cmap='YlOrRd', ax=axes[1,0])
    axes[1,0].set_title('性能热力图')
    
    # 图表4: 算法对比
    algorithm_means = df.groupby('algorithm')['time'].mean().sort_values()
    algorithm_means.plot(kind='bar', ax=axes[1,1], color='lightblue')
    axes[1,1].set_title('算法平均性能排名')
    axes[1,1].set_ylabel('平均执行时间 (秒)')
    axes[1,1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('results/performance_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("可视化完成! 图表已保存至: results/performance_analysis.png")

def main():
    print("=== 排序算法性能可视化 ===")
    
    # 检查依赖
    if not ensure_dependencies():
        sys.exit(1)
    
    # 如果数据文件不存在，生成示例数据
    if not os.path.exists("results/performance_results.csv"):
        print("数据文件不存在，生成示例数据...")
        generate_sample_data()
    else:
        print("找到现有数据文件")
    
    # 创建可视化
    create_simple_visualization()
    
    # 显示数据统计
    import pandas as pd
    df = pd.read_csv("results/performance_results.csv")
    print(f"\n数据统计:")
    print(f"总记录数: {len(df)}")
    print(f"测试的优化级别: {df['optimization'].unique().tolist()}")
    print(f"测试的算法: {df['algorithm'].unique().tolist()}")
    print(f"测试的数据规模: {df['size'].unique().tolist()}")

if __name__ == "__main__":
    main()
