# 跟 cpp 的 map 一樣 key-value pair 
# 但是 python 的 dict 可以用任何 hashable 的東西當 key 
# 且不用 include

# 創建 dict
d = {}
d = dict()
d = {'apple': 1, 'banana': 2}
print(d)

# 取值
print(d['apple'])
print(d.get('apple'))

# 修改
d['apple'] = 3

# 新增
d['orange'] = 4

# 刪除
del d['apple']

# 檢查 key 是否存在
print('apple' in d)

# 取得所有 key
print(d.keys())

# 取得所有 value
print(d.values())

# 取得所有 key-value pair
print(d.items())

# 取得所有 key-value pair
for key, value in d.items():
    print(key, value)

# 清空
d.clear()

# 刪除
del d

# copy
d = {'apple': 1, 'banana': 2}

d2 = d.copy()
d3 = dict(d)
d4 = d

# dict method
d = {'apple': 1, 'banana': 2}
print(d.get('apple'))  # 1
print(d.get('orange'))  # None
print(d.get('orange', 0))  # 0
print(d.setdefault('apple', 3))  # 1
print(d.setdefault('orange', 4))  # 4
print(d)  # {'apple': 1, 'banana': 2, 'orange': 4}
print(d.pop('apple'))  # 1
print(d.pop('orange', 0))  # 4
print(d)  # {'banana': 2}
print(d.popitem())  # ('banana', 2)
print(d)  # {}
d = {'apple': 1, 'banana': 2}
d.update({'apple': 3, 'orange': 4})

# dict comprehension
d = {i: i * i for i in range(10)}
print(d)
d = {i: i * i for i in range(10) if i % 2 == 0}
print(d)
d = {i: i * i for i in range(10)}
print(d)
d = {i: i * i for i in range(10)}
print(d)
