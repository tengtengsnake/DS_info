import os
import math
from PIL import Image

# 檔案讀取/寫入 必要手動修改區域 -> 這是第5行
image_files_path = r'C:\Users\peite\Desktop\yolov8_self\images' # 設定圖片資料集的路徑

yaml_file_path = r'C:\Users\peite\Desktop\yolov8_self' # 給yaml存的路徑

labels_files_path = r'C:\Users\peite\Desktop\yolov8_self\labels' # 設定圖片資料集txt的路徑

# 設定圖片資料集的拆分比例
train_rate = 0.7
val_rate = 0.1
test_rate = 0.2

if not os.path.exists(image_files_path): # 如果資料夾不存在,就離開
    print('資料夾不存在!')
    exit()
# 讀取資料夾中的圖片路徑
img_list = []
for img in os.listdir(image_files_path):
    if img.lower().endswith(('.jpg', '.jpeg', '.png','txt')):
        img_list.append(os.path.join(image_files_path, img))

# 計算訓練集,驗證集,測試集的大小
# 圖片組圖片總數
total_images = len(img_list) # 有17張圖片
# 訓練集圖片數
train_images = math.floor(total_images * train_rate)
# 驗證集圖片數
val_images = math.floor(total_images * val_rate)
# 測試集圖片數
test_images = total_images - train_images - val_images

print(f'訓練集圖片數: {train_images},驗證集圖片數: {val_images},測試集圖片數: {test_images}')

# 將圖片路經拆分成訓練集,驗證集,測試集

train_images_path = img_list[:train_images]
val_images_path = img_list[train_images:train_images+val_images] 
test_images_path = img_list[train_images+val_images:]

# 創建拆分後圖片的資料夾
train = 'train'
val = 'val'
test = 'test'

# 檔案是否已經存在
split_dirs = [train,val,test]
for split_dir in split_dirs:
    try:
        os.makedirs(os.path.join(image_files_path,split_dir))
    except FileExistsError:
        print(f'{split_dir} 檔案已經存在!')

# 將拆分好的訓練圖片打開,並存到拆分訓練圖片資料夾中
for image_path in train_images_path:  
    image = Image.open(image_path)
    image.save(os.path.join(image_files_path,train,os.path.basename(image_path))) 

for image_path in val_images_path: 
    image = Image.open(image_path)
    image.save(os.path.join(image_files_path,val,os.path.basename(image_path))) 
 
for image_path in test_images_path: 
    image = Image.open(image_path)
    image.save(os.path.join(image_files_path,test,os.path.basename(image_path))) 

print('圖片資料集拆分成功!')
# 撰寫yaml檔
yf = open(yaml_file_path+'\\require.yaml','w')
yf.write('train: '+os.path.join(image_files_path,train)+'\n')
yf.write('val: '+os.path.join(image_files_path,val)+'\n')
yf.write('test: '+os.path.join(image_files_path,test+'\n'))
yf.write('names:\n    0:car') 
yf.close()

print("必要yaml檔案撰寫完成!")

# 拆分.txt檔
if not os.path.exists(labels_files_path): # 如果資料夾不存在,就離開
    print('資料夾不存在!')
    exit()
img_list = []
for img in os.listdir(labels_files_path):
    if (img.endswith('.txt')): # 如果資料夾中有txt格式
        img_list.append(os.path.join(labels_files_path,img)) # 取得圖片並放入圖片清單

train_images_path = img_list[:train_images]
val_images_path = img_list[train_images:train_images+val_images] 
test_images_path = img_list[train_images+val_images:]

train = 'train'
val = 'val'
test = 'test'

split_dirs = [train,val,test]

for split_dir in split_dirs:
    try:
        os.makedirs(os.path.join(labels_files_path, split_dir))
    except FileExistsError:
        print(f'{split_dir} 資料夾已經存在!')

for image_txt_path in train_images_path: 
    with open(image_txt_path,'r') as train_input_file:
        train_file_contents = train_input_file.read()
    with open(os.path.join(labels_files_path,train,os.path.basename(image_txt_path)),'w') as train_ouput_file: 
        train_ouput_file.write(train_file_contents)

for image_txt_path in val_images_path: 
    with open(image_txt_path,'r') as val_input_file:
        val_file_contents = val_input_file.read()
    with open(os.path.join(labels_files_path,val,os.path.basename(image_txt_path)),'w') as val_ouput_file: 
        val_ouput_file.write(val_file_contents)  

for image_txt_path in test_images_path: 
    with open(image_txt_path,'r') as test_input_file:
        test_file_contents = test_input_file.read()
    with open(os.path.join(labels_files_path,test,os.path.basename(image_txt_path)),'w') as test_ouput_file: 
            test_ouput_file.write(test_file_contents)

print('圖片txt資料集拆分成功!')
