total_cost = 0

print("請輸入每樣菜品的金額 (輸入 0 來結束):")

while True:
    dish_cost = float(input("菜品金額: "))
    
    if dish_cost == 0:
        break
    
    total_cost += dish_cost

num_people = int(input("請輸入幾個人分攤: "))

cost_per_person = round(total_cost / num_people)

print(f"每個人分攤的費用為: {cost_per_person} 元")
