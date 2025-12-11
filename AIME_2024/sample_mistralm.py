import random
import pickle
sample_data = []
#["output_few_format.json"]:#,"output_alby_format.json","output_ey_format.json","output_fy_format.json","output_ry_format.json","output_yy_format.json"]
for presence_penalty in [0.5]:
    for Temperature in [1.0]:
        for top_p in [0.6]:
            for question_tran in [0]:
                for few in [0,1]:
                    for mul in [0,1]:
                        for language in ["alby","ey","fy","ry","yy","zw"]:
                            for max_tokens in [10,100,4000]:  
                                for cot in [0,1]:
                                    for question_type in [0,1]:
                                        one_data = {
                                            "language":language,
                                            "cot":cot,
                                            "few":few,
                                            "mul":mul,
                                            "question_type":question_type,
                                            "question_tran":question_tran,
                                            "Temperature":Temperature,
                                            "max_tokens":max_tokens,
                                            "top_p":top_p,
                                            "presence_penalty":presence_penalty
                                        }
                                        sample_data.append(one_data)
random.shuffle(sample_data)
print(sample_data)

with open("sample_mistralm.pkl", "wb") as f:  # 'wb' 表示二进制写入
    pickle.dump(sample_data, f)