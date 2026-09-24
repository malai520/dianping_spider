from urllib.parse import urlsplit


def safe_url(url):
    """Return a URL without query or fragment so tokens are not logged."""
    parts = urlsplit(url or '')
    if not parts.scheme and not parts.netloc:
        return parts.path or '-'
    return f'{parts.scheme}://{parts.netloc}{parts.path}'


class DianpingSpiderError(RuntimeError):
    exit_code = 1


class AuthenticationRequiredError(DianpingSpiderError):
    exit_code = 3

    def __init__(self, url):
        super().__init__(f'大众点评要求登录：{safe_url(url)}')


class VerificationRequiredError(DianpingSpiderError):
    exit_code = 4

    def __init__(self, url):
        super().__init__(f'大众点评要求人工验证：{safe_url(url)}')


class RequestFailedError(DianpingSpiderError):
    exit_code = 5
