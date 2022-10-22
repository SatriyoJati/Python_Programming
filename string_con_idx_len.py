message = "python"

price = "$1100"
print(message + " "  + price )
print(id(message)) # refer to first var message
#string concatination
message = message + "test"
print(id(message)) #refer to second var message

print("String indexing")
name = "Interstellar"
#index 0
print("first char")
print(name[0])

#index last
print("last char")
print(name[-1])

#slicing
print("Slicing")
#start index - stop + 1
print(name[5:7])

#if not specified after : then until end
print(name[6:])

#id not specified all then all
print(name[:])

#using step : [start : stop + 1 : ]
print(name[2:6:2])

print("Reversing:\n")
print(name[::-1])
