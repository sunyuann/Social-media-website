'''requests is imported to obtain data from flask server'''
import json
import requests
import pytest

@pytest.mark.usefixtures("url")
def test_echo(url):
    '''
    A simple test to check echo
    '''
    resp = requests.get(url + 'echo', params={'data': 'hello'})
    assert json.loads(resp.text) == {'data': 'hello'}
