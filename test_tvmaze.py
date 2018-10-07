# test_tv_maze

from unittest import TestCase
import tvmaze as tvm

__doc__ = """test_tv_maze"""
__version__ = "0.1"
__changelog__ = """

"""

if __name__ == '__main__':
    pass


class TestTvMaze(TestCase):
    TEST_SHOW_ID = 66  # Big bang theory
    TEST_EPISODE = 'The Bat Jar Conjecture'

    def setUp(self):
        self.show_unique = 'the big bang theory'
        self.show_multiple = 'girls'
        self.test_route = r'http://api.tvmaze.com/search/shows'

    def _check_episode_list(self, episodes):
        for episode in episodes:
            if episode['name'].lower() == TestTvMaze.TEST_EPISODE.lower():
                return True
        return False

    def _show_name_all_occurrenes(self, r, tosearch):
        for item in r:
            if not tosearch.lower() in item['show']['name'].lower():
                return False
        return True

    def _get_unique_show(self):
        r = tvm.get_shows(self.show_unique)
        r = tvm.get_show_by_id(r[0][0])
        return r

    def test_route_key_not_found(self):
        self.assertEqual(tvm._set_query('not_a_route_key'), None)

    def test_route_key_ok(self):
        self.assertEqual(tvm._set_query('search'), self.test_route,
                         f'Should be {self.test_route}')

    def test_get_data_none(self):
        not_a_show = "asdfsdfewet"
        self.assertEqual(tvm._get_data(self.test_route, not_a_show), None)

    def test_get_data_ok(self):
        r = tvm._get_data(self.test_route, {'q': self.show_unique})
        self.assertTrue(r is not None)

    def test_find_shows(self):
        r = tvm._get_data(self.test_route, {'q': self.show_multiple})
        self.assertTrue(len(r) > 1, "Return value should be a list of dicts")

    def test_find_shows_name_expected(self):
        r = tvm._get_data(self.test_route, {'q': self.show_multiple})
        self.assertTrue(self._show_name_all_occurrenes(r, self.show_multiple))

    def test_get_shows_ok(self):
        r = tvm.get_shows(self.show_multiple)
        print(r)
        self.assertTrue(len(r) > 1)

    def test_get_show_id_not_found(self):
        not_a_show = "asdfsdfewet"
        self.assertTrue(tvm.get_show_id(not_a_show), -1)

    def test_get_show_id_found(self):
        self.assertTrue(tvm.get_show_id(self.show_unique),
                        TestTvMaze.TEST_SHOW_ID)

    def test_get_show_by_id_ko(self):
        not_valid_id = '123123123123123123'
        r = tvm.get_show_by_id(not_valid_id)
        self.assertTrue(r is None)

    def test_get_show_by_id_ok(self):
        r = tvm.get_shows(self.show_unique)
        r = tvm.get_show_by_id(r[0][0])
        self.assertTrue(r['name'].lower() == 'the big bang theory')

    def test_get_show_image_medium_ok(self):
        r = tvm.get_show_image(TestTvMaze.TEST_SHOW_ID, tvm.ImgType.medium)
        self.assertTrue(r is not None)

    def test_get_show_status_not_a_show(self):
        not_valid_id = '123123123123123123'
        self.assertEqual(tvm.get_show_status(not_valid_id), None)

    def test_get_show_status_ok(self):
        self.assertTrue(
            tvm.get_show_status(TestTvMaze.TEST_SHOW_ID).lower()
            in ('ended', 'running'))

    def test_is_running_show_true(self):
        """Careful, ckeck if show_id is actually running, otherwise the test
        will fail"""
        # 66 = the big bang theory
        self.assertTrue(tvm.is_a_running_show(TestTvMaze.TEST_SHOW_ID))

    def test_is_running_show_false(self):
        # 1 = under the dome
        self.assertFalse(tvm.is_a_running_show(1))

    def test_get_show_and_episodes_all_seasons(self):
        show_id, show_name, episodes = tvm.get_show_and_episodes_short(
            TestTvMaze.TEST_SHOW_ID)
        self.assertTrue(self._check_episode_list(episodes))

    def test_get_show_and_episodes_filter_seasons(self):
        seasons = (1, 3, 6)
        show_id, show_name, episodes = tvm.get_show_and_episodes_short(
            TestTvMaze.TEST_SHOW_ID, seasons)

        self.assertTrue(all(eps['season'] for eps in episodes
                            if eps['season'] in seasons))

    def test_get_number_of_seasons(self):
        show_id = 1  # Under the Dome - 3 seasons - show ended
        self.assertEqual(tvm.get_number_of_seasons(show_id), 3, "Should be 3")


