# coding: utf-8

import logging
import urllib
import urllib2
import re
import json
import requests

import js2py

from django.conf import settings

logger = logging.getLogger(__name__)

RE_RESULT = re.compile(
    r"((?<=\[)(\s*)(?=,))|((?<=,)(\s*)(?=,))|((?<=,)(\s*)(?=\]))",
)
JS_CTX = js2py.EvalJs()
JS_CTX.execute("""
function TL(a) {
    var k = "";
    var b = 406644;
    var b1 = 3293161072;

    var jd = ".";
    var $b = "+-a^+6";
    var Zb = "+-3^+b+-f";

    for (var e = [], f = 0, g = 0; g < a.length; g++) {
        var m = a.charCodeAt(g);
        128 > m ? e[f++] = m : (
            2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) &&
            g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ?
            (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
            e[f++] = m >> 18 | 240,
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
            e[f++] = m >> 6 & 63 | 128),
            e[f++] = m & 63 | 128)
    }
    a = b;
    for (f = 0; f < e.length; f++) a += e[f],
    a = RL(a, $b);
    a = RL(a, Zb);
    a ^= b1 || 0;
    0 > a && (a = (a & 2147483647) + 2147483648);
    a %= 1E6;
    return a.toString() + jd + (a ^ b)
};

function RL(a, b) {
    var t = "a";
    var Yb = "+";
    for (var c = 0; c < b.length - 2; c += 3) {
        var d = b.charAt(c + 2),
        d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
        d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
        a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
    }
    return a
}
""")


class Translator(object):
    API_URL = getattr(
        settings, "BAIDU_API_URL",
        "http://translate.google.cn/translate_a/single"
    )
    NAME = u"谷歌翻译"

    def __init__(self, *args, **kwargs):
        self.session = requests.Session()


    def get_tk(self, text):
        return JS_CTX.TL(text)

    def translate(self, text, from_lang, to_lang):
        parmas = [
            "client=t", "dt=at", "dt=bd", "srcrom=0", "ssel=0",
            "tsel=0", "dt=ex", "dt=ld", "dt=md", "dt=qca", "dt=rw",
            "dt=rm", "dt=ss", "dt=t", "ie=UTF-8", "oe=UTF-8",
            "clearbtn=1", "otf=1", "pc=1", "kc=2",
            "sl=%s" % from_lang,
            "tl=%s" % to_lang,
            "hl=%s" % to_lang,
            "tk=%s" % self.get_tk(text),
            "q=%s" % urllib.quote(text),
        ]
        url = "%s?%s" % (self.API_URL, "&".join(parmas))
        logger.info("google url: %s", url)
        response = self.session.get(url)
        result = json.loads(re.sub(
            r"((?<=\[)(\s*)(?=,))|((?<=,)(\s*)(?=,))|((?<=,)(\s*)(?=\]))",
            "null", response.content,
        ))
        return "".join(i[0] for i in result[0] if i[0])
