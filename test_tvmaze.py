import unittest
import tvmaze


class MyTestCase(unittest.TestCase):
    def test_search_show_not_found(self):
        result = tvmaze.find_shows("a non existent show")
        self.assertEqual(len(result), 0,  "Should be an empty list!")

    def test_search_show_found(self):
        result = tvmaze.find_shows("girls")
        self.assertIsNotNone(result, "Exptected a populated list")

    def test_singlesearch_show_not_found(self):
        result = tvmaze.single_search("a non existent show")
        self.assertIsNone(result, "Should be none, got %s" % type(result))

    def test_singlesearch_show_found(self):
        result = tvmaze.single_search("walking dead")
        self.assertIsNotNone(result, "Exptected some show infos")

    def test_get_show_by_id_found(self):
        result = tvmaze.get_show(73)
        self.assertTrue('walking dead' in result['name'].lower(),
                        "The walking dead show should be found")

    def test_get_show_by_id_not_found(self):
        result = tvmaze.get_show(7121454543)
        self.assertIsNone(result, "Should be None")

    def test_get_show_id_not_found(self):
        result = tvmaze.get_show_id("a non existent show")
        self.assertEqual(result, -1, "Should be -1")

    def test_get_show_id_found(self):
        result = tvmaze.get_show_id("walking dead")
        self.assertEqual(result, 73, "Expected 73")

    def test_get_show_and_episodes_short_show_id_not_found(self):
        show_id, show_name, episodes = tvmaze.get_show_and_episodes_short(
            tvmaze.get_show_id("a non existent show")
        )
        self.assertIsNone(show_name, "If show not found should be None")
        self.assertEqual(len(episodes), 0, "Should be an empty list")

    def test_get_show_and_episodes_short_show_id_found(self):
        show_id, show_name, episodes = tvmaze.get_show_and_episodes_short(
            tvmaze.get_show_id("walking dead")
        )
        self.assertTrue('walking dead' in show_name.lower())
        self.assertGreater(len(episodes), 0, "Expected a populated list")

    def test_get_episodes_show_id_found_selected_seasons(self):
        show_id, show_name, episodes = tvmaze.get_show_and_episodes_short(
            tvmaze.get_show_id("walking dead"), (2,)
        )
        test = 2
        for ep in episodes:
            if ep['season'] != 2:
                test = ep['season']
                break
        self.assertEqual(test, 2, "Expected season 2 only")

    def test_get_number_of_seasons(self):
        self.assertGreaterEqual(
            tvmaze.get_seasons_number(tvmaze.get_show_id("buffy")), 7,
                "The Buffy show has 7 seasons"
            )

    def test_get_shows_found_something(self):
        result = tvmaze.get_shows("girls")
        self.assertGreater(result, 0, "Expected a populated list!")

    def test_get_shows_found_nothing(self):
        result = tvmaze.get_shows("nonexistent")
        self.assertEqual(len(result), 0, "Expected a populated list!")


if __name__ == '__main__':
    unittest.main()
