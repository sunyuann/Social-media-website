'''test for echo to help further our understanding on how pytest works'''
import pytest
import echo
from error import InputError

def test_echo():
    '''
    test if function returns proper output if no InputError is raised
    '''
    assert echo.echo("1") == "1", "1 == 1"
    assert echo.echo("abc") == "abc", "abc == abc"
    assert echo.echo("trump") == "trump", "trump == trump"

def test_echo_except():
    '''
    test to check if pytest raises InputError when "echo" is entered (invalid input)
    '''
    with pytest.raises(InputError):
        assert echo.echo("echo")
