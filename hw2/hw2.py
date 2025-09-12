# 2.3
grade=91
if grade >= 90:
    print("Congrats! Your grade of "+str(grade)+" earns you an A")
#2.4
a =27.5
b =2
print("27.5 + 2 = "+ str(a + b))
print("27.5 - 2 = "+ str(a - b))
print("27.5 * 2 = "+ str(a * b))
print("27.5 / 2 = "+ str(a / b))
print("27.5 // 2 = "+ str(a // b))
print("27.5 ** 2 = "+ str(a ** b))
# 2.5
raduis = 2
print("The diameter of the circle is "+str(raduis*2))
print("The circumfrence of the cirlce is "+str(raduis*2*3.14159))
print("The area of the circle is "+str(3.14159*raduis**2 ))

#2.6
number = 5
if number % 2 ==1:
    print("this number is odd")
else:
    print("this number is even")

#2.7
if 1024 % 4==0:
    print("1024 is devisable by 4")
else:
    print("1024 is not devisable by 4")
if 10 % 2 ==0:
    print("10 is devisable by 2")
else:
    print("10 is not devisable by 2")

#2.8
print("number\tsquare\tcube")
for number in range(6):        
    square =number ** 2
    cube =number ** 3
    print(f"{number}\t{square}\t{cube}")