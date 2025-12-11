import argparse
import numpy as np
import sys
import re
from scipy.stats import beta

# ======================
# 正则匹配日志中的准确率
# ======================
pattern1 = re.compile(
    r"总题组数:\s*\d+.*?第一轮正确答案数:\s*\d+.*?正确率:\s*[\d.]+%.*?第二轮正确答案数:\s*\d+.*?正确率:\s*([\d.]+)%"
)
pattern2 = re.compile(
    r"总题数:\s*(\d+).*?正确数:\s*(\d+).*?正确率:\s*([\d.]+)%,\s*耗时:"
)

def get_accuracies(logfile, start=0, max_samples=100):
    """
    从日志文件中获取准确率数据 (0~1)，以及可能的(正确数, 总题数)
    """
    accuracies = []
    counts = []  # (correct, total) 如果提取不到则 None

    with open(logfile, 'r', encoding='utf-8') as f:
        for line in f:
            m1 = pattern1.search(line)
            if m1:
                acc = float(m1.group(1)) / 100.0
                accuracies.append(acc)
                counts.append(None)
                continue
            m2 = pattern2.search(line)
            if m2:
                total = int(m2.group(1))
                correct = int(m2.group(2))
                acc = float(m2.group(3)) / 100.0
                accuracies.append(acc)
                counts.append((correct, total))

    if len(accuracies) == 0:
        print("❌ 未能从日志文件中抽取到准确率数据，请检查日志内容和正则表达式。")
        sys.exit(1)

    if start >= len(accuracies):
        print(f"❌ 指定的起始样本 {start} 超出日志中样本数量 {len(accuracies)}")
        sys.exit(1)

    accuracies = accuracies[start:start + max_samples]
    counts = counts[start:start + max_samples]
    return np.array(accuracies), counts

# ======================
# 贝叶斯样本量估计
# ======================
def bayesian_sample_size(error=0.03, confidence=0.95, alpha_prior=1, beta_prior=1,
                         questions_per_sample=None, accuracies=None, counts=None, max_n=10000):
    """
    使用贝叶斯方法估计所需样本量 (基于可信区间宽度)
    - error: 允许的最大误差 (置信区间半宽)
    - confidence: 置信水平
    - alpha_prior, beta_prior: Beta先验参数
    - questions_per_sample: 如果日志没有题数，假设每个样本固定题数
    - accuracies: 日志提取的准确率
    - counts: 日志提取的(正确数, 总题数)，可能有None
    - max_n: 最大搜索范围
    """

    # 确定总 correct, total
    total_correct, total_questions = 0, 0
    for acc, c in zip(accuracies, counts):
        if c is not None:
            correct, total = c
            total_correct += correct
            total_questions += total
        else:
            if questions_per_sample is None:
                raise ValueError("日志缺少题目数，请指定 --questions_per_sample")
            correct = int(round(acc * questions_per_sample))
            total_correct += correct
            total_questions += questions_per_sample

    # 先验
    alpha = alpha_prior
    beta_param = beta_prior

    # 目标区间宽度
    target_width = 2 * error
    lower_q = (1 - confidence) / 2
    upper_q = 1 - lower_q

    # 遍历样本量
    for n in range(1, max_n + 1):
        # 最保守情况：假设成功率在 0.5 附近
        k = int(n * 0.5)
        alpha_post = alpha + k
        beta_post = beta_param + n - k

        lower = beta.ppf(lower_q, alpha_post, beta_post)
        upper = beta.ppf(upper_q, alpha_post, beta_post)
        width = upper - lower

        if width <= target_width:
            print(f"✅ 所需最小样本量: {n}, 区间宽度: {width:.4f} ≤ {target_width}")
            return n

    print(f"⚠️ 在 {max_n} 样本范围内未找到满足条件的样本量")
    return None

# ======================
# 主程序入口
# ======================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="基于日志的贝叶斯样本量估计")
    parser.add_argument("--log", default="log/sample_test.log", help="日志文件路径")
    parser.add_argument("--error", type=float, default=0.03, help="允许的最大误差 (置信区间半宽，如0.03)")
    parser.add_argument("--confidence", type=float, default=0.95, help="置信水平 (如0.95/0.99)")
    parser.add_argument("--alpha_prior", type=float, default=1, help="Beta先验参数α")
    parser.add_argument("--beta_prior", type=float, default=1, help="Beta先验参数β")
    parser.add_argument("--max_samples", type=int, default=500, help="最多使用多少个样本")
    parser.add_argument("--start", type=int, default=0, help="从第几个样本开始取数据 (0 表示第一个样本)")
    parser.add_argument("--questions_per_sample", type=int, default=100, help="当日志缺少题目数时，假设每个样本题目数")
    parser.add_argument("--max_n", type=int, default=500, help="搜索的最大样本量")
    args = parser.parse_args()

    # 读取日志数据
    accuracies, counts = get_accuracies(args.log, args.start, max_samples=args.max_samples)

    # 样本量估计
    bayesian_sample_size(error=args.error, confidence=args.confidence,
                         alpha_prior=args.alpha_prior, beta_prior=args.beta_prior,
                         questions_per_sample=args.questions_per_sample,
                         accuracies=accuracies, counts=counts, max_n=args.max_n)