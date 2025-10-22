#!/bin/bash

echo "=== 排序算法编译和性能测试 ==="

# 创建编译目录
mkdir -p bin
mkdir -p results

# 优化级别数组
OPT_LEVELS=("-O0" "-O1" "-O2" "-O3" "-Ofast")

# 清空之前的CSV结果
echo "optimization,algorithm,size,time,correct" > results/performance_results.csv

# 为每个优化级别编译和测试
for opt in "${OPT_LEVELS[@]}"; do
    echo ""
    echo "使用优化级别 $opt 编译..."
    
    # 编译程序
    gcc $opt -fopenmp sorting_analysis.c -o bin/sort_test_${opt} -lm
    
    if [ $? -eq 0 ]; then
        echo "编译成功！运行性能测试..."
        echo "=== 优化级别: $opt ===" >> results/test_log.txt
        ./bin/sort_test_${opt} >> results/test_log.txt 2>&1
        echo "测试完成！"
    else
        echo "编译失败: $opt"
    fi
done

echo ""
echo "=== 所有测试完成 ==="
echo "详细日志: results/test_log.txt"
echo "性能数据: results/performance_results.csv"
