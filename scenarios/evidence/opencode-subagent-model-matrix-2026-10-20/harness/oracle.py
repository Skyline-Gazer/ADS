"""Independent oracle for the ADS #21 medium task. Not derived from app/contracts.py."""
import sys, math
sys.path.insert(0, 'app')
from temperature import convert_celsius
from tags import normalize_tags

checks = []
def eq(label, fn, want=None, raises=False):
    try:
        got = fn()
    except ValueError:
        if raises: checks.append((label, 'PASS')); return
        checks.append((label, 'FAIL: no ValueError')); return
    except Exception as e:
        checks.append((label, f'FAIL: wrong error {type(e).__name__}')); return
    if raises: checks.append((label, 'FAIL: expected ValueError')); return
    checks.append((label, 'PASS' if got == want else f'FAIL: got {got!r} want {want!r}'))

eq('c=0', lambda: convert_celsius(0), 32)
eq('c=100', lambda: convert_celsius(100), 212)
eq('c=-40', lambda: convert_celsius(-40), -40)
eq('c=2.5', lambda: convert_celsius(2.5), 36.5)
eq('c=21/3', lambda: convert_celsius(7), 44.6)
eq('c_bool', lambda: convert_celsius(True), raises=True)
eq('c_none', lambda: convert_celsius(None), raises=True)
eq('c_str', lambda: convert_celsius('1'), raises=True)
eq('c_inf', lambda: convert_celsius(float('inf')), raises=True)
eq('c_nan', lambda: convert_celsius(float('nan')), raises=True)
eq('t_basic', lambda: normalize_tags([' A ','b','a','',' B ','Straße','STRASSE']), ['a','b','strasse'])
eq('t_empty', lambda: normalize_tags([]), [])
eq('t_none', lambda: normalize_tags(None), raises=True)
eq('t_str', lambda: normalize_tags('one'), raises=True)
eq('t_int_member', lambda: normalize_tags([1]), raises=True)
eq('t_bool_member', lambda: normalize_tags(['ok', True]), raises=True)
eq('t_tuple', lambda: normalize_tags(('a',)), raises=True)

fails = [c for c in checks if not c[1].startswith('PASS')]
for label, res in checks: print(f'{label}: {res}')
print(f'ORACLE {"PASS" if not fails else "FAIL"} ({len(checks)-len(fails)}/{len(checks)})')
sys.exit(0 if not fails else 1)
