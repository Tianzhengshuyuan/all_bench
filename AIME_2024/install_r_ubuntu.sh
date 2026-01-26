#!/bin/bash
# Ubuntu 22.04 快速安装 R 和 lme4 脚本（最小安装版本）

# 设置非交互式模式，避免所有交互式提示
export DEBIAN_FRONTEND=noninteractive
export NEEDRESTART_MODE=a  # 自动处理服务重启提示

echo "=========================================="
echo "开始安装 R 和 lme4（最小安装）"
echo "=========================================="

# 检查磁盘空间
echo ""
echo "检查磁盘空间..."
AVAILABLE=$(df / | tail -1 | awk '{print $4}')
if [ "$AVAILABLE" -lt 1048576 ]; then  # 小于 1GB
    echo "⚠️  警告：可用空间不足 1GB，建议先清理空间"
    echo "运行清理脚本: ./cleanup_disk_space.sh"
    read -p "是否继续安装？(y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 步骤 0: 清理 apt 缓存以释放空间
echo ""
echo "[0/5] 清理 apt 缓存..."
sudo apt-get clean
sudo apt-get autoclean

# 步骤 1: 添加 CRAN 镜像源
echo ""
echo "[1/5] 添加 CRAN 镜像源..."
sudo apt-get update
sudo apt-get install --no-install-recommends -y -o Dpkg::Options::="--force-confold" software-properties-common gnupg2

# 添加 CRAN 仓库（Ubuntu 22.04 Jammy）
sudo add-apt-repository -y "deb https://cloud.r-project.org/bin/linux/ubuntu jammy-cran40/"

# 添加 GPG 密钥
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9

sudo apt-get update

# 步骤 2: 安装 R（最小安装）
echo ""
echo "[2/5] 安装 R（最小安装）..."
sudo apt-get install --no-install-recommends -y -o Dpkg::Options::="--force-confold" r-base r-base-core

# 安装编译依赖（lme4 可能需要，最小安装）
echo ""
echo "[3/5] 安装编译依赖（最小安装）..."
sudo apt-get install --no-install-recommends -y -o Dpkg::Options::="--force-confold" \
    libnlopt-dev libcurl4-openssl-dev libssl-dev \
    gcc g++ gfortran libreadline-dev make

# 步骤 3: 安装 lme4
echo ""
echo "[4/5] 安装 lme4 包..."
Rscript -e "install.packages('lme4', repos='https://cloud.r-project.org', quiet=TRUE)"

# 步骤 4: 验证安装
echo ""
echo "[5/5] 验证安装..."
echo "=========================================="
echo "验证安装..."
echo "=========================================="
R --version
echo ""
Rscript -e "library(lme4); cat('✓ lme4 版本:', as.character(packageVersion('lme4')), '\n')"

echo ""
echo "=========================================="
echo "安装完成！"
echo "=========================================="
echo ""
echo "现在可以使用 run_r_mixed_for_label_question_and_aug 函数了。"
echo ""
echo "（可选）如果要使用 rpy2 在 Python 中直接调用 R："
echo "  pip install rpy2"
echo ""
