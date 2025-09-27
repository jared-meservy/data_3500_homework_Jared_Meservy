#3.4
for x in range(2):
    for y in range(7):
        print("@",end='')
    print()

#3.9
num=input("give me a 7-10 digit number: ")
for x in num:
    print (x)

#3.11
repeat= True
while repeat:
    gallon=int(input("Enter gallons used(-1 to end): "))
    if gallon == -1:
        break
    miles=int(input("Enter how many miles you drove: "))
    print("The miles/gallon of the tank was "str(miles/gallon))

#3.12
number=input("Give me a 5 digit number: ")
if number[0]== number[4]:
    print("Its a palindrome")
else:
    print("It is not a palindrome")

#3.14
#first time rounding to 3.14 152, 2nd 295. 3.141 295 

blank=False
pi=0
times=0
for x in range(1,1500,2):
    if pi==3.141:
        break
    if blank:
        pi -= 4 / x
        blank=False
        times+=1
    else:
        pi+=4/x
        blank =True
        times +=1
print(pi)
print(times)