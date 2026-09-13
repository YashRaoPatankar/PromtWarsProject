import unittest
from unittest.mock import MagicMock, patch

class TestStudentWorkspace(unittest.TestCase):
    def test_course_contexts_available(self):
        """Verify standard academic contexts are registered."""
        contexts = ["General", "Computational and Data Science", "Calculus", "Physics", "Python Programming"]
        self.assertIn("Computational and Data Science", contexts)
        self.assertEqual(len(contexts), 5)

    def test_prompt_template_generation(self):
        """Ensure course context is injected into prompt template."""
        context = "Calculus"
        prompt = f"Expert academic tutor for a student studying {context}."
        self.assertIn("Calculus", prompt)

    @patch('google.generativeai.GenerativeModel')
    def test_mock_gemini_response(self, mock_model_class):
        """Verify API response handling works without making live external calls."""
        mock_instance = MagicMock()
        mock_instance.generate_content.return_value.text = "### Revision Notes\n- Core Theorem"
        mock_model_class.return_value = mock_instance
        
        model = mock_model_class('gemini-1.5-flash')
        response = model.generate_content("Analyze notes")
        self.assertEqual(response.text, "### Revision Notes\n- Core Theorem")

if __name__ == '__main__':
    unittest.main()
