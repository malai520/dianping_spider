# -*- coding:utf-8 -*-

import argparse


def parse_bool(value):
    if isinstance(value, bool):
        return value
    normalized = value.strip().lower()
    if normalized in {'1', 'true', 'yes', 'y', 'on'}:
        return True
    if normalized in {'0', 'false', 'no', 'n', 'off'}:
        return False
    raise argparse.ArgumentTypeError('布尔值必须是 true/false、1/0、yes/no')


def build_parser():
    parser = argparse.ArgumentParser(description='大众点评搜索、详情与评论采集工具')
    parser.add_argument('--normal', type=int, choices=(0, 1), default=1,
                        help='完整流程：搜索 -> 可选详情/评论（默认 1）')
    parser.add_argument('--detail', type=int, choices=(0, 1), default=0,
                        help='只读取指定店铺详情')
    parser.add_argument('--review', type=int, choices=(0, 1), default=0,
                        help='只读取指定店铺评论')
    parser.add_argument('--shop_id', type=str, default='', help='详情/评论模式的店铺 ID')
    parser.add_argument('--need_more', nargs='?', const=True, default=False, type=parse_bool,
                        help='读取完整网页详情；可写 --need_more 或 --need_more true/false')
    return parser


def run(args):
    from utils.errors import DianpingSpiderError
    from utils.logger import logger
    from utils.spider_controller import controller

    selected_modes = args.normal + args.detail + args.review
    if selected_modes != 1:
        raise DianpingSpiderError('normal/detail/review 必须且只能启用一个模式')
    if (args.detail or args.review) and not args.shop_id.strip():
        raise DianpingSpiderError('详情或评论模式必须提供 --shop_id')

    if args.normal:
        controller.main()
    elif args.detail:
        logger.info('读取店铺 %s 详情', args.shop_id)
        controller.get_detail(args.shop_id, detail=args.need_more)
    else:
        logger.info('读取店铺 %s 评论', args.shop_id)
        controller.get_review(args.shop_id, detail=args.need_more)


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        run(args)
    except Exception as exc:
        from utils.errors import DianpingSpiderError
        if isinstance(exc, DianpingSpiderError):
            parser.exit(exc.exit_code, f'错误：{exc}\n')
        raise
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
