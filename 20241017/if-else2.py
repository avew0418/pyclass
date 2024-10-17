# 輸入：使用者的錢以及今天是否吃了布丁
money = int(input("你有多少錢？(以新台幣計算): "))
ate_pudding_today = input("今天有吃布丁嗎？(是/否): ").strip().lower()

# 根據流程圖進行決策
if money > 100:
    if ate_pudding_today == "是":
        print("吃蛋糕。")
    else:
        print("買布丁。")
else:
    print("買優惠鮮乳。")
