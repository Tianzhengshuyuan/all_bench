import re
import argparse
import numpy as np
from scipy import stats

# 编译两种正则
pattern1 = re.compile(
    r"总题组数:\s*\d+.*?第一轮正确答案数:\s*\d+.*?正确率:\s*[\d.]+%.*?第二轮正确答案数:\s*\d+.*?正确率:\s*([\d.]+)%"
)
pattern2 = re.compile(
    r"总题数:\s*\d+.*?正确数:\s*\d+.*?正确率:\s*([\d.]+)%,\s*耗时:"
)

def get_accuracies(logfile, max_samples=100):
    accuracies = []
    with open(logfile, 'r', encoding='utf-8') as f:
        for line in f:
            m1 = pattern1.search(line)
            if m1:
                acc = float(m1.group(1)) / 100.0
                accuracies.append(acc)
                if len(accuracies) >= max_samples:
                    break
                continue
            m2 = pattern2.search(line)
            if m2:
                acc = float(m2.group(1)) / 100.0
                accuracies.append(acc)
                if len(accuracies) >= max_samples:
                    break
    return np.array(accuracies)

def ci_normal(accuracies, N, conf_level):
    n = len(accuracies)
    mean = np.mean(accuracies) # 计算均值
    std = np.std(accuracies, ddof=1) # 计算样本标准差，ddof=1表示无偏估计（除以$n-1$）
    se = std / np.sqrt(n) # 计算均值的标准误差（standard error, SE），即标准差除以样本容量的平方根
    fpc = np.sqrt((N - n) / (N - 1)) # 计算有限总体修正系数（Finite Population Correction, FPC
    se_fpc = se * fpc # 计算修正后的标准误差（SE_FPC），将标准误乘以FPC。
    t_value = stats.t.ppf(1 - (1 - conf_level) / 2, df=n-1) # 查找t分布的临界值，conf_level为置信区间，如0.95
    # 计算置信区间
    ci_lower = mean - t_value * se_fpc
    ci_upper = mean + t_value * se_fpc
    return mean, ci_lower, ci_upper

def ci_bootstrap(accuracies, N, conf_level, n_boot=10000, random_seed=42):
    rng = np.random.default_rng(random_seed) # 创建一个随机数生成器对象 rng，用指定的种子，确保每次运行结果一致
    n = len(accuracies)
    means = []
    for _ in range(n_boot): # bootstrap主循环，重复n_boot次
        sample = rng.choice(accuracies, size=n, replace=True) # 从已有的accuracies中有放回地随机采样n个，形成一个bootstrap样本
        means.append(np.mean(sample))
    alpha = 1 - conf_level
    # 计算置信区间的百分位数下界和上界。例如置信度0.95时，下界是2.5分位（2.5%），上界是97.5分位（97.5%）
    lower_percentile = 100 * (alpha / 2)
    upper_percentile = 100 * (1 - alpha / 2)
    # 从所有bootstrap均值中，取出下界和上界的分位数，作为置信区间的下界和上界
    ci_lower = np.percentile(means, lower_percentile)
    ci_upper = np.percentile(means, upper_percentile)
    mean = np.mean(accuracies)
    return mean, ci_lower, ci_upper

def get_confidence_interval(logfile, N, max_samples=100, method="normal", conf_level=0.95):
    accuracies = get_accuracies(logfile, max_samples)
    n = len(accuracies)
    if n == 0:
        print("未找到任何匹配的正确率数据！")
        exit()
    if method == "normal":
        mean, ci_lower, ci_upper = ci_normal(accuracies, N, conf_level)
        method_name = "正态/Student-t方法"
    elif method == "bootstrap":
        mean, ci_lower, ci_upper = ci_bootstrap(accuracies, N, conf_level)
        method_name = "Bootstrap方法"
    else:
        print("未知method参数，仅支持normal或bootstrap")
        exit()
    ci_percent = int(conf_level * 100)
    print(f"方法: {method_name}")
    print(f"提取到{n}个准确率样本，均值: {mean:.4f}")
    print(f"{ci_percent}%置信区间: [{ci_lower:.4f}, {ci_upper:.4f}]")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="计算准确率的置信区间")
    parser.add_argument('--logfile', default="log/sample_test.log", help="日志文件名")
    parser.add_argument('--N', type=int, default=15552, help="配置空间大小")
    parser.add_argument('--max_samples', type=int, default=100, help="采样样本数")
    parser.add_argument('--method', default="normal", choices=["normal", "bootstrap"], help="计算方法: normal或bootstrap")
    parser.add_argument('--conf_level', type=float, default=0.95, help="置信水平，例如0.95或0.99")
    args = parser.parse_args()
    
    get_confidence_interval(args.logfile, args.N, args.max_samples, args.method, args.conf_level)