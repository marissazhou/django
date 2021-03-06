from django.forms import SelectMultiple

from .base import WidgetTest


class SelectMultipleTest(WidgetTest):
    widget = SelectMultiple()
    numeric_choices = (('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('0', 'extra'))

    def test_render_selected(self):
        self.check_html(self.widget, 'beatles', ['J'], choices=self.beatles, html=(
            """<select multiple="multiple" name="beatles">
            <option value="J" selected="selected">John</option>
            <option value="P">Paul</option>
            <option value="G">George</option>
            <option value="R">Ringo</option>
            </select>"""
        ))

    def test_render_multiple_selected(self):
        self.check_html(self.widget, 'beatles', ['J', 'P'], choices=self.beatles, html=(
            """<select multiple="multiple" name="beatles">
            <option value="J" selected="selected">John</option>
            <option value="P" selected="selected">Paul</option>
            <option value="G">George</option>
            <option value="R">Ringo</option>
            </select>"""
        ))

    def test_render_none(self):
        """
        If the value is None, none of the options are selected.
        """
        self.check_html(self.widget, 'beatles', None, choices=self.beatles, html=(
            """<select multiple="multiple" name="beatles">
            <option value="J">John</option>
            <option value="P">Paul</option>
            <option value="G">George</option>
            <option value="R">Ringo</option>
            </select>"""
        ))

    def test_render_value_label(self):
        """
        If the value corresponds to a label (but not to an option value), none
        of the options are selected.
        """
        self.check_html(self.widget, 'beatles', ['John'], choices=self.beatles, html=(
            """<select multiple="multiple" name="beatles">
            <option value="J">John</option>
            <option value="P">Paul</option>
            <option value="G">George</option>
            <option value="R">Ringo</option>
            </select>"""
        ))

    def test_multiple_options_same_value(self):
        """
        Multiple options with the same value can be selected (#8103).
        """
        self.check_html(self.widget, 'choices', ['0'], choices=self.numeric_choices, html=(
            """<select multiple="multiple" name="choices">
            <option value="0" selected="selected">0</option>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="0" selected="selected">extra</option>
            </select>"""
        ))

    def test_multiple_values_invalid(self):
        """
        If multiple values are given, but some of them are not valid, the valid
        ones are selected.
        """
        self.check_html(self.widget, 'beatles', ['J', 'G', 'foo'], choices=self.beatles, html=(
            """<select multiple="multiple" name="beatles">
            <option value="J" selected="selected">John</option>
            <option value="P">Paul</option>
            <option value="G" selected="selected">George</option>
            <option value="R">Ringo</option>
            </select>"""
        ))

    def test_compare_string(self):
        choices = [('1', '1'), ('2', '2'), ('3', '3')]

        self.check_html(self.widget, 'nums', [2], choices=choices, html=(
            """<select multiple="multiple" name="nums">
            <option value="1">1</option>
            <option value="2" selected="selected">2</option>
            <option value="3">3</option>
            </select>"""
        ))

        self.check_html(self.widget, 'nums', ['2'], choices=choices, html=(
            """<select multiple="multiple" name="nums">
            <option value="1">1</option>
            <option value="2" selected="selected">2</option>
            <option value="3">3</option>
            </select>"""
        ))

        self.check_html(self.widget, 'nums', [2], choices=choices, html=(
            """<select multiple="multiple" name="nums">
            <option value="1">1</option>
            <option value="2" selected="selected">2</option>
            <option value="3">3</option>
            </select>"""
        ))

    def test_optgroup_select_multiple(self):
        widget = SelectMultiple(choices=(
            ('outer1', 'Outer 1'),
            ('Group "1"', (('inner1', 'Inner 1'), ('inner2', 'Inner 2'))),
        ))
        self.check_html(widget, 'nestchoice', ['outer1', 'inner2'], html=(
            """<select multiple="multiple" name="nestchoice">
            <option value="outer1" selected="selected">Outer 1</option>
            <optgroup label="Group &quot;1&quot;">
            <option value="inner1">Inner 1</option>
            <option value="inner2" selected="selected">Inner 2</option>
            </optgroup>
            </select>"""
        ))
