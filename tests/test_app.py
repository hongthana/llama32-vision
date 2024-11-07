import unittest
from llama32-vision.app import analyze_image

class TestApp(unittest.TestCase):

    def test_analyze_image_output_format(self):
        # Mock inputs
        image = None  # Replace with a mock or sample image if needed
        prompt = "Describe this image"

        # Call the function
        result = analyze_image(image, prompt)

        # Check if the result is a string
        self.assertIsInstance(result, str)

        # Check if the result contains markdown headers
        self.assertIn("# Image Analysis", result)

        # Check if the result contains markdown bullet points
        self.assertIn("- ", result)

    # Add more tests as needed to cover other functionalities

if __name__ == '__main__':
    unittest.main()