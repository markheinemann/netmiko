

#initial comment

def inputNumber(message):
  while True:
    try:
       userInput = int(input(message))       
    except ValueError:
       print("Not an integer! Try again.")
       continue
    else:
       return userInput 
       break 
     
age = inputNumber("enter number please ?")



#guess=input("type any number : ")
#guess =int(guess)

guess = age

print (guess)


def collatz(number):
	while guess != 1:
		if number == 1:
			break
		elif number % 2 == 0:
			number = number // 2
			print(number)
		else:
			number = number *3 +1
			print(number)



collatz(guess)
# print result
print(" the final number is 1)")
