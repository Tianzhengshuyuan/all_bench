# ANOVA vs Mixed Effects Model：因子效应报告方式的差异

## 问题概述

两个脚本都使用分类变量，但报告方式不同：
- **ANOVA** (`get_main_anova_dir.py`)：报告**每个因子（factor）的整体效应**
- **Mixed Effects Model** (`get_mix_effect.py`)：报告**因子特定取值（level）的效应**

## 核心差异

### 1. ANOVA：因子整体效应

**方法**：使用 Type II ANOVA (`anova_lm(model, typ=2)`)

**原理**：
- ANOVA 将每个因子作为一个**整体**来评估
- 计算该因子所有水平（levels）共同贡献的**平方和（Sum of Squares, SS）**
- 通过 F 检验判断整个因子是否显著

**输出示例**（`deepseekv3.log`）：
```
factor              obs_eta2  p_value
Question Format     0.399643  0.000000
COT                 0.080156  0.000000
max_tokens          0.028099  0.000000
```

**含义**：
- `Question Format` 作为一个整体，解释了 39.96% 的方差
- 不区分 `question_type=0` 和 `question_type=1` 的具体效应
- 只回答："Question Format 这个因子是否重要？"

### 2. Mixed Effects Model：因子水平效应

**方法**：使用回归框架（R 的 `glmer` 或 Python 的 `MixedLM`）

**原理**：
- 将分类变量编码为**虚拟变量（dummy variables）**
- 每个因子的每个水平（除了参考水平）都有一个**系数（coefficient）**
- 系数表示该水平相对于参考水平的效应

**输出示例**（`deepseekv3_r_mixed_question_aug.txt`）：
```
                       Estimate  Pr(>|z|)
cot1                    -1.5933  1.64e-268
question_type1          -0.8181  3.74e-80
max_tokens4000           0.7890  2.85e-50
max_tokens100            0.1927  2.39e-04
```

**含义**：
- `cot1`：使用 COT（cot=1）相对于不使用 COT（cot=0，参考水平）的效应是 -1.59
- `max_tokens4000`：max_tokens=4000 相对于参考水平的效应是 +0.79
- `max_tokens100`：max_tokens=100 相对于参考水平的效应是 +0.19
- 回答："每个具体取值相对于参考水平的影响是什么？"

## 技术实现细节

### ANOVA 实现（`get_main_anova_dir.py`）

```python
# 第 119-128 行：构建公式
main_effects = [
    "C(language)", "C(question_type)", "C(question_tran)",
    "C(few)", "C(cot)", "C(mul)",
    "C(Temperature)", "C(max_tokens)", "C(top_p)", "C(presence_penalty)"
]
formula = "accuracy ~ " + " + ".join(main_effects)

# 第 81-110 行：permutation_test_anova_eta 函数
model = ols(formula, data=df).fit()
anova_res = anova_lm(model, typ=2)  # Type II ANOVA

# 计算 eta²（效应量）
ss_total = anova_res["sum_sq"].sum()
obs_eta = (anova_res["sum_sq"] / ss_total).drop("Residual")
```

**关键点**：
- `C()` 表示分类变量，但 ANOVA 将整个因子作为一个**整体**处理
- `anova_lm(typ=2)` 计算每个因子的**整体平方和**（所有水平共同贡献）
- 不区分因子内部的不同水平
- **输出**：每个因子只有一行结果（如 `Question Format: 0.399643`）

### Mixed Effects Model 实现（`get_mix_effect.py`）

```python
# 第 826-833 行：构建公式（R 脚本）
formula = (
    "accuracy ~ "
    "language + question_type + question_tran + "
    "few + cot + mul + "
    "Temperature + max_tokens + top_p + presence_penalty + "
    "(1|question_id) + (1|augmentation)"
)

# 第 858-870 行：R 脚本中转换为因子
df$language <- as.factor(df$language)
df$cot <- as.factor(df$cot)
df$max_tokens <- as.factor(df$max_tokens)
# ... 其他因子

# 第 878-879 行：拟合模型
model <- glmer(formula, data = df, family = binomial(link = "logit"))

# 第 888-912 行：输出系数
coef_summary <- summary(model)$coefficients
```

**关键点**：
- R 的 `as.factor()` 将变量转换为因子类型
- `glmer` 自动将因子编码为**虚拟变量**（dummy variables）
- 每个水平（除了参考水平）都有一个系数
- **输出**：每个因子的每个水平一行（如 `cot1: -1.5933`, `max_tokens4000: 0.7890`）

### 编码差异示例

假设 `cot` 有两个水平：`0`（不使用）和 `1`（使用）

**ANOVA 方式**：
```python
# 公式中使用 C(cot)
formula = "accuracy ~ C(cot)"
# 内部会创建虚拟变量，但 ANOVA 只报告整个因子的平方和
# 输出：COT 因子整体 eta² = 0.080156
```

**Mixed Effects 方式**：
```r
# R 自动编码
cot (因子) → cot1 (虚拟变量，cot=0 是参考水平)
# 输出：
#   (Intercept): -1.11  (参考水平：cot=0 的截距)
#   cot1: -1.59         (cot=1 相对于 cot=0 的效应)
```

**关键区别**：
- ANOVA：`C(cot)` → 报告整个因子的效应（1 行）
- Mixed Effects：`cot` → 报告每个水平的效应（每个水平 1 行，参考水平除外）

## 为什么会有这种差异？

### ANOVA 的设计目标
- **整体检验**：判断因子是否重要
- **方差分解**：将总方差分解到各个因子
- **适合**：探索性分析，找出重要因子

### Mixed Effects Model 的设计目标
- **具体效应**：量化每个水平的具体影响
- **预测和解释**：可以预测特定配置的效果
- **适合**：需要知道"使用 cot=1 比 cot=0 好多少"

## 实际例子对比

### 例子 1：COT 因子（2 个水平：0=不使用, 1=使用）

**ANOVA 报告**（`deepseekv3.log`）：
```
factor    obs_eta2    p_value
COT       0.080156    0.000000
```
**解读**：
- COT 因子整体很重要，解释了 8.02% 的方差
- **但不知道**：是 cot=1 更好还是 cot=0 更好
- **只回答**："COT 这个因子是否重要？" → 是

**Mixed Effects Model 报告**（`deepseekv3_r_mixed_question_aug.txt`）：
```
           Estimate   Pr(>|z|)
(Intercept) -1.1109   1.67e-03   # cot=0 的基准截距
cot1         -1.5933  1.64e-268  # cot=1 相对于 cot=0 的效应
```
**解读**：
- `cot1` 的系数是 **-1.59**（负数）
- 在 logit 尺度上，使用 COT（cot=1）比不使用 COT（cot=0）的对数几率**低 1.59**
- 转换为概率：使用 COT 的准确率**更低**
- **具体回答**："使用 COT 比不使用 COT 差多少？" → 对数几率低 1.59

### 例子 2：max_tokens 因子（多个水平：100, 4000, ...）

**ANOVA 报告**：
```
factor       obs_eta2    p_value
max_tokens    0.028099    0.000000
```
**解读**：
- max_tokens 因子整体重要，解释了 2.81% 的方差
- **但不知道**：哪个取值（100, 4000, ...）更好

**Mixed Effects Model 报告**：
```
                Estimate   Pr(>|z|)
max_tokens4000    0.7890   2.85e-50   # 4000 相对于参考水平
max_tokens100     0.1927   2.39e-04   # 100 相对于参考水平
```
**解读**：
- `max_tokens4000` 系数是 **+0.79**（正数，最好）
- `max_tokens100` 系数是 **+0.19**（正数，但较小）
- **结论**：max_tokens=4000 比参考水平好 0.79，max_tokens=100 比参考水平好 0.19
- **具体回答**："哪个 max_tokens 值最好？" → 4000

### 例子 3：question_type 因子

**ANOVA 报告**：
```
factor          obs_eta2    p_value
Question Format  0.399643    0.000000
```
**解读**：Question Format 是最重要的因子，解释了 39.96% 的方差

**Mixed Effects Model 报告**：
```
                Estimate   Pr(>|z|)
question_type1   -0.8181   3.74e-80
```
**解读**：
- `question_type1` 系数是 **-0.82**（负数）
- question_type=1 相对于 question_type=0 的效应是负的
- **具体回答**："哪种问题格式更好？" → question_type=0（参考水平）

## 混合效应模型也可以进行因子整体检验！

**重要更新**：混合效应模型不仅可以报告每个水平的具体效应，**也可以进行因子整体检验**，类似 ANOVA！

### 方法：似然比检验（Likelihood Ratio Test）

在 R 的 `lme4` 包中，可以使用 `drop1()` 函数来测试每个因子的整体显著性：

```r
# 测试每个因子作为整体的显著性
drop1_result <- drop1(model, test = "Chisq")
```

**原理**：
- 比较完整模型 vs 去掉该因子后的模型
- 使用似然比检验（LRT）判断因子是否显著
- 类似于 ANOVA 的整体检验，但适用于混合效应模型

**输出示例**（已添加到代码中）：
```
---- Overall Factor Significance (Likelihood Ratio Test) ----
Factor            Df    AIC      LRT      Pr(>Chi)  Pseudo_R2_contrib
cot               1     14250    1250.5   < 2e-16   0.45
question_type     1     14280    980.2    < 2e-16   0.35
max_tokens        3     14290    120.5    < 2e-16   0.04
...
```

**解读**：
- `LRT`：似然比统计量，越大说明因子越重要
- `Pr(>Chi)`：p 值，判断因子是否显著
- `Pseudo_R2_contrib`：相对贡献度，类似 ANOVA 的 eta²

### 两种报告方式对比

| 报告方式 | 回答的问题 | 输出内容 |
|---------|-----------|---------|
| **因子整体检验**（`drop1()`） | "这个因子重要吗？" | 每个因子 1 行，整体显著性 |
| **水平具体效应**（`summary()`） | "这个具体取值的影响是什么？" | 每个水平 1 行，具体系数 |

## 总结

| 维度 | ANOVA | Mixed Effects Model |
|------|-------|---------------------|
| **因子整体检验** | ✅ eta²（效应量） | ✅ LRT（似然比检验） |
| **水平具体效应** | ❌ 不提供 | ✅ 系数（Estimate） |
| **统计量** | eta², F 统计量 | LRT, 系数, z 值 |
| **回答的问题** | "这个因子重要吗？" | "这个因子重要吗？" + "这个具体取值的影响是什么？" |
| **输出行数（整体）** | 每个因子 1 行 | 每个因子 1 行 |
| **输出行数（水平）** | 无 | 每个水平 1 行（除参考水平） |
| **适用场景** | 探索性分析，因子筛选 | 因子筛选 + 具体效应量化 + 预测 |

## 如何选择？

- **用 ANOVA**：
  - 简单快速，适合初步探索
  - 不需要考虑随机效应时
  
- **用 Mixed Effects**：
  - ✅ **既可以做因子整体检验**（类似 ANOVA）
  - ✅ **又可以看具体水平效应**（ANOVA 做不到）
  - 需要处理随机效应（如题目、扰动类型）时
  - 需要预测和优化配置时

**结论**：混合效应模型功能更全面，既能做整体检验，又能看具体效应！
