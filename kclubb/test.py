<<<<<<< HEAD
import math


math.cos()

class car:
    def func1():
        pass

var1 = car()

var2 = 'hello'



=======
#Exercise 1

amt = 100
def calc_tax(amount):
    rate = 0.1
    tax = amount * rate
    print("Tax:", tax)
calc_tax(amt)

#Exercise 2
months = 12
temperature = 36.6
message = 'Hello'
colors = ["blue","orange","green"]
#print(colors)
book = {'title':'John Wayne',  'author':'Lisa McEntire',  'year': 1998}
#print(book)

# Exercise 3 
#total_cost, 3d_model, email_address

#Exercise 4
length_str ="15"
width_str = "8.4"

length_int = int(length_str)
width_flt = float(width_str)
tri_area = length_int * width_flt
#print(tri_area)

#Exercise 5
allowed_users = ['alice', 'bob','charlie']

email = 'bob@example.com'

info = {'email': 'bob@example.com', 'age': 25, 'member': True}

print("bob" in allowed_users)
print('@' in email)
print("age" in info)
print("False" in info)

#Exercise 6
data = [10,20,30,40,50,60]
s = "abcdefg"

print(data[:3])
print(data[-2:])
print(data[::2])
print(s[2:5])
print(s[::-1])

#Exercise 7
temp_c = 25

if temp_c <0:
    print("Frozen(ice)")
elif temp_c > 100:
    print("Gas(steam)")
else: 
    print("Liquid water")

#Exercise 8
num_list = [3, 7, 1, 12, 9]
new_total = 0
for n in num_list:
   new_total += n
print(new_total)

#Exercise 9

counter = 1

while counter <= 5:
    print(counter)
    counter += 1
    
print('Loop Finished!!')


#Exercise 10

def square(num_to_square:int|float) -> int|float:
    if type(num_to_square)!= float and type(num_to_square) != int:
        print("The function parameter must be a float!")
         
    return num_to_square ** 2


print(square(3.2))
>>>>>>> fd6cd7f (first file)
