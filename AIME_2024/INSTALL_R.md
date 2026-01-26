# R 和 lme4 安装指南

本指南说明如何在 Linux 系统上安装 R 和 lme4 包，以便使用 `run_r_mixed_for_label_question_and_aug` 函数。

## 1. 安装 R

### Ubuntu/Debian 系统

#### 步骤 1: 添加 CRAN 镜像源

```bash
# 对于 Ubuntu 24.04 (Noble) 或更新版本
sudo apt-get update
sudo apt-get install -y software-properties-common
sudo add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/"

# 添加 GPG 密钥
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9

# 更新包列表
sudo apt-get update
```

#### 步骤 2: 安装 R

```bash
# 安装 R 基础包
sudo apt-get install -y r-base r-base-dev

# 验证安装
R --version
```

### CentOS/RHEL 系统

```bash
# 安装 EPEL 仓库（如果还没有）
sudo yum install -y epel-release

# 安装 R
sudo yum install -y R R-devel
```

### 从源码编译（适用于所有 Linux 发行版）

```bash
# 下载 R 源码
wget https://cran.r-project.org/src/base/R-4/R-4.3.2.tar.gz
tar -xzf R-4.3.2.tar.gz
cd R-4.3.2

# 配置和编译
./configure --prefix=/usr/local
make
sudo make install
```

## 2. 安装 lme4 包

安装 R 后，启动 R 并安装 lme4：

```bash
# 启动 R
R
```

在 R 控制台中执行：

```r
# 安装 lme4（会自动安装依赖包）
install.packages("lme4")

# 验证安装
library(lme4)
```

### 非交互式安装（命令行方式）

如果需要在脚本中自动安装，可以使用：

```bash
Rscript -e "install.packages('lme4', repos='https://cloud.r-project.org')"
```

### 如果遇到编译问题

某些系统可能需要额外的开发库：

```bash
# Ubuntu/Debian
sudo apt-get install -y libnlopt-dev libcurl4-openssl-dev libssl-dev

# CentOS/RHEL
sudo yum install -y nlopt-devel openssl-devel libcurl-devel
```

## 3. （可选）安装 rpy2（Python 接口）

如果希望在 Python 中直接调用 R（而不是通过 R 脚本），可以安装 `rpy2`：

```bash
# 使用 pip 安装
pip install rpy2

# 或者使用 conda
conda install -c conda-forge rpy2
```

**注意**：安装 rpy2 之前，确保 R 已经正确安装并在 PATH 中。

### 验证 rpy2 安装

```python
import rpy2.robjects as ro
print(ro.r('R.version.string'))
```

## 4. 验证完整安装

### 测试 R 和 lme4

```bash
# 创建测试脚本 test_r.R
cat > test_r.R << 'EOF'
library(lme4)
cat("R version:", R.version.string, "\n")
cat("lme4 version:", as.character(packageVersion("lme4")), "\n")
cat("安装成功！\n")
EOF

# 运行测试
Rscript test_r.R
```

### 测试 Python 中的 R 函数

```python
# 测试脚本 test_r_function.py
from AIME_2024.get_mix_effect import run_r_mixed_for_label_question_and_aug

# 假设有测试数据
# run_r_mixed_for_label_question_and_aug("ames_log_2026", "test_label", outdir="test_output")
```

## 5. 常见问题排查

### 问题 1: R 命令未找到

```bash
# 检查 R 是否在 PATH 中
which R

# 如果不在，添加到 PATH（根据实际安装路径调整）
export PATH=/usr/local/bin:$PATH
```

### 问题 2: lme4 安装失败

```r
# 在 R 中尝试从不同镜像安装
options(repos = c(CRAN = "https://cloud.r-project.org"))
install.packages("lme4")

# 或者指定镜像
install.packages("lme4", repos = "https://mirrors.tuna.tsinghua.edu.cn/CRAN/")
```

### 问题 3: 编译错误

确保安装了必要的编译工具和开发库：

```bash
# Ubuntu/Debian
sudo apt-get install -y build-essential gfortran libreadline-dev

# CentOS/RHEL
sudo yum groupinstall -y "Development Tools"
sudo yum install -y gcc-gfortran readline-devel
```

### 问题 4: rpy2 导入失败

```bash
# 检查 R_HOME 环境变量
echo $R_HOME

# 如果未设置，可能需要设置
export R_HOME=$(R RHOME)
```

## 6. 快速安装脚本（Ubuntu/Debian）

```bash
#!/bin/bash
# 一键安装 R 和 lme4（适用于 Ubuntu/Debian）

# 添加 CRAN 源
sudo apt-get update
sudo apt-get install -y software-properties-common
sudo add-apt-repository -y "deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/"
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
sudo apt-get update

# 安装 R
sudo apt-get install -y r-base r-base-dev libnlopt-dev

# 安装 lme4
Rscript -e "install.packages('lme4', repos='https://cloud.r-project.org')"

# 验证
Rscript -e "library(lme4); cat('lme4 安装成功！\n')"
```

保存为 `install_r.sh`，然后运行：

```bash
chmod +x install_r.sh
./install_r.sh
```

## 参考链接

- R 官网: https://www.r-project.org/
- CRAN 镜像: https://cran.r-project.org/mirrors.html
- lme4 文档: https://lme4.github.io/lme4/
- rpy2 文档: https://rpy2.github.io/
