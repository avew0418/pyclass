# 輸入使用者的身高和體重
height = float(input("請輸入身高(公尺): "))
weight = float(input("請輸入體重(公斤): "))

# 計算 BMI
bmi = weight / (height ** 2)

# 判斷 BMI 的結果
if bmi >= 27:
    print("肥胖")
elif bmi >= 24:
    print("過重")
elif bmi >= 18:
    print("健康")
else:
    print("過輕")
