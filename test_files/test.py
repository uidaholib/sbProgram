from copy import copy, deepcopy
class Person(object):
    def __init__(self, name, height, car):
        self.name = name
        self.height = height
        self.car = car
        print("Person created.")

    def Print(self):
        print("""
        Here is {0}.
        He is {1} inches tall.
        He drives a {2}.
        """.format(self.name, self.height, self.car))

def main():
    print("Starting...")
    greg = Person("Greg", 70, "Mercedes")
    print("Greg at home:")
    greg.Print()

    greg_buys_a_car(greg)

    print("Greg at home:")
    greg.Print()

    greg_rents_a_gar(greg)

    print("Greg at home:")
    greg.Print()


    greg2 = clone_a_person(greg)
    print("Greg was the victim of a terrible accident at a lab he worked at.")
    print("Greg was cloned!")
    print("Greg 2.0 is way cooler than the original.")
    print("To prove it, Greg 2.0 built himself a spaceship.")
    greg2.car = "Spaceship"
    greg2.Print()


    print("Original Greg at home:")
    greg.Print()
    print("At least he still has his stolen Ferrari.")
    
    

def greg_buys_a_car(greg):
    print("Greg just bought a car and sold the old one!")
    print("Sadly, that car was a Ford. ")
    greg.car = "Ford"
    print("This downgrade made Greg shink in shame.")
    greg.height = 65
    print("Greg at the dealership:")
    greg.Print()
    return

def greg_rents_a_gar(greg):
    print("Greg rented a car on a business trip. It was a Ferrari. Super cool"
          + ", Greg.")
    x = greg
    x.car = "Ferarri"
    print("Greg on his business trip:")
    x.Print()
    print("Then Greg went home. He should give his Ferrari back...")
    return

def clone_a_person(greg):
    clone = deepcopy(greg)
    clone.name = greg.name + " 2.0"
    return clone


if __name__ == "__main__":
    main()
