from lib import image_io

def test_load_save():
    img = image_io.load_image('./data/input.jpg', gray=True)
    image_io.save_image(img, './data/output_test.jpg')
    print("Test passed")

if __name__ == "__main__":
    test_load_save()