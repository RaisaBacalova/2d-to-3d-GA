import unittest
import imgPreprocessing

class ImagePreprocessingTest (unittest.TestCase):
    def testClassExists(self):
        gray = imgPreprocessing.ImagePreprocessing.imgToGrayscale()
        edges = imgPreprocessing.ImagePreprocessing.edgeDetection()
        self.assertIsNotNone(gray,edges)

    unittest.main()