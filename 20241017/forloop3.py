# 輸出金字塔形狀的聖誕樹
rows = 9  # 行數設定

for i in range(1, rows+1):
    # 輸出空格，使得星星居中
    print(" " * (rows - i), end="")
    
    # 輸出星星
    print("*" * (2 * i - 1))

for i in range(rows):
    for j in range(i):
        print(i,end="")

    print()