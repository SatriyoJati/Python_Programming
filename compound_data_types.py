my_list = [15, 6 , 7, 8, 35, 12, 14, 4, 10]
my_string_list = ["comp sci", "physics", "elec eng", "philosophy"]
print(f"Ints : {my_list}")
print(f"Strings: {my_string_list}")

print("Sorting...")
print(f"Sorted Ints L {my_list}")
print(sorted(my_list)) #print new list

'''this is shorted my list in place'''
print(my_list.sort())

#to check you can use id()
print(dir(my_list))
