import matplotlib.pyplot as plt
import numpy as np

# 数据
llm_names = ['deepseek', 'kimi', 'doubao', 'qwen', 'qwen25']
means = np.array([0.2276, 0.0817, 0.2545, 0.1843, 0.2089])
conf95 = np.array([[0.1852, 0.2699], [0.0711, 0.0923], [0.2271, 0.2818], [0.1648, 0.2039], [0.1844, 0.2335]])
conf99 = np.array([[0.1717, 0.2834], [0.0678, 0.0957], [0.2185, 0.2904], [0.1586, 0.2100], [0.1586, 0.2100]])
# 红叉位置: 只有qwen有20%，其余为0
default_values = np.array([0, 0, 0, 0.2, 0])

x = np.arange(len(llm_names))

# 计算误差
yerr_95 = np.abs(conf95.T - means)
yerr_99 = np.abs(conf99.T - means)

plt.figure(figsize=(8,6))

# 99%置信区间（橙色）
plt.errorbar(x, means, yerr=yerr_99, fmt='*', color='orange',
             label='99% Confidence Intervals', capsize=6, elinewidth=2, markersize=10)

# 95%置信区间（蓝色）
plt.errorbar(x, means, yerr=yerr_95, fmt='o', color='blue',
             label='95% Confidence Intervals', capsize=6, elinewidth=2, markersize=8)

# 均值点（黄色星星覆盖）
plt.scatter(x, means, color='gold', marker='*', s=120, zorder=5, label='Mean')

# 红叉（default）
plt.scatter(x, default_values, color='red', marker='x', s=100, label='default')

plt.xticks(x, llm_names, fontsize=12)
plt.ylabel('Accuracy', fontsize=14, weight='bold')
plt.xlabel('LLM', fontsize=14, weight='bold')
plt.title('Accuracy and Confidence Intervals for LLMs on AIME', fontsize=15, weight='bold')
plt.ylim(0, 0.35)
plt.legend(fontsize=11)
plt.tight_layout()
plt.savefig('llm_accuracy.png', dpi=300) 
plt.show()