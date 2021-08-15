#    Friendly Telegram (telegram userbot)
#    Copyright (C) 2018-2019 The Authors

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

# requires: pyyandextranslateapi

import logging
import requests
import urllib
import json
import re

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class TranslateMod(loader.Module):
    """Translator"""
    strings = {"name": "Translator",
               "translated": "<b>From: </b><code>{from_lang}</code>"
               "\n<b>To: </b><code>{to_lang}</code>\n\n{output}",
               "invalid_text": "Invalid text to translate or from_lang or to_lang not correctly declared",
               "doc_default_lang": "Language to translate to by default"}

    def __init__(self):
        self.config = loader.ModuleConfig("DEFAULT_LANG", "en", lambda m: self.strings("doc_default_lang", m))
		

    @loader.unrestricted
    @loader.ratelimit
    async def translatecmd(self, message):
        """.translate [from_lang->][->to_lang] <text>"""
        args = utils.get_args(message)
        logger.debug(message)
        logger.debug(args)
        print(message)
        print(args)
        if len(args) <= 2:
            if message.is_reply:
                text = (await message.get_reply_message()).message
            else:
                await utils.answer(message, self.strings("invalid_text", message))
                return
        else:
            text = " ".join(args[2:])
        print("Text: " + text)
        print(args)
        sentences = re.split('\. |\? |\! ', text)
        text = urllib.parse.quote(text)
        print("Text_URL: " + text)
        url = "http://translate.googleapis.com/translate_a/single?client=gtx&sl=" + args[0] + "&tl=" + args[1] + "&dt=t&q=" + text
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; SM-A310F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.91 Mobile Safari/537.36 OPR/42.7.2246.114996'}
        print(url)
        print(headers)
        r = requests.post(url, "", json.dumps(headers))
        print(r.text)
        translated = ""
        for sentence in sentences:
            sentence = sentence.replace("'","")
            sentence = sentence.replace("\n","")
            part = (r.text.split(sentence)[0]).split('["')
            translated = translated + (part[len(part)-1])[:-4] + " "
        ret = self.strings("translated", message).format(from_lang=utils.escape_html(args[0]), to_lang=utils.escape_html(args[1]), output=utils.escape_html(translated))
        await utils.answer(message, ret)