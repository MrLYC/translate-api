#!/usr/bin/env python
# encoding: utf-8

import json

from django import http
from django.utils.encoding import smart_text

from translate_api.translators import google


def post(request):
    try:
        data = json.loads(request.body)
    except Exception:
        return http.HttpResponseBadRequest("json is required")

    query = data.get("q")
    from_lang = data.get("f", "auto")
    to_lang = data.get("t", "zh-CN")

    if not data:
        return http.HttpResponseBadRequest("q is required")
    text = smart_text(query, "utf-8")
    translator = google.Translator()
    result = translator.translate(text, from_lang, to_lang)
    return http.JsonResponse({
        "ok": True,
        "text": text,
        "result": result,
    })
