students = int(input())
unique_langs = set()
for i in range(int(input())):
    unique_langs.update(x for x in input().split())
for i in range(students - 1):
    new_langs = set()
    langs = int(input())
    for j in range(langs):
        new_langs.update(x for x in input().split())
    unique_langs &= new_langs
print(len(unique_langs))
print(*sorted(unique_langs), sep='\n')