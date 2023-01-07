import os
import time

def run():
    print("toying with files")
    while True:
        time.sleep(1)
        files = ["{}".format(x) for x in range(20)]

        for file_name in files:
            file_path = "files/{}.txt".format(file_name)
            if os.path.exists(file_path):
                with open(file_path, "r") as file:
                    content = file.read()
                    # print(content)
            
            # delete file
            if os.path.exists(file_path):
                print("deleting {}".format(file_path))
                os.remove(file_path)

            with open(file_path, "w") as file:
                print("creating {}".format(file_path))
                file.write("wtmg {}".format(file_name))

            time.sleep(0.5)

if __name__ == "__main__":
    run()