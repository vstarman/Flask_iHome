a = [
    {"name": 'a', 'age': 15},
    {"name": 'b', 'age': 23},
    {"name": 'c', 'age': 14},
    {"name": 'd', 'age': 26},
]


def sort_list(list1):
    list2 = []
    for i in list1:
        list2.append(i['age'])
    list2.sort()

a.sort(key=lambda x:x['age'])
print sorted(a, key=lambda x:x['age'])
print a