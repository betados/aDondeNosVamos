import os

def changePaths(name):
    cadenaS = 'dataBases'
    cadenaR = '/home/viajes/mysite/dataBases'
    out = open('temp.txt', 'w')
    with open(name) as f:
        lines = f.readlines()
        for line in lines:
            i = line.find(cadenaS)
            if i != -1:
                line = line[:i] + cadenaR + line[i+len(cadenaS):]
            out.write(line)
    out.close()
    f.close()
    os.remove(name)
    os.rename('temp.txt', name)


os.system("git checkout feature/autoConvert")
os.system("git merge develop")
changePaths('webApp.py')
os.system("git add .")
os.system('git commit --amend -m ""')

# os.system('git push origin rama')
