#    Friendly Telegram (telegram userbot)
#    Copyright (C) 2018-2019 The Authors

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from .. import loader, utils
import logging


logger = logging.getLogger(__name__)


@loader.tds
class SendPipeMod(loader.Module):
    """Sends a message to a Telegram account."""
    strings = {"name": "SendPipeMsg",
               "need_id_msg": "<b>Need Chat ID / Phone number and Message."
               "</b>",
               "need_msg": "<b>Need Message.</b>",
               "config_true": "<b>Config successfully updated!\nMessage will "
               "be deleted.</b>",
               "config_false": "<b>Config successfully updated!\nMessage will "
               "be kept.</b>",
               "config_fail": "<b>Failed to update config!\nOnly \'true\' or "
               "\'false\' permitted!\n.sendpipedelconfig &lt;true_or_false&gt;</b>",
               "config_need": "<b>Need true or false.\n.sendpipedelconfig "
               "&lt;true_or_false&gt;</b>",
               "sendpipe_botid_correct": "<b>Config successfully updated!</b>",
               "sendpipe_botid_incorrect": "<b>Failed to update config!\nOnly bot_id "
               "permitted!\nYou got it while creating your Bot."
               "The ID are the numbers befor :\n.sendpipebotconfig &lt;123456789&gt;</b>",
               "sendpipe_botid_need": "<b>Need Bot_ID, you got it while creating your Bot."
               "The ID are the numbers befor :\n.sendpipebotconfig "
               "&lt;123456789&gt;</b>"}

    async def client_ready(self, client, db):
        self._db = db

    async def sendpipedelconfigcmd(self, message):
        """.sendpipedelconfig <true_or_false>\ne.g. .sendpipedelconfig false
If set to true, command message will be deleted after message was send."""
        args = utils.get_args(message)
        if len(args) == 0:
            await utils.answer(message, self.strings("config_need", message))
        else:
            if args[0] == "true":
                self._db.set(__name__, "deleteBotMsg", True)
                await utils.answer(message,
                                   self.strings("config_true", message))
            elif args[0] == "false":
                self._db.set(__name__, "deleteBotMsg", False)
                await utils.answer(message,
                                   self.strings("config_false", message))
            else:
                await utils.answer(message,
                                   self.strings("config_fail", message))
                                
    async def sendpipebotconfigcmd(self, message):
        """.sendpipebotconfig <bot_id>\ne.g. .sendpipebotconfig 123456789
Set the bot_id to only process and forward messages from this particular bot.
If empty, every ID is allowed"""
        args = utils.get_args(message)
        if len(args) == 0:
            await utils.answer(message, self.strings("sendpipe_botid_need", message))
        else:
            if args[0].isdigit():
                self._db.set(__name__, "sendpipe_botid", args[0])
                await utils.answer(message,
                                   self.strings("sendpipe_botid_correct", message))
            else:
                await utils.answer(message,
                                   self.strings("sendpipe_botid_incorrect", message))

    async def sendcmd(self, message):
        """.send <id> <message>\ne.g. .send @user Hello World!"""
        if self._db.get(__name__, "sendpipe_botid", "") == "":
            await utils.answer(message, self.strings("need_id_msg", message))
            return
        if message.from_id == self._db.get(__name__, "sendpipe_botid", False) or self._db.get(__name__, "sendpipe_botid", "") == "":
            args = utils.get_args(message)
            if len(args) == 0:
                await utils.answer(message, self.strings("need_id_msg", message))
                return
            if not message.media and len(args) == 1:
                await utils.answer(message, self.strings("need_msg", message))
                return
            await message.client.send_message(args[0],
                                                message.message.split(" ".join(args[0:1]))[1], 
                                                file=message.media if message.media else None)
            if self._db.get(__name__, "deleteBotMsg", False):
                await message.client.delete_messages(message.to_id, message.id)
