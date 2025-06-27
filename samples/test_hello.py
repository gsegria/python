from hello import say_hello

def test_say_hello():
    assert say_hello("Ping") == "Hello, Ping!"
    assert say_hello("VS Code") == "Hello, VS Code!"