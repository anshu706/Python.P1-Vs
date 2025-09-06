print("Welcome to my computer quiz!")

playing = input("Do you want to play? ")

if playing != "yes":
    quit()

print("Okay! Let's play :)")
score = 0

answer = input("What does CPU stands for? ")
if answer == "Central Processing Unit":
    print('Correct!')
    score += 1
else:
    print("Incorrect!")

answer = input("What does a GPU stands for? ")
if answer == "Graphics Processing Unit":
    print('Correct!')
    score += 1
else:
    print("Incorrect!")

answer = input("What does RAM stands for? ")
if answer == "Random Access Memory":
    print('Correct!')
    score += 1
else:
    print("Incorrect!")

answer = input("What does PSU stands for? ")
if answer == "Power Supply Unit":
    print('Correct!')
    score += 1
else:
    print("Incorrect!")

print("You got " + str(score) + " questions correct!")
print("You got " + str((score/4) * 100) + "%.")
