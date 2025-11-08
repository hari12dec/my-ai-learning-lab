class ScenarioBased:
    
    # A system checks if a user is eligible to vote based on their age.
    # Write logic to ask the user for their age and determine if they are eligible to vote based on whether they are 18 or older.
    def voterEligibility():
        try:
            voterAge = int(input("Please enter your age:"))
            if voterAge <= 0:
                print("please enter valid age")
            elif voterAge >= 18:
                print("You are eligible to cast your vote")
            else:
                print("You are not eligible")
                print(f"You can vote after {18 - voterAge} years")
        except:
            print("Please enter only number")

    # A program processes a list of numbers and needs to find the largest value.
    # Write logic to identify and return the largest number from a given list.
    def findTheLargestNumber():
        inputNumbers = input("Please enter list of numbers with space:")
        numbersList = [int(num) for num in inputNumbers.split()]
        largestNumber = 0

        for numb in numbersList:
            if largestNumber < numb:
                largestNumber = numb

        return largestNumber

    # A company provides employees with a 10% bonus if their salary exceeds $50,000.
    # Write logic to determine the bonus amount based on the given salary.
    def detemineBonus(salary):
        if salary > 50000:
            bonusAmount = salary * 0.10
        else:
            print("Bonus not eligible")
            return

        print(f"Bonus amount: {bonusAmount}")


    # A program evaluates a number to determine if it is even or odd.
    # Write logic to check whether a given number is even or odd.
    def findOddorEvenNumber(givenNumber):
        if givenNumber % 2 == 0:
            print(f"{givenNumber} is even")
        else:
            print(f"{givenNumber} is odd")

    # A text-processing tool reverses a given word or sentence for formatting purposes.
    # Write logic to take a word or sentence as input and produce its reversed version.
    def textProcessReverse():
        inputText = input("Please enter your input:")
        # string[start:end:step]
        reversedText = inputText[::-1]
        print(reversedText)

    # A grading system determines whether a student has passed or failed based on their score.
    # Write logic to check if a student has passed a subject by scoring at least 40 marks.
    def checkStudentScoring():
        inputScore = int(input("Enter your score:"))
        if inputScore >= 40:
            print("Congratulations! You scored well")
        else:
            print("Better luck next time")

    # A retail store offers a 20% discount if a customer’s total order exceeds $100. 
    # Write logic to calculate the final amount to be paid after applying the discount.
    def offerCalculation(totalBilledAmount):
        if totalBilledAmount > 100:
            totalBilledAmount = totalBilledAmount - (totalBilledAmount * 0.2)
            return (True, totalBilledAmount)
        else:
            return (False, totalBilledAmount)
            
    # Scenario: A banking system processes withdrawal requests and ensures the user has enough balance.
    # Write logic to check if a user has enough balance before allowing a withdrawal and update the remaining balance accordingly.
    def bankingWithdrawalProcess():
        try:
            currentBalance = 14089
            print(f"Your Current Balance: ${currentBalance}")
            inputAmount = int(input("Please enter the withdrawal amount:"))
            if inputAmount <= currentBalance:
                print(f"Withdrawal successful! ₹{inputAmount} debited.")
                print(f"Your Balance after Withdrawal {currentBalance - inputAmount}")
            else:
                print("Insufficient balance! Transaction declined.")
        except ValueError:
            print("Please enter valid amount")
                            
    # Scenario: A calendar system verifies whether a given year is a leap year based on standard leap year rules.
    # Write logic to determine whether a given year is a leap year.
    def findLeapYear(year):
        print(f"Given year is {year}")
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            print("This is a leap year")
        else:
            print("This is not a leap year")
            
    # Scenario: A program filters out only even numbers from a given list.
    # Write logic to extract and return only the even numbers from a list.
    def filterEvenNumber():
        inputNumbers = input("Please enter list of numbers with space:")
        numbersList = [int(num) for num in inputNumbers.split()]
        newList = []
        
        for numb in numbersList:
            if numb % 2 == 0:
                newList.append(numb)

        return newList
                
        
                        



            