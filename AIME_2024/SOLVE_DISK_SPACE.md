# 解决磁盘空间不足问题

## 问题
安装 R 时遇到错误：
```
E: You don't have enough free space in /var/cache/apt/archives/.
```

## 快速解决方案

### 方案 1: 运行清理脚本（推荐）

```bash
cd /root/all-bench/AIME_2024
./cleanup_disk_space.sh
```

### 方案 2: 手动清理

```bash
# 1. 清理 apt 缓存
sudo apt-get clean
sudo apt-get autoclean

# 2. 清理系统日志（保留最近3天）
sudo journalctl --vacuum-time=3d

# 3. 清理 pip 缓存
pip cache purge

# 4. 清理 conda 缓存
conda clean --all -y

# 5. 清理未使用的包
sudo apt-get autoremove -y
```

### 方案 3: 删除大文件（需要谨慎）

检查大目录：
```bash
# 查看各目录大小
du -h --max-depth=1 /root | sort -h

# 常见可清理的大目录：
# - /root/.vscode-server (3.1G) - VS Code 服务器缓存
# - /root/.lingma (4.2G) - 某个应用的缓存
# - /root/1990-2023高考试题 (7.7G) - 如果不需要可以删除
```

**注意**：删除前请确认这些文件不再需要！

## 安装 R（使用最小安装）

清理空间后，使用修改后的安装脚本（已优化为最小安装）：

```bash
cd /root/all-bench/AIME_2024
./install_r_ubuntu.sh
```

或者手动安装（最小安装）：

```bash
# 添加 CRAN 源
sudo apt-get update
sudo add-apt-repository -y "deb https://cloud.r-project.org/bin/linux/ubuntu jammy-cran40/"
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
sudo apt-get update

# 最小安装 R
sudo apt-get install --no-install-recommends -y r-base r-base-core

# 安装编译依赖（最小）
sudo apt-get install --no-install-recommends -y \
    libnlopt-dev libcurl4-openssl-dev libssl-dev \
    gcc g++ gfortran libreadline-dev make

# 安装 lme4
Rscript -e "install.packages('lme4', repos='https://cloud.r-project.org')"
```

## 检查磁盘空间

```bash
# 查看磁盘使用情况
df -h /

# 查看各目录大小
du -h --max-depth=1 /root | sort -h
```

## 预防措施

定期清理可以避免空间不足：

1. **设置自动清理**（添加到 crontab）：
```bash
# 每月清理一次
0 0 1 * * /root/all-bench/AIME_2024/cleanup_disk_space.sh
```

2. **监控磁盘使用**：
```bash
# 添加到 ~/.bashrc
alias disk='df -h / && echo "---" && du -h --max-depth=1 /root 2>/dev/null | sort -h | tail -5'
```

## 如果仍然空间不足

如果清理后仍然空间不足，考虑：

1. **扩展磁盘**（如果有虚拟化环境）
2. **移动大文件到其他位置**（如外部存储）
3. **删除不需要的项目或数据**

## 相关文件

- `cleanup_disk_space.sh` - 自动清理脚本
- `install_r_ubuntu.sh` - R 安装脚本（已优化为最小安装）
