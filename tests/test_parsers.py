import unittest

import function.detail as detail_mod
import function.review as review_mod
import function.search as search_mod


class FakeResponse:
    status_code = 200
    url = 'https://example.invalid'

    def __init__(self, text):
        self.text = text


class ParserTests(unittest.TestCase):
    def test_search_parser(self):
        html = '''<div class="shop-list"><ul><li>
        <div class="pic"><a><img src="shop.jpg"/></a></div>
        <div class="txt"><div class="tit"><a data-shopid="shop-1" href="/shop/shop-1">测试店</a></div>
        <div class="comment"><span class="star_icon"><span class="unused star_45"></span></span>
        <a class="review-num">128条评论</a><a class="mean-price"><b>88</b></a></div>
        <div class="tag-addr"><span class="tag">火锅</span><span class="tag">测试区</span>
        <span class="addr">测试路1号</span></div></div>
        <div class="recommend">推荐菜A</div><div class="comment-list">口味9 环境8 服务9</div>
        </li></ul></div>'''
        original_get = search_mod.requests_util.get_requests
        original_map = search_mod.get_search_map_file
        original_replace = search_mod.requests_util.replace_search_html
        try:
            search_mod.requests_util.get_requests = lambda *args, **kwargs: FakeResponse(html)
            search_mod.get_search_map_file = lambda text: {}
            search_mod.requests_util.replace_search_html = lambda text, mapping: text
            result = search_mod.Search().search(
                'https://example.invalid', request_type='no proxy, no cookie'
            )
        finally:
            search_mod.requests_util.get_requests = original_get
            search_mod.get_search_map_file = original_map
            search_mod.requests_util.replace_search_html = original_replace

        self.assertEqual('shop-1', result[0]['店铺id'])
        self.assertEqual('测试店', result[0]['店铺名'])
        self.assertEqual('4.5', result[0]['店铺总分'])
        self.assertEqual('测试路1号', result[0]['店铺地址'])

    def test_detail_parser(self):
        html = '''<div class="main"><div id="basic-info"><h1 class="shop-name">测试店<a>手机扫码</a></h1>
        <div class="brief-info"><span id="reviewCount">128条评论</span>
        <span id="avgPriceTitle">人均88元</span></div><span itemprop="street-address">测试路1号</span>
        <p class="tel">010-12345678</p><div class="other">营业时间 10:00-22:00 修改</div>
        </div></div>'''
        original_get = detail_mod.requests_util.get_requests
        original_map = detail_mod.get_search_map_file
        original_replace = detail_mod.requests_util.replace_search_html
        try:
            detail_mod.requests_util.get_requests = lambda *args, **kwargs: FakeResponse(html)
            detail_mod.get_search_map_file = lambda text: {}
            detail_mod.requests_util.replace_search_html = lambda text, mapping: text
            result = detail_mod.Detail().get_detail(
                'shop-1', request_type='no proxy, no cookie'
            )
        finally:
            detail_mod.requests_util.get_requests = original_get
            detail_mod.get_search_map_file = original_map
            detail_mod.requests_util.replace_search_html = original_replace

        self.assertEqual('测试店', result['店铺名'])
        self.assertEqual('010-12345678', result['店铺电话'])
        self.assertEqual('测试路1号', result['店铺地址'])

    def test_review_parser(self):
        html = '''<div class="content"><span>全部 (10)</span><span>好评 (8)</span></div>
        <span class="filter-pic"><span class="count">(3)</span></span>
        <span class="filter-good"><span class="count">(8)</span></span>
        <span class="filter-middle"><span class="count">(1)</span></span>
        <span class="filter-bad"><span class="count">(1)</span></span>
        <div class="reviews-items"><div class="main-review"><a class="name" href="/member/user-1">测试用户</a>
        <span class="sml-rank-stars star50"></span><span class="score">口味：5 环境：4 服务：5 人均：88元</span>
        <div class="review-words">很好吃 收起评价</div><div class="review-recommend">喜欢的菜： 菜A 菜B</div>
        <span class="time">2026-08-26</span><div class="actions"><a data-id="review-1"></a></div>
        <div class="review-pictures"><a href="/photo/1"></a></div>
        <div class="shop-reply-content">谢谢光临</div></div></div>'''
        original_get = review_mod.requests_util.get_requests
        original_map = review_mod.get_review_map_file
        original_replace = review_mod.requests_util.replace_review_html
        try:
            review_mod.requests_util.get_requests = lambda *args, **kwargs: FakeResponse(html)
            review_mod.get_review_map_file = lambda text: {}
            review_mod.requests_util.replace_review_html = lambda text, mapping: text
            parser = review_mod.Review()
            parser.pages_needed = 1
            result = parser.get_review('shop-1', request_type='no proxy, no cookie')
        finally:
            review_mod.requests_util.get_requests = original_get
            review_mod.get_review_map_file = original_map
            review_mod.requests_util.replace_review_html = original_replace

        self.assertEqual(10, result['评论总数'])
        self.assertEqual('review-1', result['精选评论'][0]['评论id'])
        self.assertEqual('很好吃', result['精选评论'][0]['评论内容'])
        self.assertEqual(['https://www.dianping.com/photo/1'], result['精选评论'][0]['评论图片'])


if __name__ == '__main__':
    unittest.main()
