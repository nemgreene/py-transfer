word = "secret"

allowed_errors = 7
guesses = []
done = False

while not done:
    for letter in word:
        if letter.lower() in guesses:
            print(letter, end=" ")
        else:
            print("_ ")
    print("")

    guess=input("Allowed errors left {allowed_errors}, Next Guess: ")
    guesses.append(guess.lower())

    if guess.lower() not in word.lower():
        allowed_errors-=1
        if allowed_errors ==0:
            break

    done = True
    for letter in word:
        if letter.lower() not in guesses:
            done = False

if done:
    print("found word {word}")
else: 
    print("failed")