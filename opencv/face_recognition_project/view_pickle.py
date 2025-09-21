import pickle

ENCODINGS_PATH = "data/encodings.pickle"

with open(ENCODINGS_PATH, "rb") as f:
    data = pickle.load(f)

print("已知人臉數量：", len(data["encodings"]))
print("已知人名：", data["names"])

# 如果想看第一筆向量
if data["encodings"]:
    print("第一個人臉向量 (前10個數值)：", data["encodings"][0][:10])
