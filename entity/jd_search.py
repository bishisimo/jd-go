"""
 @author: bishisimo
 @time: 2020-12-22 17:32
 """


class JdSearch:
    def __init__(self, key, min_price, max_price=None, brand=""):
        self.key = key
        self.min_price = min_price
        if max_price is not None:
            self.max_price = max_price
        else:
            self.max_price = min_price
        self.search_url = f"https://search.jd.com/search?keyword={key}&qrst=1&wq={key}&shop=1&ev=exbrand_{brand}%5Eexprice_{min_price}-{max_price}%5E"


if __name__ == '__main__':
    pass
