class MultipleFunctions:
    def SubfieldsInAI():
        aiSubFields = ["Machine Learning", "Neural Networks", "Vision", "Robotics", "Speech Processing", "Natural Language Processing"]
        print("Sub-fields in AI are:")
        for subField in aiSubFields:
            print(subField)
            
    def findOddorEven():
        num1 = int(input("Enter a number:"))
        if num1 % 2 == 0:
            output = f"{num1} is Even number"
        else:
            output = f"{num1} is Odd number"
        return output
    
    def marriageEligibilityCheck(gender, age):
        print(f"Your Gender: {gender}")
        print(f"Your age: {age}")
    
        if gender.lower() == "male" and age >= 21 or gender.lower() == "female" and age >= 18:
            output = "ELIGIBLE"
        else:
            output = "NOT ELIGIBLE"
        print(output)
        
    def findPercentage():
        Subject1 = int(input("Subject1="))
        Subject2 = int(input("Subject2="))
        Subject3 = int(input("Subject3="))
        Subject4 = int(input("Subject4="))
        Subject5 = int(input("Subject5="))
    
        listOfSubject = [Subject1, Subject2, Subject3, Subject4, Subject5]
        total = sum(listOfSubject)
        percentage = total/len(listOfSubject)
        return total, percentage
         
    def findAreaOfTriangle(height, breadth):
        print(f"Height:{height}")
        print(f"Breadth:{breadth}")
        print("Area formula: (Height*Breadth)/2")
        area = (height * breadth) / 2
        print(f"Area of Triangle: {area}")
        return
        
    def findPerimeterOfTriangle(height, anotherheight, breadth):
        print(f"Height1:{height}")
        print(f"Height2:{anotherheight}")
        print(f"Breadth:{breadth}")
        print("Perimeter formula: Height1+Height2+Breadth")
        perimeter = height + anotherheight + breadth
        print(f"Perimeter of Triangle: {perimeter}")
        return