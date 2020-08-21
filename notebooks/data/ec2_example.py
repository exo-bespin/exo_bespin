if __name__ == '__main__':

    # Open up some input file
    with open('input.txt') as f:
        data = f.readlines()
    print(data)

    # Save some results
    with open('results.dat', 'w') as f:
        f.write('These are my results!')