#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#WOT_UTILS
exec 'eNqtUsFu2zAMvQfIP/BmOTDce4EdurXYDKxLEKftoRgCWZIdrbLkUvSy/v2kxFqyFhg2YDyRj496D6RadD04Xw6cdqD7wSGB9lIjcA98Pmtjf638bYep7QZlayVIOxtJzUR6r7sHh0Ym2r7bdopW6OQo6F6hn/jtfBYmHEID2kLDsrK8iOq+/NGbLH/MVrHIvpbfuRmVZ/nlfAYhdAucNSX3NaG2XYJjcHgHp84Jb1Dxpyg3n0nVgmTPBewLUGkWw1zwyImQHfAjTAE2vG8khwUvYLF4uoRnhkWqJpo/myzCUDBIL4NimIcNgnUEA4ZdIb2AMl79qhjl+cmU+gdTPqBa9Ip2TrI/OvyvFgVrRyuSv4hYtuDY+YPWPmbn14iEnu24lUbheSNGfCn1ot3fX4mKiYmKRrTQJ2yq7dGXMNx7eFhutneb6nM9qdwur+uwp+wiK785bdljWEfmBeqBfBZSYbSyFLPeyfDHpjWtrjafwhg/Vvc367pafgkAjYNRrOcD05YKaFle+sFoCn82y9OOP95V27/X7Ub9Rn4ZFNfV9c3rCwsm81eUbb252lQf3jLV6WAGgnpTgChAHu7e/gRl2hcJ'.decode('base64').decode('zlib')

from gui.Scaleform.daapi.view.battle.classic.minimap import MarkCellPlugin
from gui.battle_control import minimap_utils
from messenger.ext.channel_num_gen import getClientID4BattleChannel, getClientID4Prebattle
from constants import PREBATTLE_TYPE
from messenger.m_constants import BATTLE_CHANNEL
from messenger import MessengerEntry
from gui import InputHandler
from gui.Scaleform.genConsts.BATTLE_VIEW_ALIASES import BATTLE_VIEW_ALIASES
from gui.Scaleform.framework import ViewTypes
from gui.app_loader import g_appLoader
from messenger.gui.Scaleform.battle_entry import BattleEntry
import game
import Keys

Y_POINT = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K']


class ModSM:
    def __init__(self):
        self.isKeyPress = False


def isBattleChat():
    squadChannelClientID = getClientID4Prebattle(PREBATTLE_TYPE.SQUAD)
    teamChannelClientID = getClientID4BattleChannel(BATTLE_CHANNEL.TEAM.name)
    commonChannelClientID = getClientID4BattleChannel(BATTLE_CHANNEL.COMMON.name)
    team = MessengerEntry.g_instance.gui.channelsCtrl.getController(teamChannelClientID)
    squad = MessengerEntry.g_instance.gui.channelsCtrl.getController(squadChannelClientID)
    common = MessengerEntry.g_instance.gui.channelsCtrl.getController(commonChannelClientID)
    return {'team': team, 'common': common, 'squad': squad}


def handleKeyEvent(event):
    isDown, key, mods, isRepeat = game.convertKeyEvent(event)
    if key == Keys.KEY_LALT:
        modSM.isKeyPress = isDown


@WOT_UTILS.OVERRIDE(MarkCellPlugin, 'setAttentionToCell')
def minimap_setAttentionToCell(func, self, x, y, isRightClick):
    if not isRightClick and modSM.isKeyPress and isBattleChat()["squad"] != None:
        index = minimap_utils.makeCellIndex(x, y)
        _x = (str)(((index - index % 10) / 10) + 1)
        _x = _x[0:-2]
        if _x == '10':
            _x = '0'
        isBattleChat()["squad"].sendMessage('Внимание на квадрат ' + Y_POINT[(int)(index % 10)] + _x + '!')
        return
    func(self, x, y, isRightClick)


@WOT_UTILS.OVERRIDE(BattleEntry, '_BattleEntry__me_onMessageReceived')
def onMessage(func, self, message, channel):
    _message = str(message.text)
    if _message[0:-3] == 'Внимание на квадрат ' and _message[-1] == '!' and len(_message) == 40:
        app = g_appLoader.getDefBattleApp()
        minimap = app.containerManager.getContainer(ViewTypes.VIEW).getView().getComponent(BATTLE_VIEW_ALIASES.MINIMAP)
        cells_plg = minimap.getPlugin('cells')
        x = _message[-2]
        if x == '0':
            x = '10'
        cells_plg._doAttention(Y_POINT.index(_message[-3]) + (int(x) - 1) * 10, 1)

    func(self, message, channel)


modSM = ModSM()
InputHandler.g_instance.onKeyDown += handleKeyEvent
InputHandler.g_instance.onKeyUp += handleKeyEvent

print 'Squad Minimap loaded'
