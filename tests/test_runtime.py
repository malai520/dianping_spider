import csv
import os
import subprocess
import sys
import tempfile
import unittest
from types import SimpleNamespace

from main import parse_bool
from utils.errors import AuthenticationRequiredError, VerificationRequiredError
from utils.requests_utils import requests_util
from utils.saver.csv_saver import CSV
from utils.spider_config import spider_config


class RuntimeTests(unittest.TestCase):
    def test_safe_default_config(self):
        self.assertEqual('', spider_config.COOKIE)
        self.assertEqual('csv', spider_config.SAVE_MODE)
        self.assertEqual(1, spider_config.NEED_SEARCH_PAGES)
        self.assertFalse(spider_config.USE_PROXY)

    def test_parse_bool(self):
        self.assertTrue(parse_bool('true'))
        self.assertFalse(parse_bool('False'))

    def test_help_has_no_storage_dependency(self):
        result = subprocess.run(
            [sys.executable, 'main.py', '--help'],
            cwd=os.path.dirname(os.path.dirname(__file__)),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn('大众点评搜索、详情与评论采集工具', result.stdout)

    def test_login_and_verification_are_explicit_boundaries(self):
        with self.assertRaises(AuthenticationRequiredError):
            requests_util.handle_verify(
                SimpleNamespace(url='https://account.dianping.com/pclogin?token=secret'),
                'https://www.dianping.com/search',
                'proxy, no cookie',
            )
        with self.assertRaises(VerificationRequiredError):
            requests_util.handle_verify(
                SimpleNamespace(url='https://verify.meituan.com/v2/web/general_page?token=secret'),
                'https://www.dianping.com/search',
                'proxy, no cookie',
            )

    def test_csv_saver_serializes_nested_values(self):
        with tempfile.TemporaryDirectory() as output_dir:
            saver = CSV(output_dir)
            saver.save_data({
                '店铺id': 'shop-1',
                '店铺名': '测试店',
                '店铺均分': {'口味': '4.8'},
                '推荐菜': ['菜A', '菜B'],
            }, 'search')
            with open(os.path.join(output_dir, 'search_res.csv'), encoding='utf-8-sig') as csv_file:
                rows = list(csv.DictReader(csv_file))
        self.assertEqual('shop-1', rows[0]['店铺id'])
        self.assertEqual('{"口味":"4.8"}', rows[0]['店铺均分'])
        self.assertEqual('["菜A","菜B"]', rows[0]['推荐菜'])


if __name__ == '__main__':
    unittest.main()
