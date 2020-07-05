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
import asyncio


logger = logging.getLogger(__name__)


@loader.tds
class SendMsgMod(loader.Module):
    """Executes a send message to a Telegram ID"""
    strings = {"name": "SendMsg",
               "need_id_msg": "<b>Need Chat ID / Phone number and Message.</b>",
               "need_msg": "<b>Need Message.</b>"}

    async def sendcmd(self, message):
        """.send <id> <message>\n.send @yourusername hello\n.send +xxxxxxxxxxxx hello"""
        use_reply = False
        args = utils.get_args(message)
        if len(args) == 0:
            await utils.answer(message, self.strings("need_id_msg", message))
            return
        if len(args) == 1:
            await utils.answer(message, self.strings("need_msg", message))
            return
        await message.client.send_message(args[0], " ".join(args[1:]))
