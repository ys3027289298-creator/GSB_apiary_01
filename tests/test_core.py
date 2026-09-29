import unittest

import core


class TestCore(unittest.TestCase):
    def test_01_no_duplicate_hive(self):
        state = core.new_game()
        self.assertTrue(core.register_hive(state, "H1"))
        self.assertFalse(core.register_hive(state, "H1"))

    def test_02_no_harvest_off_bloom(self):
        state = core.new_game()
        state["season"] = "winter"
        result = core.harvest(state, "H1", 10)
        self.assertFalse(result)

    def test_03_honey_by_weight(self):
        state = core.new_game()
        state["honey"] = 30
        self.assertEqual(core.honey_by_weight(state), 30)

    def test_04_cancel_harvest_refunds(self):
        state = core.new_game()
        state["honey"] = 20
        core.cancel_harvest(state, "H1", 10)
        self.assertEqual(state["honey"], 10)

    def test_05_no_honey_without_queen(self):
        state = core.new_game()
        core.register_hive(state, "H1")
        state["hives"]["H1"]["queen"] = False
        result = core.count_honey(state, "H1")
        self.assertFalse(result)

    def test_06_disease_deducts_once(self):
        state = core.new_game()
        core.register_hive(state, "H1")
        state["hives"]["H1"]["population"] = 100
        core.disease(state)
        self.assertEqual(state["hives"]["H1"]["population"], 90)

    def test_07_no_work_in_bad_weather(self):
        state = core.new_game()
        state["weather"] = "storm"
        result = core.work(state)
        self.assertFalse(result)

    def test_08_load_preserves_batch(self):
        state = core.new_game()
        state["batch_id"] = 2
        loaded = core.load_state(core.save_state(state))
        self.assertEqual(loaded["batch_id"], 2)


if __name__ == "__main__":
    unittest.main()
