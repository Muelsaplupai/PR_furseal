import csv
import re
from collections import defaultdict

# 读取CSV文件
def read_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # 跳过标题行
        data = [row for row in reader]
    return headers, data

# 写入CSV文件
def write_csv(file_path, headers, rows):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for row in rows:
            writer.writerow(row)

# 分配ID
def assign_ids(data):
    face_ids = {}
    jpg_ids = {}
    results = []

    for img1, img2, _, distance in data:
        # 移除路径，只保留文件名
        img1 = re.findall(r'[^\\]+$', img1)[0]
        img2 = re.findall(r'[^\\]+$', img2)[0]

        # 提取基本图片名称，忽略末尾的"_数字"
        base_img1 = re.sub(r'(.*)_\d\.jpg$', r'\1.jpg', img1)
        base_img2 = re.sub(r'(.*)_\d\.jpg$', r'\1.jpg', img2)

        # 分配脸ID
        face_id1 = face_ids.setdefault(img1, len(face_ids) + 1)
        face_id2 = face_ids.setdefault(img2, len(face_ids) + 1)

        # 如果两张图片是同一张脸，更新face_id2为face_id1
        if float(distance) >= 0.35:
            face_id2 = face_id1

        # 分配jpgID，如果图片名有后缀，则使用基础图片名的jpgID
        jpg_id1 = jpg_ids.setdefault(base_img1, len(jpg_ids) + 1)
        jpg_id2 = jpg_ids.setdefault(base_img2, jpg_id1 if base_img1 == base_img2 else len(jpg_ids) + 1)

        # 保存结果，确保每个图片只记录一次
        if img1 not in [row[0] for row in results]:
            results.append([img1, jpg_id1, face_id1])
        if img2 not in [row[0] for row in results] and img2 != img1:
            results.append([img2, jpg_id2, face_id2])

    return results

def main():
    # 读取数据
    file_path = 'seal_identification_results.csv'
    headers, data = read_csv(file_path)
    headers=['img','jpgID','faceID']
    # 分配ID
    assigned_rows = assign_ids(data)

    # 写入CSV文件
    output_file_path = 'ID_index.csv'
    write_csv(output_file_path, headers, assigned_rows)

    print("CSV文件已生成并保存在根目录下。")

if __name__ == "__main__":
    main()
