#!/bin/bash
# 磁盘空间清理脚本

echo "=========================================="
echo "磁盘空间清理工具"
echo "=========================================="
echo ""

# 显示当前磁盘使用情况
echo "当前磁盘使用情况："
df -h / | tail -1
echo ""

# 1. 清理 apt 缓存
echo "[1] 清理 apt 缓存..."
sudo apt-get clean
sudo apt-get autoclean
echo "✓ 完成"
echo ""

# 2. 清理系统日志（保留最近3天）
echo "[2] 清理旧系统日志（保留最近3天）..."
sudo journalctl --vacuum-time=3d > /dev/null 2>&1
echo "✓ 完成"
echo ""

# 3. 清理 pip 缓存
echo "[3] 清理 pip 缓存..."
pip cache purge > /dev/null 2>&1 || true
echo "✓ 完成"
echo ""

# 4. 清理 conda 缓存
echo "[4] 清理 conda 缓存..."
conda clean --all -y > /dev/null 2>&1 || true
echo "✓ 完成"
echo ""

# 5. 清理临时文件
echo "[5] 清理临时文件..."
sudo find /tmp -type f -atime +7 -delete 2>/dev/null || true
sudo find /var/tmp -type f -atime +7 -delete 2>/dev/null || true
echo "✓ 完成"
echo ""

# 6. 清理旧的内核（可选，需要确认）
echo "[6] 检查旧内核..."
OLD_KERNELS=$(dpkg -l | grep -E 'linux-image-[0-9]' | grep -v $(uname -r) | awk '{print $2}')
if [ ! -z "$OLD_KERNELS" ]; then
    echo "发现旧内核包（不会自动删除，需要手动确认）："
    echo "$OLD_KERNELS"
    echo "如需删除，运行: sudo apt-get purge $OLD_KERNELS"
else
    echo "没有发现旧内核"
fi
echo ""

# 显示清理后的磁盘使用情况
echo "清理后磁盘使用情况："
df -h / | tail -1
echo ""

echo "=========================================="
echo "清理完成！"
echo "=========================================="
