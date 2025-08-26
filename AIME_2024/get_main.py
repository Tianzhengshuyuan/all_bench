import os
import re
import argparse
import pandas as pd
import numpy as np
from sklearn.linear_model import LassoCV, RidgeCV, ElasticNetCV
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from collections import defaultdict
from sklearn.exceptions import ConvergenceWarning
import warnings
import ast
import shap

try:
    from xgboost import XGBRegressor
    has_xgb = True
except ImportError:
    has_xgb = False

# 正则模式
config_pattern = re.compile(r"配置:\s*(\{.*\})")
acc_pattern1 = re.compile(r"总题数:\s*\d+.*?正确数:\s*\d+.*?正确率:\s*([\d.]+)%")
acc_pattern2 = re.compile(r"总题组数:\s*\d+.*?第一轮正确答案数:\s*\d+.*?正确率:\s*[\d.]+%.*?第二轮正确答案数:\s*\d+.*?正确率:\s*([\d.]+)%")

def parse_logs(input_folder):
    """逐个文件解析日志，返回 dict: {filename: DataFrame}"""
    file_data = {}
    for fname in os.listdir(input_folder):
        if not (fname.endswith(".log") and fname.startswith("sample_test_")):
            continue
        filepath = os.path.join(input_folder, fname)
        data = []
        with open(filepath, 'r', encoding='utf-8') as f:
            current_config = None
            for line in f:
                # 捕获配置
                m_cfg = config_pattern.search(line)
                if m_cfg:
                    cfg_str = m_cfg.group(1)
                    try:
                        current_config = ast.literal_eval(cfg_str)  
                    except Exception as e:
                        print("配置解析失败:", e, cfg_str)
                        current_config = None
                    continue
                
                # 捕获准确率（模式1）
                m_acc1 = acc_pattern1.search(line)
                if m_acc1 and current_config is not None:
                    acc = float(m_acc1.group(1)) / 100.0
                    row = current_config.copy()
                    row['accuracy'] = acc
                    data.append(row)
                    current_config = None
                    continue

                # 捕获准确率（模式2）
                m_acc2 = acc_pattern2.search(line)
                if m_acc2 and current_config is not None:
                    acc = float(m_acc2.group(1)) / 100.0
                    row = current_config.copy()
                    row['accuracy'] = acc
                    data.append(row)
                    current_config = None
                    continue
        if data:
            file_data[fname] = pd.DataFrame(data)
    return file_data

def compare_models_on_test_set(all_data, model_names, test_size=0.25):
    # 记录每个文件、每个模型的test R2
    r2_dict = defaultdict(dict)

    for fname, df in all_data.items():
        if df.shape[0] < 5:
            print(f"⚠️ 文件 {fname} 数据太少，跳过")
            continue

        X = df.drop(columns=['accuracy'])
        y = df['accuracy']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

        for model_name in model_names:
            # 构造预处理和模型对象
            if args.merge_languages:
                categorical = ['cot', 'few', 'mul', 'question_type', 'question_tran']
                categorical = [c for c in categorical if c in X.columns]
                numeric = [col for col in X.columns if col not in categorical + ['language']]
                preprocessor = ColumnTransformer(
                    transformers=[
                        ('lang', OrdinalEncoder(categories=[['yy','zw','ey','ry','fy','alby']]), ['language']),
                        ('cat', 'passthrough', categorical),
                        ('num', 'passthrough', numeric)
                    ]
                )
            else:
                categorical = ['language', 'cot', 'few', 'mul', 'question_type', 'question_tran']
                categorical = [c for c in categorical if c in X.columns]
                numeric = [col for col in X.columns if col not in categorical]
                preprocessor = ColumnTransformer(
                    transformers=[
                        ('cat', OneHotEncoder(drop='first'), categorical),
                        ('num', 'passthrough', numeric)
                    ]
                )

            if model_name == 'lasso':
                model = Pipeline(steps=[
                    ('preprocessor', preprocessor),
                    ('reg', LassoCV(alphas=np.logspace(-4, 0, 50), cv=5, random_state=42))
                ])
            elif model_name == 'ridge':
                model = Pipeline(steps=[
                    ('preprocessor', preprocessor),
                    ('reg', RidgeCV(alphas=np.logspace(-4, 0, 50), cv=5))
                ])
            elif model_name == 'elastic':
                model = Pipeline(steps=[
                    ('preprocessor', preprocessor),
                    ('reg', ElasticNetCV(l1_ratio=0.01, alphas=np.logspace(-4, 0, 50), cv=5, random_state=42))
                ])
            elif model_name == 'rf':
                model = Pipeline(steps=[
                    ('preprocessor', preprocessor),
                    ('reg', RandomForestRegressor(n_estimators=200, random_state=42))
                ])
            elif model_name == 'xgb' and has_xgb:
                model = Pipeline(steps=[
                    ('preprocessor', preprocessor),
                    ('reg', XGBRegressor(n_estimators=200, random_state=42, verbosity=0))
                ])
            else:
                continue

            colname = fname[len("sample_test_"):-len(".log")]  # 去掉前缀和后缀
            try:
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", category=ConvergenceWarning)
                    model.fit(X_train, y_train)
                    y_pred = model.predict(X_test)
                    r2 = r2_score(y_test, y_pred)
                r2_dict[model_name][colname] = r2
            except Exception as e:
                print(f"模型 {model_name} 在文件 {fname} 训练失败: {e}")
                r2_dict[model_name][colname] = float("nan")

    # 汇总成DataFrame
    df_r2 = pd.DataFrame(r2_dict).T  # 行是模型，列是文件
    df_r2['mean_r2'] = df_r2.mean(axis=1)
    df_r2 = df_r2.sort_values('mean_r2', ascending=False)
    print("\n测试集R2分数表（行：模型，列：文件，mean_r2为平均值）：\n")
    print(df_r2.round(4))
    print("\n模型排名（按平均测试集R2分数）：")
    for i, (model, row) in enumerate(df_r2.iterrows(), 1):
        print(f"{i}. {model}: 平均测试集R2 = {row['mean_r2']:.4f}")
        
def run_model_analysis(df, fname):
    """针对单个文件的 DataFrame 运行分析"""
    if df.shape[0] < 5:
        print(f"⚠️ 文件 {fname} 数据太少，无法建模")
        return None

    # 特征与标签
    X = df.drop(columns=['accuracy'])
    y = df['accuracy']

    # 区分类别型和数值型
    if args.merge_languages:
        categorical = ['cot', 'few', 'mul', 'question_type', 'question_tran']
        categorical = [c for c in categorical if c in X.columns]
        numeric = [col for col in X.columns if col not in categorical + ['language']]
        preprocessor = ColumnTransformer(
            transformers=[
                ('lang', OrdinalEncoder(categories=[['yy','zw','ey','ry','fy','alby']]), ['language']),
                ('cat', 'passthrough', categorical),
                ('num', 'passthrough', numeric)
            ]
        )
    else:
        categorical = ['language', 'cot', 'few', 'mul', 'question_type', 'question_tran']
        categorical = [c for c in categorical if c in X.columns]
        numeric = [col for col in X.columns if col not in categorical]
        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', OneHotEncoder(drop='first'), categorical),
                ('num', 'passthrough', numeric)
            ]
        )

    # 选择模型
    if args.model == 'lasso':
        print("Using [ Lasso ] Regression")
        model = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('reg', LassoCV(alphas=np.logspace(-4, 0, 50), cv=5, random_state=42))
        ])
    elif args.model == 'ridge':
        print("Using [ Ridge ] Regression")
        model = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('reg', RidgeCV(alphas=np.logspace(-4, 0, 50), cv=5))
        ])
    elif args.model == 'elastic':
        print("Using [ ElasticNet ] Regression")
        model = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('reg', ElasticNetCV(l1_ratio=0.01, alphas=np.logspace(-4, 0, 50), cv=5, random_state=42))
        ])
    elif args.model == 'rf':
        print("Using [ Random Forest ] Regressor")
        model = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('reg', RandomForestRegressor(n_estimators=200, random_state=42))
        ])
    elif args.model == 'xgb' and has_xgb:
        print("Using [ XGBoost ] Regressor")
        model = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('reg', XGBRegressor(n_estimators=200, random_state=42, verbosity=0))
        ])
    else:
        raise ValueError(f"未知模型 {args.model}")

    # 训练
    model.fit(X, y)
    y_pred = model.predict(X)
    print("R2 score on training data:", r2_score(y, y_pred))

    # 取出特征名
    if args.merge_languages:
        feature_names = ['language'] + categorical + numeric
    else:
        feature_names = []
        if categorical:
            ohe = model.named_steps['preprocessor'].named_transformers_['cat']
            cat_names = ohe.get_feature_names_out(categorical)
            feature_names.extend(cat_names)
        feature_names.extend(numeric)

    reg = model.named_steps['reg']

    # 线性模型：直接取系数
    if args.model in ['lasso', 'ridge', 'elastic']:
        coefs = reg.coef_
        importance = pd.DataFrame({'feature': feature_names, 'coef': coefs})
        importance['abs_coef'] = importance['coef'].abs()
        importance = importance.sort_values(by=['abs_coef', 'feature'], ascending=[False, True], kind="mergesort")
    else:
        # 树模型：用 SHAP 解释
        X_trans = model.named_steps['preprocessor'].transform(X)
        explainer = shap.TreeExplainer(reg)
        shap_values = explainer.shap_values(X_trans)
        shap_importance = np.abs(shap_values).mean(axis=0)
        importance = pd.DataFrame({'feature': feature_names, 'shap_importance': shap_importance})
        importance = importance.sort_values(by='shap_importance', ascending=False)

    # 重置索引
    importance = importance.reset_index(drop=True)
    importance.index = importance.index + 1  

    print("🚩 Top factors affecting accuracy:\n------------------------------------------------")
    print(importance.head(15))
    print("\n")
    return importance


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse logs and run model analysis")
    parser.add_argument('--input_folder', default="log", help="Folder containing log files")
    parser.add_argument('--merge_languages', action='store_true')
    parser.add_argument('--model', choices=['lasso', 'ridge', 'elastic', 'rf', 'xgb'], default='lasso')
    parser.add_argument('--test', action='store_true')
    args = parser.parse_args()
    all_data = parse_logs(args.input_folder)
    print(f"共解析到 {len(all_data)} 个日志文件\n")

    if args.test:
        model_names = ['lasso', 'ridge', 'elastic', 'rf']
        if has_xgb:
            model_names.append('xgb')
        compare_models_on_test_set(all_data, model_names)
    else:
        results = {}
        all_importance = []
        for fname, df in all_data.items():
            print(f"📂 Parsed {fname}, shape={df.shape}")
            importance = run_model_analysis(df, fname)
            if importance is not None:
                results[fname] = importance
                all_importance.append(importance.set_index('feature'))

        # === 🔥 聚合所有log的结果 ===
        if all_importance:
            combined = pd.concat(all_importance, axis=1)

            # 如果是线性模型：用 abs_coef
            if args.model in ['lasso','ridge','elastic']:
                metric = 'abs_coef'
            else:
                metric = 'shap_importance'

            # 取均值作为全局重要性
            combined_mean = combined.groupby(combined.index).mean()
            combined_mean = combined_mean[[metric]].mean(axis=1).sort_values(ascending=False)

            print(f"\n🚩 Overall factor importance across all logs using {args.model}:\n------------------------------------------------")
            print(combined_mean.round(6))