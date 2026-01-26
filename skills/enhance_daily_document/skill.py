from __future__ import annotations
import re
from pathlib import Path
from typing import Dict, List

ROOT_DIR = Path(__file__).resolve().parents[2]
DAILY_DIR = ROOT_DIR / 'daily'

REQUIRED_SECTIONS = ['学习目标', '学习内容', '实践任务（合法授权范围内）', '巩固练习（题与复盘）', '评估标准（达成判定）', '学习成果达成情况（由学习者填写）']

class DailyDocumentAnalyzer:
    def __init__(self, day_number: str):
        self.day_number = str(day_number).zfill(3)
        self.filepath = DAILY_DIR / f'Day{self.day_number}.md'
        self.content = ''
        self.sections: Dict[str, str] = {}
        
    def load(self) -> bool:
        if not self.filepath.exists():
            return False
        self.content = self.filepath.read_text(encoding='utf-8')
        self._parse_sections()
        return True
    
    def _parse_sections(self) -> None:
        lines = self.content.split('\n')
        current_section = None
        current_content = []
        for line in lines:
            section_match = re.match(r'^#+\s+(.+)', line)
            if section_match:
                if current_section:
                    self.sections[current_section] = '\n'.join(current_content)
                current_section = section_match.group(1).strip()
                current_content = [line]
            elif current_section:
                current_content.append(line)
        if current_section:
            self.sections[current_section] = '\n'.join(current_content)
    
    def analyze(self) -> Dict:
        result = {'day_number': self.day_number, 'filepath': str(self.filepath), 'exists': self.filepath.exists(), 'sections_found': [], 'missing_sections': [], 'incomplete_sections': [], 'line_count': len(self.content.split('\n')) if self.content else 0}
        if not self.filepath.exists():
            return result
        for required in REQUIRED_SECTIONS:
            found = False
            for section_name, content in self.sections.items():
                if required in section_name:
                    result['sections_found'].append({'name': section_name, 'line_count': len(content.split('\n')), 'is_complete': len(content.split('\n')) >= 20})
                    found = True
                    if len(content.split('\n')) < 20:
                        result['incomplete_sections'].append(section_name)
                    break
            if not found:
                result['missing_sections'].append(required)
        return result
    
    def get_completeness_score(self) -> float:
        if not self.filepath.exists():
            return 0.0
        score = 0.0
        found_count = 0
        for required in REQUIRED_SECTIONS:
            for section_name, content in self.sections.items():
                if required in section_name:
                    found_count += 1
                    line_count = len(content.split('\n'))
                    if line_count >= 50:
                        score += 20
                    elif line_count >= 30:
                        score += 15
                    elif line_count >= 20:
                        score += 10
                    else:
                        score += 5
                    break
        extra_sections = len(self.sections) - found_count
        score += min(extra_sections * 5, 20)
        return min(score, 100)


class DailyDocumentEnhancer:
    def __init__(self):
        pass
        
    def enhance(self, day_number: str, verbose: bool = True) -> Dict:
        day_number = str(day_number).zfill(3)
        analyzer = DailyDocumentAnalyzer(day_number)
        if not analyzer.load():
            return {'success': False, 'error': f'Document Day{day_number}.md not found'}
        
        analysis = analyzer.analyze()
        if verbose:
            print(f'Analysis for Day{day_number}:')
            print(f'   - Line count: {analysis["line_count"]}')
            print(f'   - Sections found: {len(analysis["sections_found"])}')
            print(f'   - Missing: {analysis["missing_sections"]}')
            print(f'   - Completeness: {analyzer.get_completeness_score():.1f}%')
        
        from .enhancer import ContentGenerator
        generator = ContentGenerator()
        enhanced_content = generator.generate(analyzer, verbose)
        
        if enhanced_content:
            backup_path = DAILY_DIR / f'Day{day_number}.md.bak'
            analyzer.filepath.rename(backup_path)
            analyzer.filepath.write_text(enhanced_content, encoding='utf-8')
            result = {'success': True, 'day_number': day_number, 'changes': {'missing': analysis['missing_sections'], 'incomplete': analysis['incomplete_sections']}, 'new_lines': len(enhanced_content.split('\n')), 'backup': str(backup_path)}
            if verbose:
                print(f'Enhanced Day{day_number}: {result["new_lines"]} lines')
            return result
        return {'success': True, 'day_number': day_number, 'message': 'Already complete'}
    
    def enhance_all(self, start_day: str = '001', end_day: str = '090', skip_existing: bool = True, verbose: bool = True) -> Dict:
        results = {'total': 0, 'enhanced': 0, 'skipped': 0, 'failed': 0, 'details': []}
        start, end = int(start_day), int(end_day)
        for day in range(start, end + 1):
            day_str = str(day).zfill(3)
            results['total'] += 1
            analyzer = DailyDocumentAnalyzer(day_str)
            if not analyzer.load():
                results['failed'] += 1
                results['details'].append({'day': day_str, 'status': 'not_found'})
                continue
            score = analyzer.get_completeness_score()
            if skip_existing and score >= 90:
                if verbose:
                    print(f'Skipping Day{day_str}: Already complete ({score:.1f}%)')
                results['skipped'] += 1
                continue
            result = self.enhance(day_str, verbose=False)
            if result['success']:
                results['enhanced'] += 1
                results['details'].append({'day': day_str, 'status': 'enhanced'})
            else:
                results['failed'] += 1
        if verbose:
            print(f'Summary: Total={results["total"]}, Enhanced={results["enhanced"]}, Skipped={results["skipped"]}, Failed={results["failed"]}')
        return results


def enhance(day_number: str, verbose: bool = True) -> Dict:
    enhancer = DailyDocumentEnhancer()
    return enhancer.enhance(day_number, verbose=verbose)


def enhance_all(start_day: str = '001', end_day: str = '090', skip_existing: bool = True, verbose: bool = True) -> Dict:
    enhancer = DailyDocumentEnhancer()
    return enhancer.enhance_all(start_day, end_day, skip_existing, verbose)


def analyze(day_number: str) -> Dict:
    analyzer = DailyDocumentAnalyzer(day_number)
    if not analyzer.load():
        return {'error': f'Document Day{day_number.zfill(3)}.md not found'}
    analysis = analyzer.analyze()
    analysis['completeness_score'] = analyzer.get_completeness_score()
    return analysis
