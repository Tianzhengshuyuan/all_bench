import pickle

with open('sample_data_v1.2.pkl', 'rb') as f:
    data = pickle.load(f)
print(data)
# 输出：{'a': 1, 'b': 2}