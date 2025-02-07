import os

def check_eula():
    eula_path = "./eula.txt"
    eula_text = "eula=true"
    
    if os.path.exists(eula_path):
        with open(eula_path, "r") as file:
            if eula_text in file.read():
                print("EULA already accepted.")
                return
    
    choice = input("Accept EULA? (Y/N): ").strip().lower()
    if choice == "y":
        with open(eula_path, "w") as file:
            file.write(eula_text + "\n")
        print("EULA accepted.")
    else:
        print("EULA not accepted. Exiting.")
        exit(1)

check_eula()
