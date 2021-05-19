print("\nWelcome to Our Recommendation Engine!\n")

userlist=['A0','A1','A2']

valid=False
while valid == False:
    user = input("Please enter your user name: ")
    if user not in userlist:
        print("User not found. Please try again.")
    if user in userlist:
        print("Login Successful. Welcome back " + user + "!")
        valid=True
