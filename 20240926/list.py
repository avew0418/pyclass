# 有序可變動列表 List
grades = [12, 60, 25, 70, 90]
print(grades)            # 輸出整個列表
print(grades[0])         # 輸出列表中的第一個元素
print(grades[3])         # 輸出列表中的第四個元素
print(grades[1:4])       # 輸出從第二個到第四個的元素，範圍為[1,4)，不包含索引4
grades = [12, 60, 25, 70, 90]
grades[0] = 55           # 把 55 放到列表中的第一個位置
print(grades)            # 輸出修改後的列表

grades = [12, 60, 25, 70, 90]
grades[1:4] = []  # 連續刪除列表中從編號 1 到編號 4 (不包括4)
print(grades)

grades = [12, 60, 25, 70, 90]
grades = grades + [12, 33]  # 後面加上列表
print(grades)

grades = [12, 60, 25, 70, 90]  # 取得列表的長度 len(列表資料)
length = len(grades)
print(length)

data = [[3, 4, 5], [6, 7, 8]]  # 巢狀列表
print(data[0])  # 輸出巢狀列表的第一個子列表


print(data[0])
print(data[0][1])
print(data[0][0:2])
print(data)

data[0][0:2] = [5, 5, 5]  # 資料取代
print(data)

# 有序不可變動列表 Tuple
data = (3, 4, 5)
# data[0] = 5  # 錯誤：Tuple的資料不可以變動
print(data[2])
print(data[0:2])

# copy list
a=[0,1,2,3,4,5]
b = a[:]
c= a.copy()
d = list(a)
print('copy list')
print(a)
print(b)
print(c)
print(d)

# list method ( offset )
a=['apple','banana','banana','orange']
print(a.index('banana'))#1

# len()
print(len(a))#4

#count()
print(a.count('banana'))#2
print(a.count('orange'))#1

# in()
print('banana' in a)#True
print('watermelon' in a)#False

#insert()
a.insert(1,'watermelon')
print(a)#['apple', 'watermelon', 'banana', 'banana', 'orange']

# join()
a= ['hello world', 'I am oxxo', 'how are you?']
b=','.join(a) # 使用逗號「,」進行結合
print(b)# hello world, I am oxxo, how are you?

# use *
a=['apple','banana']
b=a*3
print(b)#['apple', 'banana', 'apple', 'banana', 'apple', 'banana']
print(a)#['apple', 'banana']


