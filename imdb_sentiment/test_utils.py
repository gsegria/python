from utils import clean_text

def test_clean_text():
    text = "<b>Hello!!!</b> This is a TEST 123."
    cleaned = clean_text(text)
    assert cleaned == "hello this is a test"
