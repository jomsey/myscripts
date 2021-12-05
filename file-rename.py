import os
import clipboard

def file(f_path,pat):
    try:
        os.path.pathsep="\\"
        os.chdir(f_path)
        if os.path.isdir(f_path):
            print("\n====================================Files to rename=============================================\n")
            print()
            for dir in os.listdir(f_path): 
                if pat in dir.strip():
                    print("                          ",dir)
                    n_name = dir.replace(pat,"")
                    os.rename(dir,n_name)
        print()
        print(" DONE")
        
    except FileNotFoundError:
        print(f" {f_path} not found on system")

               
os.system("cls")
path = clipboard.paste()
print()
while True:
    print()
    pattern = input("  Enter pattern you wish to remove from file name => ")
    file(path,pattern)
    

    
