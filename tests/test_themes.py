import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build import load_tokens, render_contrast, render_css


class ThemeTests(unittest.TestCase):
    def test_all_theme_text_passes_aa_on_every_surface(self):
        report = json.loads(render_contrast(load_tokens()))
        self.assertEqual(report['bad'], [])

    def test_mono_is_achromatic_except_for_the_brand_mark(self):
        tokens = load_tokens()
        for name, value in tokens['theme']['light-mono'].items():
            if name in ('brandGreen', 'brandOrange'):
                continue
            self.assertEqual(value[1:3], value[3:5], name)
            self.assertEqual(value[3:5], value[5:7], name)
        for name, value in tokens['themeOverrides']['light-mono'].items():
            if value.startswith('#'):
                self.assertEqual(value[1:3], value[3:5], name)
                self.assertEqual(value[3:5], value[5:7], name)
        self.assertNotEqual(tokens['mark']['light']['green'], tokens['mark']['light']['orange'])

    def test_color_palettes_reset_when_a_theme_is_nested_inside_mono(self):
        css = render_css(load_tokens())
        color_rule = css.split('/* theme: light */')[1].split('/* theme: dark */')[0]
        self.assertIn('--xd-spine-hoja: #166534;', color_rule)
        self.assertIn('--xd-gradient-grin: linear-gradient(90deg, var(--xd-brand-green), var(--xd-brand-orange));', color_rule)


if __name__ == '__main__':
    unittest.main()
