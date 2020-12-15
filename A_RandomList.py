from random import randint, shuffle

def foo(length):
    list = []
    for i in range(1,length):
        list.append(i)
    shuffle(list)
    print(list)
    
    
