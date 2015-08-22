#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from copy import copy
from collections import OrderedDict

REPORT_DIR  = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
SOURCE_DIR  = '/includes/source/'
SOURCE_PATH = REPORT_DIR + SOURCE_DIR
TARGET_PATH = REPORT_DIR + '/listings/source/'

FILE_PREFIX     = '├─ '
LAST_PREFIX     = '└─ '
TAB_PREFIX      = '│  '
LAST_TAB_PREFIX = '   '

CONF = {
    'magento': {
        'locations': ['demo'],
        'exclude': ['.git', '.gitkeep', 'LICENSE', 'README.md', 'pub'],
        'softExclude': ['composer.lock', '.csv']
    },
    'framework': {
        'locations': ['framework'],
        'exclude': ['.git', '.gitkeep', 'LICENSE', 'README.md'],
        'softExclude': ['monitor.py', 'core/__init__.py', 'tests/__init__.py', 'tests/config/__init__.py', 'tests/core/engine/__init__.py', 'tests/engines/hybrid/__init__.py']
    },
    'inCommon': {
        'locations': ['engines/inCommon'],
        'exclude': ['.git', '.gitkeep', 'LICENSE', 'README.md']
    },
    'itemSimilarity': {
        'locations': ['engines/itemSimilarity'],
        'exclude': ['.git', '.gitkeep', 'LICENSE', 'README.md'],
        'softExclude': ['composer.lock']
    },
    'provision': {
        'locations': ['Vagrantfile', 'provision', '.gitmodules'],
        'exclude': []
    },
}

EXT2LANG = {
    'less': 'css',
    'xsd': 'xml',
    'wsgi': 'py',
    'txt': 'text',
    'Gomfile': 'ruby',
    'htaccess': 'apache',
    'Vagrantfile': 'ruby',
    'pp': 'puppet',
    'gitmodules': 'text',
    'coveragerc': 'text',
    'yml': 'yaml'
}

def get_file_dict(locations, exclude):
    files = OrderedDict()
    for loc in locations:
        subfiles = _get_file_dict([loc], exclude)[loc]

        dirs = loc.split('/')
        if len(dirs) > 1:
            dirs.reverse()
            for d in dirs[:-1]:
                if d == '':
                    continue

                subfiles = OrderedDict([(d, subfiles)])
            loc = dirs[len(dirs)-1]

        files[loc] = subfiles

    return files

def _get_file_dict(locations, exclude, parentLoc=''):
    files = OrderedDict()
    for loc in locations:
        found = False
        for exc in exclude:
            if loc.find(exc) != -1:
                found = True
                break
        if found:
            continue

        absLoc = SOURCE_PATH + parentLoc + loc
        isDir = os.path.isdir(absLoc)

        if isDir:
            files[loc] = _get_file_dict(os.listdir(absLoc), exclude, parentLoc + loc + '/')
        else:
            files[loc] = loc

    return files

def get_tree(files, prefix=''):
    tree = ''
    i = 0
    l = len(files) - 1
    for d, t in files.iteritems():
        isDir = t != d
        linePrefix = FILE_PREFIX if i < l else LAST_PREFIX
        tree += prefix + linePrefix + d + os.linesep

        i += 1
        if t == d:
            continue

        dirPrefix = TAB_PREFIX if (i-1) < l else LAST_TAB_PREFIX
        tree += get_tree(t, prefix + dirPrefix)

    return tree

def get_files(fileDict, result, exclude, path=''):
    for d, f in fileDict.iteritems():
        newPath = path + d

        if (type(f) is OrderedDict):
            get_files(f, result, exclude, newPath + '/')
        else:
            found = False
            for exc in exclude:
                if newPath.find(exc) != -1:
                    found = True
                    break

            if found:
                continue

            result.append(newPath.replace('_', '\string_'))

for moduleName, module in CONF.iteritems():
    fileDict = get_file_dict(module['locations'], module['exclude'])
    tree = get_tree(fileDict)

    files = []
    softExclude = module['softExclude'] if 'softExclude' in module else []
    get_files(fileDict, files, softExclude)

    content = """\\begin{codebox}[Directory structure]
\\begin{minted}{text}
%s
\end{minted}
\end{codebox}

""" % tree

    for f in files:
        lang = f.rsplit('.')
        lang = lang[len(lang)-1]
        if lang == 'dist':
            lang = lang[len(lang) - 2]

        if lang.find('/') != -1:
            lang = f.rsplit('/')
            lang = lang[len(lang) - 1]

        if lang in EXT2LANG:
            lang = EXT2LANG[lang]
        elif lang == f:
            lang = ''

        filePath = '.' + SOURCE_DIR + f

        content += """\\begin{codebox}[%s]
\inputminted{%s}{%s}
\end{codebox}
""" % (f, lang, filePath)

    with open(TARGET_PATH + moduleName + '.tex', 'w') as f:
        f.write(content)