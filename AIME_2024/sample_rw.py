import random
import pickle
sample_data = []
for cot in [0,1]:
    for Temperature in [0.0,1.0,2.0]:
        for max_tokens in [10,8192,32768]:  
            for top_p in [0.2,0.6,1.0]:
                for presence_penalty in [-0.5,0.5,1.5]:
                    one_data = {
                        "language":"yy",
                        "cot":cot,
                        "few":0,
                        "mul":0,
                        "question_type":1,
                        "question_tran":0,
                        "Temperature":Temperature,
                        "max_tokens":max_tokens,
                        "top_p":top_p,
                        "presence_penalty":presence_penalty
                    }
                    sample_data.append(one_data)
random.shuffle(sample_data)
print(sample_data)

with open("related_work_data.pkl", "wb") as f:  # 'wb' 表示二进制写入
    pickle.dump(sample_data, f)