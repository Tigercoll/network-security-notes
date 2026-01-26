#!/usr/bin/env python3
"""
Daily Document Enhancement CLI Tool
"""

from __future__ import annotations
import argparse
import sys
from pathlib import Path

# Add skills directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from skills.enhance_daily_document.skill import (
    DailyDocumentAnalyzer,
    DailyDocumentEnhancer,
    enhance,
    enhance_all,
    analyze
)


def main():
    parser = argparse.ArgumentParser(
        description="网络安全每日学习文档增强工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    # 分析单个文档
    python scripts/enhance_daily.py --analyze --day 050

    # 增强单个文档
    python scripts/enhance_daily.py --day 050

    # 增强所有文档
    python scripts/enhance_daily.py --all

    # 增强范围内的文档
    python scripts/enhance_daily.py --range 001 030
        """
    )
    
    parser.add_argument("--day", help="指定要增强的日期（001-090）")
    parser.add_argument("--all", action="store_true", help="增强所有每日文档")
    parser.add_argument("--range", nargs=2, metavar=("START", "END"), help="增强指定范围的文档")
    parser.add_argument("--analyze", action="store_true", help="仅分析文档完整性")
    parser.add_argument("--force", action="store_true", help="强制重新增强")
    parser.add_argument("--verbose", action="store_true", default=True, help="显示详细输出")
    parser.add_argument("--quiet", action="store_true", help="减少输出信息")
    
    args = parser.parse_args()
    
    if not (args.day or args.all or args.range):
        parser.print_help()
        print("\n错误：请指定 --day、--all 或 --range 参数")
        return 1
    
    if args.analyze:
        if args.day:
            result = analyze(args.day)
            print(f"\nDay{args.day} 分析结果:")
            print(f"   完整性评分: {result.get('completeness_score', 0):.1f}%")
            print(f"   缺失部分: {result.get('missing_sections', [])}")
        else:
            print("错误：分析模式需要指定 --day")
            return 1
    elif args.day:
        if not args.force:
            analyzer = DailyDocumentAnalyzer(args.day)
            if analyzer.load() and analyzer.get_completeness_score() >= 90:
                print(f"Day{args.day.zfill(3)} 已完整（{analyzer.get_completeness_score():.1f}%）")
                print("使用 --force 参数强制重新增强")
                return 0
        
        result = enhance(args.day, verbose=not args.quiet)
        if result.get("success"):
            print(f"\n增强完成: Day{args.day.zfill(3)}")
            return 0
        else:
            print(f"\n增强失败: {result.get('error', '未知错误')}")
            return 1
    elif args.all or args.range:
        start, end = ("001", "090") if args.all else args.range
        result = enhance_all(start, end, skip_existing=not args.force, verbose=not args.quiet)
        print(f"\n批量增强完成:")
        print(f"   总数: {result['total']}")
        print(f"   增强: {result['enhanced']}")
        print(f"   跳过: {result['skipped']}")
        print(f"   失败: {result['failed']}")
        return 0 if result['failed'] == 0 else 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
