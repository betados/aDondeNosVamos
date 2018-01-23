import os

def changePaths():
    pass

os.system("git checkout feature/autoConvert")
os.system("git merge develop")
changePaths()
os.system("git add .")
os.system('git commit --amend -m ""')
