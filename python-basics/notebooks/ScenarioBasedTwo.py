class ScenarioBased:
    # You are developing a banking application that categorizes transactions based on the amount entered.
    # Write logic to determine whether the amount is positive, negative, or zero.
    def categorizeTransaction():
        try:
            amount = float(input("Enter transaction amount: "))
        
            if amount > 0:
                print("The transaction is positive.")
            elif amount < 0:
                print("The transaction is negative.")
            else:
                print("The transaction amount is zero.")
            
        except ValueError:
            print("Please enter a valid number.")

    # A digital locker requires users to enter a numerical passcode. As part of a security feature, the system checks the sum of the digits of the passcode.
    # Write logic to compute the sum of the digits of a given number.
    def sumOfDigits():
        try:
            num = int(input("Enter the passcode: "))
        
            digits = [int(d) for d in str(abs(num))]
            total = sum(digits)
        
            print("Digits:", digits)
            print("Sum of digits:", total)
        
        except ValueError:
            print("Please enter a valid number.")

    # A mobile payment app uses a simple checksum validation where reversing a transaction ID helps detect fraud.
    # Write logic to take a number and return its reverse.
    def simpleChecksum(inputNum):
        if len(str(abs(inputNum))) < 4:
            print("Invalid transId")
            return
        strNumber = str(inputNum)
        strNumber = strNumber[::-1]
        print(strNumber)

    # In a secure login system, certain features are enabled only for users with prime-numbered user IDs.
    # Write logic to check if a given number is prime.
    def findPrimeNumberUserIds():
        num = int(input("Enter your userId: "))
            
        if len(str(abs(num))) < 5:
            for i in range(2, int(num ** 0.5) + 1):
                if num % i == 0:
                    print("Success! Valid UserId")
                    break
                else:
                    print("Not Valid UserId, please check")
        else:
            print("Please enter valid user id")

    # A scientist is working on permutations and needs to calculate the factorial of numbers frequently.
    # Write logic to find the factorial of a given number using recursion.
    def findFactorial(number):
        if number < 0:
            return "Factorial not defined for negative numbers"
            
        result = 1
        
        for i in range(1, n+1):
            result *= i
            
        return result

    # A unique lottery system assigns ticket numbers where only Armstrong numbers win the jackpot.
    # Write logic to check whether a given number is an Armstrong number.
    def findArmstrong():
        try:
            num = int(input("Enter a number: "))
            digits = len(str(abs(num))) 
            total = 0
            temp = abs(num)
        
            while temp > 0:
                digit = temp % 10
                total += digit ** digits
                temp = temp // 10
        
            if total == num:
                print(f"{num} is Armstrong")
            else:
                print(f"{num} is NOT Armstrong")
            
        except ValueError:
            print("Please enter a valid integer.")  

    # A password manager needs to strengthen weak passwords by swapping the first and last characters of user-generated passwords.
    # Write logic to perform this operation on a given string.
    def swappingPassword():
        password = input("Please enter your password: ")
        swapped = password[-1] + password[1:-1] + password[0]
        return swapped

    # A low-level networking application requires decimal numbers to be converted into binary format before transmission.
    # Write logic to convert a given decimal number into its binary equivalent.
    def decimalToBinary():
        try:
            num = int(input("Enter a decimal number: "))
        
            binaryDigits = []
            n = num
            while n > 0:
                remainder = n % 2
                binaryDigits.append(str(remainder))
                n = n // 2
        
            binaryDigits.reverse()
            binary = "".join(binary_digits)
            print(f"Decimal: {num} → Binary: {binary}")
        
        except ValueError:
            print("Please enter a valid integer.")

    # A text-processing tool helps summarize articles by identifying the most significant words.
    # Write logic to find the longest word in a sentence.
    def findLongestWord(sentence):
        wordLength = 0
        longestWord = ""
        wordList = sentence.split(" ")

        for word in wordList:
            wordLen = len(word)
            if wordLength < wordLen:
                wordLength = wordLen
                longestWord = word

        return (longestWord, wordLength)

    # A plagiarism detection tool compares words from different documents and checks if they are anagrams (same characters but different order).
    # Write logic to check whether two given strings are anagrams.
    def checkAnagram(str1, str2):
        str1 = "".join(sorted(str1))
        str2 = "".join(sorted(str2))
        if str1 == str2:
            print("Given strings are Anagrams")
        else:
            print("Given strings are NOT Anagrams")




    
