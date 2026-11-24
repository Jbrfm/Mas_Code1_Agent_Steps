import unittest

from basic_agent.tools import analyze_csv, analyze_text


class AnalysisToolsTest(unittest.TestCase):
    def test_persian_normalization_and_half_space(self):
        result = analyze_text("كتاب کتاب! می‌روم می‌روم؟", top_k=1)
        self.assertEqual(result["word_count"], 4)
        self.assertEqual(result["unique_word_count"], 2)
        self.assertEqual(result["sentence_count"], 2)
        self.assertEqual(result["top_words"], [{"word": "کتاب", "count": 2}])

    def test_empty_text_and_invalid_limit(self):
        self.assertEqual(analyze_text("")["word_count"], 0)
        self.assertEqual(analyze_text("...؟")["sentence_count"], 0)
        with self.assertRaises(ValueError):
            analyze_text("hello", top_k=0)
        with self.assertRaises(ValueError):
            analyze_text("a" * 100_001)

    def test_csv_statistics_missing_and_quoted_cells(self):
        result = analyze_csv('name,score,unused\n"Ali, A",18,\nSara,20,\nReza,,')
        self.assertEqual(result["row_count"], 3)
        self.assertEqual(result["columns"]["name"]["type"], "text")
        self.assertEqual(result["columns"]["score"], {
            "type": "numeric", "missing_count": 1,
            "min": 18, "max": 20, "mean": 19, "median": 19,
        })
        self.assertEqual(result["columns"]["unused"]["type"], "empty")

    def test_invalid_csv_and_nonfinite_numbers(self):
        for data in ["", "a,a\n1,2", "a,\n1,2", "a,b\n1", 'a\n"unclosed']:
            with self.subTest(data=data), self.assertRaises(ValueError):
                analyze_csv(data)
        self.assertEqual(analyze_csv("value\nNaN")["columns"]["value"]["type"], "text")
        self.assertEqual(analyze_csv("a,b")["row_count"], 0)


if __name__ == "__main__":
    unittest.main()
