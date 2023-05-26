students = int(input())
new_langs = set()
unique_langs = set()
polyglots = {}
for i in range(students):
    langs = int(input())
    if langs <= 500:
        for j in range(langs):
            new_langs.add(lan for lan in input() if len(lan) <= 1000)
        if len(unique_langs) == 0:
            unique_langs = new_langs.copy()
            for k in unique_langs:
                if k in polyglots:
                    polyglots[k] += 1
                else:
                    polyglots.update({k : 1})
        else:
            unique_langs &= new_langs
            for k in unique_langs:
                if k in polyglots:
                    polyglots[k] += 1
                else:
                    polyglots.update({k : 1})
    else:
        for j in range(0, 500):
            new_langs.add(lan for lan in input() if len(lan) <= 1000)
        if len(unique_langs) == 0:
            unique_langs = new_langs.copy()
            for k in unique_langs:
                if k in polyglots:
                    polyglots[k] += 1
                else:
                    polyglots.update({k : 1})
        else:
            unique_langs &= new_langs
            for k in unique_langs:
                if k in polyglots:
                    polyglots[k] += 1
                else:
                    polyglots.update({k : 1})
print(max(polyglots.values()))
print(unique_langs)
for i in unique_langs:
    print(i)


