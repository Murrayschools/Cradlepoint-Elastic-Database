from cradlepoint import PageParser

def test_page_parser_urls():
    x = PageParser("cradlep", variables={"doc": "nope", "chad": "yep"}, fields=["rssi", "signal_strength"])
    assert x.url == "https://www.cradlepointecm.com/api/v2/cradlep/?doc=nope&chad=yep&fields=rssi,signal_strength", "Url is not correct"
