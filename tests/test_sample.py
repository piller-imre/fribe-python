import unittest

from fribe.loader import load_engine_from_string


class SampleTest(unittest.TestCase):
    """Test the sample behavior definition"""

    def test_two_input_dimensions(self):
        behavior_description = """
        universe "x"
            "low" 0 0
            "high" 1 1
        end

        universe "y"
            "low" 0 0
            "high" 1 1
        end

        universe "z"
            "low" 0 0
            "high" 1 1
        end

        rulebase "z"
            rule "high" when "x" is "high" and "y" is "high" end
            rule "low" when "x" is "low" end
            rule "low" when "y" is "low" end
        end
        """
        engine = load_engine_from_string(behavior_description)
        samples = [
            {'x': 0, 'y': 0, 'z': 0},
            {'x': 0, 'y': 1, 'z': 0},
            {'x': 1, 'y': 0, 'z': 0},
            {'x': 1, 'y': 1, 'z': 1},
            {'x': 0.5, 'y': 0.5, 'z': 1 / 3}
        ]
        for sample in samples:
            engine.calc_consequences({'x': sample['x'], 'y': sample['y']})
            z = engine.get_state('z')
            self.assertEqual(sample['z'], z)
