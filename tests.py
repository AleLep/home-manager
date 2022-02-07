import unittest
from datetime import datetime
import project1


class TestProject(unittest.TestCase):

    def test_date_diff(self):
        task_one = [{"id": 1, "title": 'clean', "date": (datetime.strptime('2022-02-08', '%Y-%m-%d')).date(),
                     "status": 'New', "weather": 'Y'}]
        result = project1.display_warning(task_one)
        self.assertEqual(result, 1)


if __name__ == '__main__':
    unittest.main()
