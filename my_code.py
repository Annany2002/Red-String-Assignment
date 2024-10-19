def calculate_area(length, width):
    """Calculates the area of a rectangle."""
    area = length * width  
    return area

def main():
    length = 10
    width = 5
    area = calculate_area(length, width)
    print(f"The area is: {area}") 

if __name__ == "__main__":
    main()