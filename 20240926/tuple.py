# 跟 list 一樣 是 有序的 但是 tuple 是不可變動的

a=('apple','banana','orange','grap')
b =('apple',)
type(a)# tuple
type(b)# tuple

t=('apple','banana','orange','grap')
a,b,c,d=t
print(a)# apple
print(b)# banana
print(c)# orange
print(d)# grap


t=('apple','banana','orange','grap')
print(t[0])# apple
print(t[1])# banana
print(t[2])# orange
print(t[3])# grap