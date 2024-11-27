from deepface import DeepFace
import os
import pandas as pd

# 设置图像库路径
image_folder = "/task_datasets"
image_paths = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('.jpg', '.png'))]

# 创建一个 DataFrame 来存储结果
results = []

# 逐对比较图像
for i in range(len(image_paths)):
    for j in range(i + 1, len(image_paths)):
        img1_path = image_paths[i]
        img2_path = image_paths[j]
        
        # 使用 DeepFace 进行验证
        result = DeepFace.verify(img1_path, img2_path, model_name='VGG-Face', distance_metric='cosine')
        
        # 将结果存储到列表中
        results.append({
            "img1": img1_path,
            "img2": img2_path,
            "verified": result["verified"],
            "distance": result["distance"]
        })

# 将结果转换为 DataFrame
results_df = pd.DataFrame(results)

# 输出结果
print(results_df)

# 保存结果到 CSV 文件
results_df.to_csv("seal_identification_results.csv", index=False)