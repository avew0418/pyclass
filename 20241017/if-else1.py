# 輸入成績
score = int(input("請輸入成績: "))

# 根據成績判斷等第
if score >= 90:
    print("成績等級是 A")
elif score >= 80:
    print("成績等級是 B")
elif score >= 70:
    print("成績等級是 C")
else:
    print("成績等級是 D")
