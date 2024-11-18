############################################################################################################
"""Fully commented file"""
############################################################################################################

#Skeleton Program code for the AQA A Level Paper 1 Summer 2025 examination
#this code should be used in conjunction with the Preliminary Material
#written by the AQA Programmer Team
#developed in the Python 3.9 programming environment

# Imports
import re
import random
import math

# Main Game function
def Main():
    NumbersAllowed = []    # Used as the list of nubmers given to make larger numbers.
    Targets = []
    MaxNumberOfTargets = 20
    MaxTarget = 0
    MaxNumber = 0        # Highest number a user can input
    TrainingGame = False
    Choice = input("Enter y to play the training game, anything else to play a random game: ").lower()    # Option to play training or not
    print()            # New line
    if Choice == "y":    # Training game
        MaxNumber = 1000
        MaxTarget = 1000
        TrainingGame = True
        Targets = [-1, -1, -1, -1, -1, 23, 9, 140, 82, 121, 34, 45, 68, 75, 34, 23, 119, 43, 23, 119]
    else:        # Normal game
        MaxNumber = 10
        MaxTarget = 50
        Targets = CreateTargets(MaxNumberOfTargets, MaxTarget)    # Create list of numbers for user to reach    
    NumbersAllowed = FillNumbers(NumbersAllowed, TrainingGame, MaxNumber)
    PlayGame(Targets, NumbersAllowed, TrainingGame, MaxTarget, MaxNumber)
    input()    # Keeps console window open

# Main control of the game
def PlayGame(Targets, NumbersAllowed, TrainingGame, MaxTarget, MaxNumber):
    Score = 0    # Starting score
    GameOver = False    
    while not GameOver:    # Start of game
        DisplayState(Targets, NumbersAllowed, Score)
        UserInput = input("Enter an expression: ")    # Input user's maths expression
        print()                                        # New line
        if CheckIfUserInputValid(UserInput):        # Check if characters input are allowed
            UserInputInRPN = ConvertToRPN(UserInput)
            if CheckNumbersUsedAreAllInNumbersAllowed(NumbersAllowed, UserInputInRPN, MaxNumber):
                IsTarget, Score = CheckIfUserInputEvaluationIsATarget(Targets, UserInputInRPN, Score)
                if IsTarget: # Target has been hit
                    NumbersAllowed = RemoveNumbersUsed(UserInput, MaxNumber, NumbersAllowed) # Remove used numbers from list of available
                    NumbersAllowed = FillNumbers(NumbersAllowed, TrainingGame, MaxNumber) # Add new number(s) to list of available
        Score -= 1    # Score decremented by 1
        if Targets[0] != -1: # If there is no target in the first item of the targets list
            GameOver = True # Game Over
        else:
            Targets = UpdateTargets(Targets, TrainingGame, MaxTarget) # Fill targets   
    print("Game over!")
    DisplayScore(Score)

def CheckIfUserInputEvaluationIsATarget(Targets, UserInputInRPN, Score):
    UserInputEvaluation = EvaluateRPN(UserInputInRPN) # Calculate RPN expression
    UserInputEvaluationIsATarget = False
    if UserInputEvaluation != -1: # If Evaluate RPN is not able to produce a valid integer
        for Count in range(0, len(Targets)): # Linear search
            if Targets[Count] == UserInputEvaluation: # If target is found
                Score += 2 # Increment score by 2
                Targets[Count] = -1 # Replace the target found with -1
                UserInputEvaluationIsATarget = True # A target has been hit
    return UserInputEvaluationIsATarget, Score
    
def RemoveNumbersUsed(UserInput, MaxNumber, NumbersAllowed):
    UserInputInRPN = ConvertToRPN(UserInput) # RPN expression
    for Item in UserInputInRPN: # Linear Search
        if CheckValidNumber(Item, MaxNumber): # If valid number below max
            if int(Item) in NumbersAllowed: # If numbers in RPN list are in Numbers Allowed
                NumbersAllowed.remove(int(Item)) # Number removed from the list of available
    return NumbersAllowed # List of available numbers returned

def UpdateTargets(Targets, TrainingGame, MaxTarget):
    for Count in range (0, len(Targets) - 1):
        Targets[Count] = Targets[Count + 1] # Shift target values left one position in the target list
    Targets.pop()
    if TrainingGame: # Training Game
        Targets.append(Targets[-1]) # Append the final item in the target list
    else: # Normal Game
        Targets.append(GetTarget(MaxTarget)) # Append a random target
    return Targets

def CheckNumbersUsedAreAllInNumbersAllowed(NumbersAllowed, UserInputInRPN, MaxNumber):
    Temp = []
    for Item in NumbersAllowed: Make a copy of the inputted NumbersAllowed list
        Temp.append(Item)
    for Item in UserInputInRPN:
        if CheckValidNumber(Item, MaxNumber): # Does not have an else statement to which returns False if a number is >MaxNumber
            if int(Item) in Temp: # Remove the item from the temp list after being used so it cannot be used again
                Temp.remove(int(Item)) # Remove the item from the list
            else:
                return False            
    return True

def CheckValidNumber(Item, MaxNumber):
    if re.search("^[0-9]+$", Item) is not None: # Number must only contain any digit 0 or higher in any combination at least once
        ItemAsInteger = int(Item) # Cast inputted number to an integer
        if ItemAsInteger > 0 and ItemAsInteger <= MaxNumber: # If Check if the number inputted is below the max number
            return True # Number valid
    return False # Number invalid
    
def DisplayState(Targets, NumbersAllowed, Score):
    DisplayTargets(Targets)
    DisplayNumbersAllowed(NumbersAllowed)
    DisplayScore(Score)    

# Outputs the user's current score
def DisplayScore(Score):
    print("Current score: " + str(Score))
    print()        # Blank line
    print()        # Blank line
    
def DisplayNumbersAllowed(NumbersAllowed):
    print("Numbers available: ", end = '')
    for N in NumbersAllowed:
        print(str(N) + "  ", end = '')
    print()        # Blank line
    print()        # Blank line
    
def DisplayTargets(Targets):
    print("|", end = '')
    for T in Targets:
        if T == -1:
            print(" ", end = '')
        else:
            print(T, end = '')           
        print("|", end = '')
    print()        # Blank line
    print()        # Blank line

def ConvertToRPN(UserInput): # Convert to Reverse Polish
    Position = 0
    Precedence = {"+": 2, "-": 2, "*": 4, "/": 4}    # Operator precedence dictionary BIDMAS
    Operators = []
    Operand, Position = GetNumberFromUserInput(UserInput, Position)
    UserInputInRPN = []
    UserInputInRPN.append(str(Operand))
    Operators.append(UserInput[Position - 1])
    while Position < len(UserInput): # Go through each postion
        Operand, Position = GetNumberFromUserInput(UserInput, Position) # Get inputted data from user
        UserInputInRPN.append(str(Operand))
        if Position < len(UserInput):
            CurrentOperator = UserInput[Position - 1] # Set the current operator to the inputted user  
            while len(Operators) > 0 and Precedence[Operators[-1]] > Precedence[CurrentOperator]: # Sorts out operator precedence
                # for example, if expression was "2+2/2", then: Operand = 2, Position = 2 --> UserInputInRPN = ['2'], Operators = ['+'] --> Operand = 2, Position = 4 --> UserInputInRPN = ['2','2'], CurrentOperator = '/' --> Operators = ['+', '/'] --> Operand = 2, Position = 5 --> UserInputInRPN = ['2','2','2'] --> Goes into bottom else statement, userInputInRPN = ['2','2','2','/'], Operators = ['+'] --> Still in Else statement, UserInputInRPN = ['2','2','2','/','+'], Operators = [] --> RETURNS UserInputInRPN since Operators is empty, and the postion(pointer) is at the end of the UserInputExpression 
                UserInputInRPN.append(Operators[-1])
                Operators.pop() # Remove the final operator on the operator list        
            if len(Operators) > 0 and Precedence[Operators[-1]] == Precedence[CurrentOperator]:
                UserInputInRPN.append(Operators[-1])
                Operators.pop() # Remove the final operator on the operator list  
            Operators.append(CurrentOperator)
        else:
            while len(Operators) > 0:
                UserInputInRPN.append(Operators[-1])
                Operators.pop()
    return UserInputInRPN

def EvaluateRPN(UserInputInRPN):
    S = [] # Temp proxy stack
    while len(UserInputInRPN) > 0: # While the UserInputInRPN is not empty
        while UserInputInRPN[0] not in ["+", "-", "*", "/"]: # While the first element is not an operator
            S.append(UserInputInRPN[0])
            UserInputInRPN.pop(0)        
        Num2 = float(S[-1]) # Set Num2 to the last element in the S list
        S.pop() # Remove the last element in the S list
        Num1 = float(S[-1]) # Set Num1 to the last element in the S list
        S.pop() # Remove the last element in the S list
        Result = 0.0
        if UserInputInRPN[0] == "+":
            Result = Num1 + Num2
        elif UserInputInRPN[0] == "-":
            Result = Num1 - Num2
        elif UserInputInRPN[0] == "*":
            Result = Num1 * Num2
        elif UserInputInRPN[0] == "/":
            Result = Num1 / Num2
        UserInputInRPN.pop(0)
        S.append(str(Result))       
    if float(S[0]) - math.floor(float(S[0])) == 0.0: # Check if it is an integer
        return math.floor(float(S[0])) # Floor rounds down to the nearest integer
    else:
        return -1

def GetNumberFromUserInput(UserInput, Position):
    Number = "" # Temp variable
    MoreDigits = True # Temp variable
    while MoreDigits:
        if not(re.search("[0-9]", str(UserInput[Position])) is None): # Number contrains digits 0-9
            Number += UserInput[Position]
        else:
            MoreDigits = False            
        Position += 1
        if Position == len(UserInput):
            MoreDigits = False
    if Number == "":
        return -1, Position
    else:
        return int(Number), Position    

def CheckIfUserInputValid(UserInput):
    if re.search("^([0-9]+[\\+\\-\\*\\/])+[0-9]+$", UserInput) is not None:
        # ^ Start of expression
        # [] A set of characters
        # 0-9 All digits 0 to 9
        # + One or more Occurrences
        # \\+\\-\\*\\/ plus or minus or asterisk or slash            \\+\\ exclude special function to just use as a character
        # $ End of expression
        return True    # Input valid
    else:
        return False    # Input not valid

def GetTarget(MaxTarget):
    """
    MaxTarget : Upper inclusive bound for random number
    """
    return random.randint(1, MaxTarget) # Random number x         1<= x <=MaxTarget
    
def GetNumber(MaxNumber):
    """
    MaxNumber : Upper inclusive bound for random number
    """
    return random.randint(1, MaxNumber) # Random number y         1<= y <=MaxNumber

# Create list of numbers for user to reach 
def CreateTargets(SizeOfTargets, MaxTarget):
    """
    SizeOfTargets : Number of targets
    MaxTarget : Highest value for a target
    """
    Targets = []        # Create empty local list
    for Count in range(1, 6):    # Loop 5 times
        Targets.append(-1)        # Append denary "-1" to the list
    for Count in range(1, SizeOfTargets - 4):    # SizeOfTargets 
        Targets.append(GetTarget(MaxTarget))
    return Targets
    
def FillNumbers(NumbersAllowed, TrainingGame, MaxNumber):
    if TrainingGame:    # Training game
        return [2, 3, 2, 8, 512]
    else:                # Normal Game
        while len(NumbersAllowed) < 5:    # Check if there are less than 5 elements in NumbersAllowed
            NumbersAllowed.append(GetNumber(MaxNumber))    # Insert into the list a random number  
        return NumbersAllowed

if __name__ == "__main__":
    Main()

# SCORING DOES NOT WORK - IF THERE ARE 2 OF THE SAME NUMBER, IT ADDS 3 TO YOUR SCORE INSTEAD OF 2, AND ADDS 5 IF YOU GET 3 AT SAME TIME
# FOLLOWS BIDMAS, BUT THERE IS NO BRACKETS?! SO YOU CAN'T DO (3+2)*5
# SPACES BETWEEN CHARACTERS ARE NOT ALLOWED
