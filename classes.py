class Country:
    def __init__(self, country_name, country_code):
        self.name = country_name
        self.code = country_code
        
    def __str__(self):
        return f"Country: {self.name}, Code: {self.code}"
    
    def __repr__(self):
        return self.name, self.code

class University(Country):
    def __init__(self, uni_name, location, program_name, cost, duration):
        self.name = uni_name
        self.location = location
        self.program = program_name
        self.cost = cost
        self.duration = duration
    
    def __str__(self):
        return f"University: {self.name}, Location: {self.location}, Program: {self.program}, Cost: {self.cost}, Duration: {self.duration}"
    
    def __repr__(self):
        return f"{self.name}, {self.location}, {self.program}, {self.cost}, {self.duration}"
    

    
    def __iter__(self):
        return iter([self.name, self.location, self.program, self.cost, self.duration])

    def run(list):
        for item in list:
            print(str(item))



    
