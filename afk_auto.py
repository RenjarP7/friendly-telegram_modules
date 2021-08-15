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

from .. import loader, utils

import logging
import datetime
import time

logger = logging.getLogger(__name__)


@loader.tds
class AFKAutoMod(loader.Module):
    """Provides a message saying that you are unavailable"""
    strings = {"name": "AFK_AUTO",
               "gone": "<b>I'm going AFK_AUTO</b>",
               "back": "<b>I'm no longer AFK_AUTO</b>",
               "afk": "<b>Automatische Antwort:</b>\nIch bin ist seit {} nicht "
               "mehr zu erreichen.\nGrund:\n<i>Ich fahre gerade Auto. Deine "
               "Nachricht wird mir aber vorgelesen.</i>\n\n<b>Automatic reply:"
               "</b>\nI have been unreachable since {}.\nReason:\n<i>I'm driving "
               "right now. But your message will be read to me.</i>"}

    async def client_ready(self, client, db):
        self._db = db
        self._me = await client.get_me()

    async def afk_autocmd(self, message):
        """.afk [message]"""

        self._db.set(__name__, "afk", True)
        self._db.set(__name__, "gone", time.time())

        await self.allmodules.log("afk", data=utils.get_args_raw(message) or None)
        await utils.answer(message, self.strings("gone", message))

    async def unafk_autocmd(self, message):
        """Remove the AFK status"""
        self._db.set(__name__, "afk", False)
        self._db.set(__name__, "gone", None)
        await self.allmodules.log("unafk")
        await utils.answer(message, self.strings("back", message))

    async def watcher(self, message):
        if message.mentioned or getattr(message.to_id, "user_id", None) == self._me.id:
            afk_state = self._db.get(__name__, "afk", False)
            if not afk_state:
                return
            logger.debug("tagged!")
            user = await utils.get_user(message)
            if user.is_self or user.bot or user.verified:
                logger.debug("User is self, bot or verified.")
                return
            now = datetime.datetime.now().replace(microsecond=0)
            gone = datetime.datetime.fromtimestamp(self._db.get(__name__, "gone")).replace(microsecond=0)
            diff = now - gone
            ret = self.strings("afk", message).format(diff, diff)
            await utils.answer(message, ret)
