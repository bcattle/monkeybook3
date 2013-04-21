from unittest import TestCase
from monkeybook.data_connnectors.results import ResultsCollection


class BondGirl1:
    id = 1
    name = 'Natalya Simonova'
    location = 'Moscow'

class BondGirl2:
    id = 2
    name = 'Miss Moneypenny'
    location = 'London'

class BondGirl3:
    id = 3
    name = 'Honey Ryder'
    location = 'London'


class ResultsCollectionTestCase(TestCase):
    def test_get_by_field_empty(self):
        results = ResultsCollection()
        # No items
        self.assertRaises(IndexError, results.get_by_field, 'name', 'Natalya Simonova')

    def test_get_by_field_single(self):
        results = ResultsCollection()
        results.append(BondGirl1())
        results.append(BondGirl2())
        results.append(BondGirl3())
        # Get by name
        honey = results.get_by_field('name', 'Honey Ryder')
        self.assertEqual(len(honey), 1)
        self.assertEqual(honey[0].name, 'Honey Ryder')

    def test_get_by_field_multiple(self):
        results = ResultsCollection()
        results.append(BondGirl1())
        results.append(BondGirl2())
        results.append(BondGirl3())
        # Get by location
        london = results.get_by_field('location', 'London')
        self.assertEqual(len(london), 2)

