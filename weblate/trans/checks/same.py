# -*- coding: utf-8 -*-
#
# Copyright © 2012 - 2014 Michal Čihař <michal@cihar.com>
#
# This file is part of Weblate <http://weblate.org/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from django.utils.translation import ugettext_lazy as _
from weblate.trans.checks.base import TargetCheck
from weblate.trans.checks.format import (
    PYTHON_PRINTF_MATCH, PHP_PRINTF_MATCH, C_PRINTF_MATCH,
    PYTHON_BRACE_MATCH,
)
import re

# We ignore some words which are usually not translated
SAME_BLACKLIST = frozenset((
    'abc',
    'accelerator',
    'account',
    'action',
    'actions',
    'active',
    'add-ons',
    'addons',
    'address',
    'admin',
    'administrator',
    'administration',
    'africa',
    'agenda',
    'alarm',
    'album',
    'aliasing',
    'alt',
    'altitude',
    'amazon',
    'android',
    'antialias',
    'antialiasing',
    'applet',
    'appliance',
    'appliances',
    'aptitude',
    'array',
    'artist',
    'attribute',
    'attribution',
    'atom',
    'audio',
    'author',
    'auto',
    'autostart',
    'authentication',
    'avatar',
    'backend',
    'backspace',
    'balance',
    'baltic',
    'bar',
    'baseball',
    'battery',
    'begin',
    'bios',
    'bit',
    'bitcoin',
    'bitcoins',
    'bitmap',
    'bitmaps',
    'block',
    'blog',
    'bluetooth',
    'bool',
    'boolean',
    'boot',
    'bootloader',
    'branch',
    'broadcast',
    'browser',
    'buffer',
    'byte',
    'bytes',
    'bzip',
    'bzip2',
    'cache',
    'captcha',
    'caps',
    'cardinality',
    'charset',
    'charsets',
    'chat',
    'china',
    'click',
    'clipboard',
    'club',
    'code',
    'collation',
    'color',
    'commit',
    'component',
    'components',
    'compression',
    'conductor',
    'console',
    'contact',
    'contacts',
    'context',
    'control',
    'cookie',
    'copyright',
    'creation',
    'criteria',
    'csd',
    'csv',
    'ctrl',
    'cvs',
    'cyrillic',
    'dashboard',
    'data',
    'database',
    'date',
    'dbm',
    'debian',
    'debug',
    'default',
    'definition',
    'del',
    'delete',
    'demo',
    'description',
    'design',
    'designer',
    'destination',
    'detail',
    'details',
    'ding',
    'direction',
    'disc',
    'distance',
    'distribution',
    'distro',
    'doc',
    'docs',
    'doctor',
    'document',
    'documentation',
    'dollar',
    'download',
    'downloads',
    'dpkg',
    'dpi',
    'drizzle',
    'dummy',
    'dump',
    'e-mail',
    'editor',
    'eib',
    'ellipsis',
    'email',
    'engine',
    'engines',
    'enter',
    'enterprise',
    'enum',
    'error',
    'escape',
    'exchange',
    'excel',
    'expert',
    'export',
    'extra',
    'false',
    'fanfare',
    'farm',
    'fauna',
    'fax',
    'fedora',
    'feeds',
    'feet',
    'file',
    'files',
    'filter',
    'filters',
    'finance',
    'firewall',
    'firmware',
    'fjord',
    'flash',
    'flattr',
    'flora',
    'font',
    'format',
    'freemind',
    'freeplane',
    'full',
    'fulltext',
    'function',
    'gammu',
    'general',
    'gentoo',
    'geocache',
    'geocaching',
    'gettext',
    'global',
    'gnu',
    'golf',
    'google',
    'gib',
    'git',
    'gpl',
    'gpx',
    'graphic',
    'graphics',
    'grant',
    'gtk',
    'gzip',
    'hack',
    'hacks',
    'handle',
    'handler',
    'hardware',
    'hash',
    'hashed',
    'headset',
    'help',
    'hmpf',
    'home',
    'homepage',
    'hong',
    'hook',
    'horizontal',
    'host',
    'hosting',
    'hostname',
    'hostel',
    'hotel',
    'html',
    'http',
    'hut',
    'hyperlink',
    'icmp',
    'icon',
    'icons',
    'ids',
    'idea',
    'ignore',
    'irc',
    'irda',
    'image',
    'imap',
    'imei',
    'imsi',
    'import',
    'inconsistent',
    'index',
    'india',
    'indigo',
    'info',
    'information',
    'infrastructure',
    'inline',
    'innodb',
    'input',
    'ins',
    'insert',
    'install',
    'installation',
    'int',
    'integer',
    'interlingua',
    'internet',
    'intro',
    'introduction',
    'ion',
    'ios',
    'ip6tables',
    'iptables',
    'irix',
    'isbn',
    'ismn',
    'issn',
    'isrc',
    'item',
    'items',
    'jabber',
    'java',
    'join',
    'joins',
    'jpeg',
    'karaoke',
    'kernel',
    'kib',
    'kill',
    'knoppix',
    'kong',
    'label',
    'land',
    'latex',
    'latin',
    'latitude',
    'layout',
    'ldif',
    'level',
    'libgammu',
    'linestring',
    'link',
    'links',
    'linux',
    'list',
    'lithium',
    'lithium',
    'lock',
    'local',
    'locales',
    'logcheck',
    'login',
    'logo',
    'logos',
    'longitude',
    'lord',
    'ltr',
    'mah',
    'manager',
    'mandrake',
    'mandriva',
    'manual',
    'mail',
    'mailbox',
    'mailboxes',
    'maildir',
    'mailing',
    'markdown',
    'master',
    'max',
    'maximum',
    'media',
    'mediawiki',
    'menu',
    'merge',
    'mesh',
    'message',
    'messages',
    'meta',
    'metal',
    'metre',
    'metres',
    'mib',
    'micropayment',
    'micropayments',
    'microsoft',
    'migration',
    'mile',
    'min',
    'minimum',
    'mint',
    'minus',
    'minute',
    'minutes',
    'mode',
    'model',
    'module',
    'modules',
    'monitor',
    'monument',
    'motel',
    'motif',
    'mouse',
    'mph',
    'multiplayer',
    'musicbottle',
    'name',
    'namecoin',
    'namecoins',
    'navigation',
    'net',
    'netfilter',
    'network',
    'neutral',
    'nimh',
    'node',
    'none',
    'normal',
    'note',
    'notify',
    'null',
    'num',
    'numeric',
    'obex',
    'office',
    'offline',
    'ogg',
    'online',
    'opac',
    'open',
    'opendocument',
    'openmaps',
    'openstreet',
    'opensuse',
    'openvpn',
    'opera',
    'operator',
    'option',
    'options',
    'orientation',
    'osm',
    'osmand',
    'output',
    'overhead',
    'package',
    'page',
    'pager',
    'pages',
    'parameter',
    'parameters',
    'park',
    'partition',
    'party',
    'password',
    'pause',
    'paypal',
    'pdf',
    'pdu',
    'percent',
    'perfume',
    'personal',
    'performance',
    'php',
    'phpmyadmin',
    'pib',
    'ping',
    'pirate',
    'pirates',
    'placement',
    'plan',
    'playlist',
    'plugin',
    'plugins',
    'plural',
    'plus',
    'png',
    'podcast',
    'podcasts',
    'point',
    'polygon',
    'polymer',
    'pool',
    'port',
    'portable',
    'portrait',
    'position',
    'post',
    'posts',
    'pre',
    'pre-commit',
    'prince',
    'procedure',
    'procedures',
    'process',
    'profiling',
    'program',
    'project',
    'promotion',
    'property',
    'properties',
    'protocol',
    'provider',
    'proxy',
    'pull',
    'push',
    'python',
    'python-gammu',
    'query',
    'question',
    'questions',
    'radar',
    'radio',
    'radius',
    'rate',
    'realm',
    'rebase',
    'redhat',
    'regexp',
    'region',
    'relation',
    'relations',
    'render',
    'replication',
    'repository',
    'report',
    'reports',
    'reset',
    'resource',
    'responsive',
    'restaurant',
    'restaurants',
    'return',
    'rich-text',
    'richtext',
    'roadmap',
    'route',
    'routine',
    'routines',
    'rss',
    'rst',
    'rtl',
    'salt',
    'sauna',
    'saver',
    'scalable',
    'scenario',
    'score',
    'screen',
    'screenshot',
    'screensaver',
    'script',
    'scripts',
    'scripting',
    'scroll',
    'sector',
    'seed',
    'selinux',
    'send',
    'sergeant',
    'serie',
    'series',
    'server',
    'servers',
    'service',
    'set',
    'shell',
    'shift',
    'sim',
    'singular',
    'site',
    'slash',
    'slide',
    'slideshow',
    'slot',
    'slots',
    'slug',
    'sms',
    'smsc',
    'smsd',
    'snapshot',
    'snapshots',
    'snmp',
    'socket',
    'software',
    'solaris',
    'source',
    'spatial',
    'spline',
    'sport',
    'sql',
    'standard',
    'start',
    'status',
    'stop',
    'string',
    'strings',
    'structure',
    'style',
    'submit',
    'subproject',
    'subquery',
    'substring',
    'suggestion',
    'suggestions',
    'sum',
    'sunos',
    'supermarket',
    'support',
    'suse',
    'svg',
    'symbol',
    'syndication',
    'system',
    'swap',
    'tab',
    'table',
    'tables',
    'tabs',
    'tada',
    'tag',
    'tags',
    'taiwan',
    'tbx',
    'tent',
    'termbase',
    'test',
    'texy',
    'text',
    'theme',
    'theora',
    'thread',
    'threads',
    'tib',
    'timer',
    'todo',
    'todos',
    'total',
    'tray',
    'trigger',
    'triggers',
    'true',
    'tutorial',
    'tour',
    'type',
    'twiki',
    'twitter',
    'ubuntu',
    'ukolovnik',
    'unicode',
    'unique',
    'unit',
    'update',
    'upload',
    'url',
    'utf',
    'variable',
    'variables',
    'vcalendar',
    'vcard',
    'vector',
    'version',
    'versions',
    'vertical',
    'video',
    'view',
    'views',
    'vorbis',
    'vote',
    'votes',
    'wammu',
    'web',
    'website',
    'weblate',
    'widget',
    'widgets',
    'wiki',
    'wikipedia',
    'wildcard',
    'windowed',
    'windows',
    'word',
    'www',
    'xhtml',
    'xkeys',
    'xml',
    'yard',
    'zen',
    'zero',
    'zip',
    'zoo',
    'zoom',

    # Months are same in some languages
    'january',
    'february',
    'march',
    'april',
    'may',
    'june',
    'july',
    'august',
    'september',
    'october',
    'november',
    'december',

    'jan',
    'feb',
    'mar',
    'apr',
    'jun',
    'jul',
    'aug',
    'sep',
    'oct',
    'nov',
    'dec',

    # Week names shotrcuts
    'mon',
    'tue',
    'wed',
    'thu',
    'fri',
    'sat',
    'sun',

    # Roman numbers
    'iii',

    # Architectures
    'alpha',
    'amd',
    'amd64',
    'arm',
    'aarch',
    'aarch64',
    'hppa',
    'i386',
    'i586',
    'm68k',
    'powerpc',
    'sparc',
    'x86_64',

    # Language names
    'afrikaans',
    'acholi',
    'akan',
    'albanian',
    'amharic',
    'angika',
    'arabic',
    'aragonese',
    'argentinean',
    'armenian',
    'assamese',
    'asturian',
    'aymará',
    'azerbaijani',
    'basque',
    'belarusian',
    'bengali',
    'bodo',
    'bokmål',
    'bosnian',
    'brazil',
    'breton',
    'bulgarian',
    'burmese',
    'catalan',
    'colognian',
    'cornish',
    'croatian',
    'czech',
    'danish',
    'dogri',
    'dutch',
    'dzongkha',
    'english',
    'esperanto',
    'estonian',
    'faroese',
    'filipino',
    'finnish',
    'flemish',
    'franco',
    'french',
    'frisian',
    'friulian',
    'fulah',
    'gaelic',
    'galician',
    'georgian',
    'german',
    'greek',
    'greenlandic',
    'gujarati',
    'gun',
    'haitian',
    'hausa',
    'hebrew',
    'hindi',
    'hungarian',
    'chhattisgarhi',
    'chiga',
    'chinese',
    'icelandic',
    'indonesian',
    'interlingua',
    'irish',
    'italian',
    'japanese',
    'javanese',
    'kannada',
    'kashubian',
    'kazakh',
    'khmer',
    'kinyarwanda',
    'kirghiz',
    'klingon',
    'korean',
    'kurdish',
    'kyrgyz',
    'lao',
    'latvian',
    'limburgish',
    'lingala',
    'lithuanian',
    'lojban',
    'luxembourgish',
    'macedonian',
    'maithili',
    'malagasy',
    'malay',
    'malayalam',
    'maltese',
    'mandinka',
    'manipuri',
    'maori',
    'mapudungun',
    'marathi',
    'mongolian',
    'morisyen',
    'nahuatl',
    'neapolitan',
    'nepali',
    'norwegian',
    'nynorsk',
    'occitan',
    'oriya',
    'ossetian',
    'papiamento',
    'pedi',
    'persian',
    'piemontese',
    'piqad',
    'polish',
    'portugal',
    'portuguese',
    u'provençal',
    'punjabi',
    'pushto',
    'romanian',
    'romansh',
    'russian',
    'sami',
    'santali',
    'sardinian',
    'scots',
    'serbian',
    'sindhi',
    'sinhala',
    'slovak',
    'slovenian',
    'somali',
    'songhai',
    'sorani',
    'sotho',
    'spanish',
    'sundanese',
    'swahili',
    'swedish',
    'tagalog',
    'tajik',
    'tamil',
    'tatar',
    'telugu',
    'thai',
    'tibetan',
    'tigrinya',
    'tsonga',
    'turkish',
    'turkmen',
    'uighur',
    'ukrainian',
    'urdu',
    'uzbek',
    'valencian',
    'venda',
    'vietnamese',
    'walloon',
    'welsh',
    'wolof',
    'yakut',
    'yoruba',
    'zulu',

    # whole alphabet
    'abcdefghijklmnopqrstuvwxyz',
))

# Email address to ignore
EMAIL_RE = re.compile(
    r'[a-z0-9_.-]+@[a-z0-9_.-]+\.[a-z0-9-]{2,}',
    re.IGNORECASE
)

URL_RE = re.compile(
    r'(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
    r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$',
    re.IGNORECASE
)

HASH_RE = re.compile(r'#[A-Za-z0-9_-]*')

DOMAIN_RE = re.compile(
    r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
    r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)',
    re.IGNORECASE
)

PATH_RE = re.compile(r'(^|[ ])(/[a-zA-Z0-9=:?._-]+)+')

TEMPLATE_RE = re.compile(r'{[a-z_-]+}|@[A-Z_]@')

RST_MATCH = re.compile(r'(?::ref:`[^`]+`|``[^`]+``)')

SPLIT_RE = re.compile(
    ur'(?:\&(?:nbsp|rsaquo|lt|gt|amp|ldquo|rdquo|times|quot);|' +
    ur'[() ,.^`"\'\\/_<>!?;:|{}*^@%#&~=+\r\n✓—…\[\]0-9-])+'
)

# Docbook tags to ignore
DB_TAGS = (
    'screen',
    'indexterm',
    'programlisting',
)


def strip_format(msg, flags):
    '''
    Checks whether given string contains only format strings
    and possible punctation. These are quite often not changed
    by translators.
    '''
    if 'python-format' in flags:
        regex = PYTHON_PRINTF_MATCH
    elif 'python-brace-format' in flags:
        regex = PYTHON_BRACE_MATCH
    elif 'php-format' in flags:
        regex = PHP_PRINTF_MATCH
    elif 'c-format' in flags:
        regex = C_PRINTF_MATCH
    elif 'rst-text' in flags:
        regex = RST_MATCH
    else:
        return msg
    stripped = regex.sub('', msg)
    return stripped


def strip_string(msg, flags):
    '''
    Strips (usually) not translated parts from the string.
    '''
    # Strip format strings
    stripped = strip_format(msg, flags)

    # Remove email addresses
    stripped = EMAIL_RE.sub('', stripped)

    # Strip full URLs
    stripped = URL_RE.sub('', stripped)

    # Strip hash tags / IRC channels
    stripped = HASH_RE.sub('', stripped)

    # Strip domain names/URLs
    stripped = DOMAIN_RE.sub('', stripped)

    # Strip file/URL paths
    stripped = PATH_RE.sub('', stripped)

    # Strip template markup
    stripped = TEMPLATE_RE.sub('', stripped)

    # Cleanup trailing/leading chars
    return stripped


def test_word(word):
    '''
    Test whether word should be ignored.
    '''
    return len(word) <= 2 or word in SAME_BLACKLIST


class SameCheck(TargetCheck):
    '''
    Check for not translated entries.
    '''
    check_id = 'same'
    name = _('Unchanged translation')
    description = _('Source and translated strings are same')
    severity = 'warning'

    def should_ignore(self, source, unit, cache_slot):
        '''
        Check whether given unit should be ignored.
        '''
        # Use cache if available
        result = self.get_cache(unit, cache_slot)
        if result is not None:
            return result

        # Ignore some docbook tags
        if unit.comment.startswith('Tag: '):
            if unit.comment[5:] in DB_TAGS:
                self.set_cache(unit, True, cache_slot)
                return True

        # Lower case source
        lower_source = source.lower()

        # Check special things like 1:4 1/2 or copyright
        if (len(source.strip('0123456789:/,.')) <= 1
                or '(c) copyright' in lower_source
                or u'©' in source):
            result = True
        else:
            # Strip format strings
            stripped = strip_string(lower_source, unit.all_flags)

            # Ignore strings which don't contain any string to translate
            # or just single letter (usually unit or something like that)
            if len(stripped) <= 1:
                result = True
            else:
                # Check if we have any word which is not in blacklist
                # (words which are often same in foreign language)
                for word in SPLIT_RE.split(stripped):
                    if not test_word(word):
                        return False
                return True

        # Store in cache
        self.set_cache(unit, result, cache_slot)

        return result

    def check_single(self, source, target, unit, cache_slot):
        # English variants will have most things not translated
        if self.is_language(unit, ('en', )):
            return False

        # One letter things are usually labels or decimal/thousand separators
        if len(source) <= 1 and len(target) <= 1:
            return False

        # Probably shortcut
        if source.isupper() and target.isupper():
            return False

        # Check for ignoring
        if self.should_ignore(source, unit, cache_slot):
            return False

        return source == target
