# try:
#     file= open("a_file.txt")
#     a_dictionary={"key":"value"}
#     print(a_dictionary["hfhfd"])
# except FileNotFoundError:
#     file=open("a_file.txt", "w")
#     file.write("something"
#                )
# except KeyError as error_message:
#     print("that key does not exist")
# else:
#     content=file.read()
#     print(content)
#
# finally:
#     raise TypeError
#

height=float(input("HEight: "))

weight= int(input("Weight: "))

if height >3:
      raise ValueError("human height should not be over 3 meters")

bm1= weight/ height**2
print(bm1)