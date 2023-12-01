import unittest
from classes import University, Country

class TestUniversity(unittest.TestCase):
    def setUp(self):
        self.university = University("DMACC", "Iowa", "Computer Science", '10000', '2')

    def tearDown(self):
        del self.university

    def test_university_name(self):
        self.assertEqual(self.university.name, "DMACC")

    def test_university_location(self):
        self.assertEqual(self.university.location, "Iowa")

    def test_univeristy_program(self):
        self.assertEqual(self.university.program, "Computer Science")
    
    def test_university_cost(self):
        self.assertEqual(self.university.cost, '10000')
    
    def test_university_duration(self):
        self.assertEqual(self.university.duration, '2')


class TestCountry(unittest.TestCase):
    def setUp(self):
        self.country = Country("United States of America", "USA")

    def tearDown(self):
        del self.country

    def test_country_name(self):
        self.assertEqual(self.country.name, "United States of America")

    def test_country_population(self):
        self.assertEqual(self.country.code, "USA")

if __name__ == '__main__':
    unittest.main()



