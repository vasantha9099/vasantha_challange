import re

n = int(input())
pattern = r'^[4-6]\d{3}(-?\d{4}){3}$'


for _ in range(n):
    string = input()
    replace_String = string.replace("-", "")
    consecutive = re.search(r'(\d)\1{3}', replace_String)
    matches = re.search(pattern,string)
    if matches and len(replace_String) == 16 and not consecutive:
        print('Valid')
    else:
        print('Invalid')
