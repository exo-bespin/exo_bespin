if __name__ == '__main__':

    # Open up some input file
    with open('input.txt') as f:
        data = f.readlines()
    print(data)

    # Save some results
    my_favorite_foods = ['Cheese', 'Avocados', 'Asparagus', 'Other types of Cheese']
    with open('resuts.dat', 'w') as f:
        f.write(my_favorite_foods)