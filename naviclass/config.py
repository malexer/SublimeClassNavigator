from collections import namedtuple

from .util import Config


ConfigItem = namedtuple(
    'ConfigItem',
    ['class_filter', 'function_filter'],
)


config = Config({
    'source.python': ConfigItem(
        class_filter=lambda s: '(…)' not in s and '(' in s,
        function_filter=lambda s: '(…)' in s),

    # default - used for all other sources
    None: ConfigItem(
        class_filter=lambda s: not s.startswith(' '),
        function_filter=lambda s: True),
})
