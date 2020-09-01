$PROJECT = $GITHUB_ORG = $GITHUB_REPO = 'xonsh'
$ACTIVITIES = [
    'authors', 'version_bump', 'changelog',
    'tag', 'push_tag', 'ghrelease',
    'pypi',
    #'conda_forge',
]
$PYPI_SIGN = False

$AUTHORS_FILENAME = "AUTHORS.md"
$VERSION_BUMP_PATTERNS = [
    ('conda_suggest/__init__.py', r'__version__\s*=.*', '__version__ = "$VERSION"'),
    ('setup.py', r'version\s*=.*,', 'version="$VERSION",'),
]

$CHANGELOG_FILENAME = 'CHANGELOG.md'
$CHANGELOG_TEMPLATE = 'TEMPLATE.md'
$CHANGELOG_PATTERN = "<!-- current developments -->"
$CHANGELOG_HEADER = """
<!-- current developments -->

## v$VERSION
"""
