# import os

# for name in os.listdir("./parts/"):
#     # name = "ADV_POS.txt"
#     print(name)

#     file = open("./parts/" + name, "r")

#     with file as fp:
#         original = fp.read()
#         fp.seek(0,0)
#         for count, line in enumerate(fp):
#             pass
#         toPrepend = str(count + 1) + " " + str(300) + "\n"


#     file = open("./parts/" + name, "w")
#     file.write(toPrepend)
#     file.write(original)

# print("done.")

file = open("./commonMatrix.txt" , "r")

with file as fp:
    original = fp.read()
    fp.seek(0,0)
    for count, line in enumerate(fp):
        pass
    toPrepend = str(count + 1) + " " + str(300) + "\n"

file.close()

fileW = open("./commonMatrix.txt" , "w")
fileW.write(toPrepend)
fileW.write(original)
fileW.close()

print("done.")
