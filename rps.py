import csv
import os
import random

def titleMessage():
    print("Welcome to Rock, Paper, Scissors\n\n1. Start New Game\n2. Load Game\n3. Quit")

def titleOption(filePath):
    x = 0
    while x not in range(1, 4):
        try:
            x = int(input("\nEnter Choice: "))
            if x not in range(1, 4):
                print("Chosen number is not 1 - 3")
        except ValueError:
            print("Please enter a valid number (1, 2, or 3)")

    if x == 1:
        option = 1

    elif x == 2:
        option = 2

    elif x == 3:
        return 3

    return option

def newGame(filePath):
    player = input(str("\nWhat is your name? "))
    playerData = {}

    if os.path.isfile(filePath):
        with open(filePath, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                    if row and row[0] == player:
                        playerData['name'] = row[0]
                        playerData['wins'] = int(row[1])
                        playerData['losses'] = int(row[2])
                        playerData['ties'] = int(row[3])
                        print(f"Welcome back, {player}. Let's play!")
                        break

    if 'name' not in playerData:
        print(f"Hello {player}. Let's play!")
        playerData['name'] = player
        playerData['wins'] = 0
        playerData['losses'] = 0
        playerData['ties'] = 0

    return playerData

def loadGame(filePath):
    player = input(str("\nWhat is your name? "))
    playerData = {'name': player, 'wins': 0, 'losses': 0, 'ties': 0}

    if os.path.isfile(filePath):
        with open(filePath, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            player_found = False
            for row in csv_reader:
                if row and row[0] == player:
                    playerData['name'] = row[0]
                    playerData['wins'] = int(row[1])
                    playerData['losses'] = int(row[2])
                    playerData['ties'] = int(row[3])
                    print(f"Welcome back, {player}. Let's play!")
                    player_found = True
                    break

            if not player_found:
                print(f"{player}, your game could not be found.\n\n")
                main()
    else:
        print(f"{player}, your game could not be found.\n\n")
        main()

    return playerData

#I havent done anything like this before
#The sources online are recomending to write the file to an array basically then to read and alter there
#Then send back the array when I'm done
#This could get slow if the file is big but for now it will work
def saveData(filePath, playerData):
    existingData = []
    player_name = playerData['name']

    if os.path.isfile(filePath):
        with open(filePath, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            existingData = [row for row in csv_reader]

    player_name = playerData['name']
    data_found = False

    for index, row in enumerate(existingData):
        if row and row[0] == player_name:
            print(f"\nSaving player {player_name}...")
            existingData[index] = [player_name, playerData['wins'], playerData['losses'], playerData['ties']]
            data_found = True

    if not data_found:
        print(f"\nSaving new player {player_name}...")
        existingData.append([player_name, playerData['wins'], playerData['losses'], playerData['ties']])

    with open(filePath, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(existingData)
        print("Saved!")

def playGame(playerData):
    choices = ["Rock", "Paper", "Scissors"]
    
    print("1. Rock\n2. Paper\n3. Scissors")
    x = 0
    while x not in range(1, 4):
        try:
            x = int(input("\nEnter Choice: "))
            if x not in range(1, 4):
                print("Chosen number is not 1 - 3")
        except ValueError:
            print("Please enter a valid number (1, 2, or 3)")
    
    x -= 1

    computer_choice = random.randint(0, 2)
    
    print(f"\nYou chose {choices[x]}. The computer chose {choices[computer_choice]}.")

    if x == computer_choice:
        print("It's a tie!")
        playerData['ties'] += 1

    elif (x == 0 and computer_choice == 2) or (x == 1 and computer_choice == 0) or (x == 2 and computer_choice == 1):
        print("You win!")
        playerData['wins'] += 1

    else:
        print("The computer wins!")
        playerData['losses'] += 1

    return playerData

def postGame(playerData):
    continue_game = True

    while continue_game:
        print("\n1. Play Again\n2. View Statistics\n3. Quit")
        x = 0
        while x not in range(1, 4):
            try:
                x = int(input("\nEnter Choice: "))
                if x not in range(1, 4):
                    print("Chosen number is not 1 - 3")
            except ValueError:
                print("Please enter a valid number (1, 2, or 3)")

        if x == 1:
            continue_game = False
        elif x == 2:
            viewStatistics(playerData)
        elif x == 3:
            continue_game = False

    return x

def viewStatistics(playerData):
    player = playerData['name']
    print(f"\n{player}, here are your game play statistics...")
    print("Wins: " + str(playerData['wins']) + "\nLosses: " + str(playerData['losses']) + "\nTies: " + str(playerData['ties']))
    
    if playerData['losses'] > 0:
        print("\nWin/Loss Ratio: " + str(playerData['wins'] / playerData['losses']))

    else:
        print("\nWin/Loss Ratio: " + str(playerData['wins']) + " (You haven't lost any games yet)")


def main():
    filePath = 'rps.csv'
    titleMessage()
    option = titleOption(filePath)

    if option == 1:
        playerData = newGame(filePath)

    elif option == 2:
        playerData = loadGame(filePath)
        
    elif option == 3:
        return

    while True:
        player = playGame(playerData)
        saveData(filePath, player)
        x = postGame(playerData)

        if x == 3:
            return

    
main()
