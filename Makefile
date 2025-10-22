# 修正的 Makefile - 自动使用虚拟环境

# 虚拟环境路径
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

.PHONY: all compile test visualize clean setup help

all: compile test visualize

setup:
	@echo "设置虚拟环境..."
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install pandas matplotlib seaborn numpy
	@echo "虚拟环境设置完成!"

compile:
	@echo "编译C程序..."
	gcc -O2 -fopenmp sorting_analysis.c -o sorting_analysis -lm

test: compile
	@echo "运行性能测试..."
	./sorting_analysis

visualize: check-env
	@echo "生成可视化..."
	@$(PYTHON) visualize_results.py

clean:
	rm -f sorting_analysis
	rm -rf results
	rm -f test_data_*.txt
	rm -f *.png

clean-all: clean
	rm -rf $(VENV)

help:
	@echo "可用命令:"
	@echo "  make setup     - 设置虚拟环境和依赖"
	@echo "  make compile   - 编译C程序"
	@echo "  make test      - 运行性能测试"
	@echo "  make visualize - 生成可视化图表"
	@echo "  make all       - 执行完整流程"
	@echo "  make clean     - 清理生成的文件"
	@echo "  make clean-all - 清理所有文件包括虚拟环境"

# 检查虚拟环境是否存在
check-env:
	@if [ ! -d "$(VENV)" ]; then \
		echo "错误: 虚拟环境不存在，请先运行 'make setup'"; \
		exit 1; \
	fi
