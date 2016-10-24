import unittest
import tvmaze


class MyTestCase(unittest.TestCase):
    def test_singlesearch_show_not_found(self):
        result = tvmaze.single_search("a non existent show")
        self.assertIsNone(result, "Should be none, got %s" % type(result))

    def test_singlesearch_show_found(self):
        result = tvmaze.single_search("walking dead")
        self.assertIsNotNone(result, "Exptected some show infos")

    def test_get_show_id_not_found(self):
        result = tvmaze.get_show_id("a non existent show")
        self.assertEqual(result, -1, "Should be -1")

    def test_get_show_id_found(self):
        result = tvmaze.get_show_id("walking dead")
        self.assertEqual(result, 73, "Expected 73")

    def test_get_episodes_show_id_not_found(self):
        result = tvmaze.get_episodes(tvmaze.get_show_id("a non existent show"))
        self.assertEqual(len(result), 0, "Should be 0 (an empty list)")

    def test_get_episodes_show_id_found(self):
        result = tvmaze.get_episodes(tvmaze.get_show_id("walking dead"))
        self.assertGreater(len(result), 0, "Expected a populated list")

    def test_get_episodes_show_id_found_selected_seasons(self):
        result = tvmaze.get_episodes(tvmaze.get_show_id("walking dead"), (2,))
        test = 2
        for ep in result:
            if ep['season'] != 2:
                test = ep['season']
                break
        self.assertEqual(test, 2, "Expected season 2 only")

    def test_get_number_of_seasons(self):
        result = tvmaze.get_episodes(tvmaze.get_show_id("buffy"))
        self.assertGreaterEqual(
            tvmaze.get_total_seasons(tvmaze.get_show_id("buffy")), 7,
                "The Buffy show has 7 seasons"
            )


if __name__ == '__main__':
    unittest.main()