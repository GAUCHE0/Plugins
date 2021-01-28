from phBot import *
import QtBind
import phBotChat
from time import sleep
import json
import os
import struct
import time
import subprocess

pVersion = '0.0.1'
pName = 'UltimateItemManager'
pUrl = 'https://raw.githubusercontent.com/GAUCHE0/Plugins/main/UltimateItemManager.py'

# KURESELLER
character_data = None
locale = None

gui_ = QtBind.init(__name__,pName)

_x = 10
_y = 0

ButtonArea1 = QtBind.createList(gui_, _x, _y, _x+160, _y+271)
lMG = QtBind.createLabel(gui_, "| MAGIC STONE | ", _x+20,_y+1 )
lluck = QtBind.createLabel(gui_, "LUCK STONE ", _x+10,_y+45)
qluck = QtBind.createLabel(gui_, "0", _x+119,_y+45)
lsteady = QtBind.createLabel(gui_, "STEADY STONE",_x+10,_y+60)
qsteady = QtBind.createLabel(gui_, "0",_x+119,_y+60)
limmortal = QtBind.createLabel(gui_, "IMMORTAL STONE",_x+10,_y+75)
qimmortal = QtBind.createLabel(gui_, "0",_x+119,_y+75)
lmaster = QtBind.createLabel(gui_, "MASTER STONE",_x+10,_y+90)
qmaster = QtBind.createLabel(gui_, "0",_x+119,_y+90)
lstamina = QtBind.createLabel(gui_, "STAMINA STONE",_x+10,_y+105)
qstamina = QtBind.createLabel(gui_, "0",_x+119,_y+105)
lmagic = QtBind.createLabel(gui_, "MAGIC STONE",_x+10,_y+120)
qmagic = QtBind.createLabel(gui_, "0",_x+119,_y+120)
lstrikes = QtBind.createLabel(gui_, "STRIKES STONE",_x+10,_y+135)
qstrikes = QtBind.createLabel(gui_, "0",_x+119,_y+135)
ldiscipline = QtBind.createLabel(gui_, "DISCIPLINE STONE",_x+10,_y+150)
qdiscipline = QtBind.createLabel(gui_, "0",_x+119,_y+150)
lpenetration = QtBind.createLabel(gui_, "PENETRATION STONE",_x+10,_y+165)
qpenetration = QtBind.createLabel(gui_, "0",_x+119,_y+165)
ldodging = QtBind.createLabel(gui_, "DODGING STONE",_x+10,_y+180)
qdodging = QtBind.createLabel(gui_, "0",_x+119,_y+180)
lfogs = QtBind.createLabel(gui_, "FOGS STONE",_x+10,_y+195)
qfogs = QtBind.createLabel(gui_, "0",_x+119,_y+195)
lair = QtBind.createLabel(gui_, "AIR STONE",_x+10,_y+210)
qair = QtBind.createLabel(gui_, "0",_x+119,_y+210)
lfire = QtBind.createLabel(gui_, "FIRE STONE",_x+10,_y+225)
qfire = QtBind.createLabel(gui_, "0",_x+119,_y+225)
limmunity = QtBind.createLabel(gui_, "IMMUNITY STONE",_x+10,_y+240)
qimmunity = QtBind.createLabel(gui_, "0",_x+119,_y+240)
lrevival = QtBind.createLabel(gui_, "REVIVAL STONE",_x+10,_y+255)
qrevival = QtBind.createLabel(gui_, "0",_x+119,_y+255)
lhp = QtBind.createLabel(gui_, "STR STONE",_x+10,_y+15)
qhp = QtBind.createLabel(gui_, "0",_x+119,_y+15)
lmp = QtBind.createLabel(gui_, "INT STONE",_x+10,_y+30)
qmp = QtBind.createLabel(gui_, "0",_x+119,_y+30)
ButtonArea5 = QtBind.createList(gui_, _x+150, _y, _x+141, _y+271)
lATT = QtBind.createLabel(gui_, "| ATTRIBUTE STONE | ", _x+165,_y+1 )
lcourage = QtBind.createLabel(gui_, "COURAGE STONE ", _x+160,_y+15)
qcourage = QtBind.createLabel(gui_, "0", _x+269,_y+15)
lwarriors = QtBind.createLabel(gui_, "WARRIORS STONE",_x+160,_y+30)
qwarriors = QtBind.createLabel(gui_, "0",_x+269,_y+30)
lphilosophy = QtBind.createLabel(gui_, "PHILOSOPHY STONE",_x+160,_y+45)
qphilosophy = QtBind.createLabel(gui_, "0",_x+269,_y+45)
lmeditation = QtBind.createLabel(gui_, "MEDITATION STONE",_x+160,_y+60)
qmeditation = QtBind.createLabel(gui_, "0",_x+269,_y+60)
lchallenge = QtBind.createLabel(gui_, "CHALLENGE STONE",_x+160,_y+75)
qchallenge = QtBind.createLabel(gui_, "0",_x+269,_y+75)
lfocus = QtBind.createLabel(gui_, "FOCUS STONE",_x+160,_y+90)
qfocus = QtBind.createLabel(gui_, "0",_x+269,_y+90)
lflesh = QtBind.createLabel(gui_, "FLESH STONE",_x+160,_y+105)
qflesh = QtBind.createLabel(gui_, "0",_x+269,_y+105)
llife = QtBind.createLabel(gui_, "LIFE STONE",_x+160,_y+120)
qlife = QtBind.createLabel(gui_, "0",_x+269,_y+120)
lmind = QtBind.createLabel(gui_, "MIND STONE",_x+160,_y+135)
qmind = QtBind.createLabel(gui_, "0",_x+269,_y+135)
lspirit = QtBind.createLabel(gui_, "SPIRIT STONE",_x+160,_y+150)
qspirit = QtBind.createLabel(gui_, "0",_x+269,_y+150)
ldodging2 = QtBind.createLabel(gui_, "DODGING STONE",_x+160,_y+165)
qdodging2 = QtBind.createLabel(gui_, "0",_x+269,_y+165)
lCIZGI = QtBind.createLabel(gui_, "----------------------------------", _x+160,_y+175)
lMG = QtBind.createLabel(gui_, "| ELIXIR | ", _x+195,_y+185 )
lWeapon = QtBind.createLabel(gui_, "WEAPON", _x+160,_y+200)
lProtector = QtBind.createLabel(gui_, "PROTECTOR", _x+160,_y+215)
lAccessory = QtBind.createLabel(gui_, "ACCESSORY", _x+160,_y+230)
lShield = QtBind.createLabel(gui_, "SHIELD", _x+160,_y+245)
qweapon = QtBind.createLabel(gui_, "0",_x+269,_y+200)
qprotector = QtBind.createLabel(gui_, "0",_x+269,_y+215)
qaccessory = QtBind.createLabel(gui_, "0",_x+269,_y+230)
qshield = QtBind.createLabel(gui_, "0",_x+269,_y+245)
ButtonArea6 = QtBind.createList(gui_, _x+300, _y, _x+160, _y+90)
lMG = QtBind.createLabel(gui_, "| COIN | ", _x+360,_y+1 )
lGoldC = QtBind.createLabel(gui_, "GOLD COIN", _x+305, _y+15)
lSilverC = QtBind.createLabel(gui_, "SILVER COIN", _x+305, _y+30)
lCopperC = QtBind.createLabel(gui_, "COPPER COIN", _x+305, _y+45)
lIronC = QtBind.createLabel(gui_, "IRON COIN", _x+305, _y+60)
lArenaC = QtBind.createLabel(gui_, "ARENA COIN", _x+305, _y+75)
qgold = QtBind.createLabel(gui_, "0", _x+429, _y+15)
qsilver = QtBind.createLabel(gui_, "0",_x+429,_y+30)
qcopper = QtBind.createLabel(gui_, "0",_x+429,_y+45)
qiron = QtBind.createLabel(gui_, "0",_x+429,_y+60)
qarena = QtBind.createLabel(gui_, "0",_x+429,_y+75)
lblDegree = QtBind.createLabel(gui_,"DEGREE ITEMLERI GOSTER..",_x+504,_y+15)
tbxDegree = QtBind.createLineEdit(gui_, "", _x+480,_y+15, 20, 15)
btnStorage = QtBind.createButton(gui_, "btnStorage_clicked", "       STORAGE        ", _x+535, _y+61)
btnGuildStorage = QtBind.createButton(gui_, "btnGuildStorage_clicked", "  GUILD STORAGE  ", _x+535, _y+84)
btnInventory = QtBind.createButton(gui_, "btnInventory_clicked", "      ENVANTER       ", _x+535, _y+38)
ButtonArea7 = QtBind.createList(gui_, _x+300, _y+105, 230, 100)
lblplayer = QtBind.createLabel(gui_, "MAIN CHAR :", _x+305, _y+110)
tbxplayer = QtBind.createLineEdit(gui_, "", _x+385, _y+110, 80, 18) 
lblparola = QtBind.createLabel(gui_, "SIFRE :", _x+305, _y+130) 
tbxparola = QtBind.createLineEdit(gui_, "", _x+385, _y+130, 80, 18) 
#SAVE / LOAD BUTON
btnSaveConfig = QtBind.createButton(gui_,'btnSaveConfig_clicked',"  KAYDET  ",_x+305,_y+155)
btnLoadConfig = QtBind.createButton(gui_,'btnLoadConfig_clicked',"  YUKLE  ",_x+390,_y+155)
lblProfil = QtBind.createLabel(gui_,"CONFIG PROFIL ISMI :",_x+305,_y+182)
tbxProfil = QtBind.createLineEdit(gui_,"",_x+415,_y+179,110,19)
lblinfo = QtBind.createLabel(gui_, "UltimateItemManager:\n * GAUCHE TARAFINDAN DUZENLENMISTIR. \n * FEEDBACK SISTEMLI BIR YAZILIMDIR. \n * HATA VE ONERI BILDIRIMLERINIZI BANA ULASTIRABILIRSINIZ.", _x+305,_y+205)
# ______________________________ MOTHODLAR ______________________________ #
def getPath():
    return get_config_dir()+pName+"\\"
def getConfig(name):
    if not name:
        name = pName;
    return getPath()+name+".json"
def loadDefaultConfig():
    # DATAYI TEMÝZLE
    QtBind.setText(gui_,tbxProfil,"")
    QtBind.setText(gui_,tbxplayer,"")
    QtBind.setText(gui_,tbxparola,"")
    QtBind.setText(gui_,tbxDegree,"")
def loadConfigs(fileName=""):
    loadDefaultConfig()
    if os.path.exists(getConfig(fileName)):
        data = {}
        with open(getConfig(fileName),"r") as f:
            data = json.load(f)
        QtBind.setText(gui_,tbxProfil,fileName)
        if "PLAYER" in data:
            QtBind.setText(gui_,tbxplayer,data["PLAYER"])
        if "PAROLA" in data:
            QtBind.setText(gui_,tbxparola,data["PAROLA"])
        if "DEGREE" in data:
            QtBind.setText(gui_,tbxDegree,data["DEGREE"])
        return True
    return False
def saveConfigs(fileName=""):
    data = {}
    data["PLAYER"] = QtBind.text(gui_,tbxplayer)
    data["PAROLA"] = QtBind.text(gui_,tbxparola)
    data["DEGREE"] = QtBind.text(gui_,tbxDegree)
    with open(getConfig(fileName),"w") as f:
        f.write(json.dumps(data,indent=4,sort_keys=True))
def btnSaveConfig_clicked():
    strConfigName = QtBind.text(gui_,tbxProfil)
    saveConfigs(strConfigName)
    if strConfigName:
        log('Plugin: ['+strConfigName+'] PROFILI KAYIT EDILDI.')
    else:
        log("Plugin: KAYIT EDILDI..")
def btnLoadConfig_clicked():
    strConfigName = QtBind.text(gui_,tbxProfil)
    if loadConfigs(strConfigName):
        if strConfigName:
            log("Plugin: ["+strConfigName+"] PROFILI YUKLENDI.")
        else:
            log("Plugin: YUKLENDI..")
    elif strConfigName:
        log("Plugin: ["+strConfigName+"] PROFILI BULUNAMADI.")

def btnStorage_clicked():
    countItems("Storage")
def btnGuildStorage_clicked():
    countItems("GuildStorage")
def btnInventory_clicked():
    countItems("Inventory")

def handle_chat(t,player,msg):
    if player == str(QtBind.text(gui_, tbxplayer)):
        #Elixir
        if msg =="sElixir" :
            sElixir()
        elif msg == "iElixir" :
            iElixir()
        elif msg == "gElixir" :
            gElixir()
        #Coin
        elif msg =="sCoin" :
            sCoin()
        elif msg == "iCoin" :
            iCoin()
        elif msg == "gCoin" :
            gCoin()
        #Stone
        elif msg == "iStone":
            iStone()
        elif msg == "sStone":
            sStone()
        elif msg == "gStone":
            gStone()
        else:
            phBotChat.Private(player, "ELIXIR-COIN-STONE KODLARININ BASINA s, i, g KOYARAK YOLLAYIN.ORN: sElixir")
            sleep(1.0)
            phBotChat.Private(player,"s : STORAGE  i : ENVANTER , g : GUILD STORAGE")
    else:
        if msg == (str(QtBind.text(gui_, tbxparola))):
            player = str(QtBind.text(gui_, tbxplayer))
            phBotChat.Private(player, "--------Storage-------")
            sleep(1.0)
            sElixir()
            sleep(1.0)
            sCoin()
            sleep(1.0)
            sStone()
            sleep(1.0)
            phBotChat.Private(player,"--------Inventory--------")
            sleep(1.0)
            iElixir()
            sleep(1.0)
            iCoin()
            sleep(1.0)
            iStone()
            sleep(1.0)
            phBotChat.Private(player,"---------Guild Storage-------")
            sleep(1.0)
            gElixir()
            sleep(1.0)
            gCoin()
            sleep(1.0)
            gStone()
            log("SIFRE DOGRULANARAK VERILER MAIN CHARA GONDERILDI..")
        else:
            pass

def ElixirChat():
    player = str(QtBind.text(gui_, tbxplayer))
    if str(QtBind.text(gui_, qweapon)) != "0" :
        phBotChat.Private(player, "Weapon : " + str(QtBind.text(gui_, qweapon)))
        sleep(1.0)
    if str(QtBind.text(gui_, qprotector)) != "0" :
        phBotChat.Private(player, "Protector : " + str(QtBind.text(gui_, qprotector)))
        sleep(1.0)
    if str(QtBind.text(gui_, qshield)) != "0" :
        phBotChat.Private(player, "Shield : " + str(QtBind.text(gui_, qshield)))
        sleep(1.0)
    if str(QtBind.text(gui_, qaccessory)) != "0" :
        phBotChat.Private(player, "Accessory : " + str(QtBind.text(gui_, qaccessory)))
    else:
        phBotChat.Private(player,"ELIXIR BULUNAMADI..")
    log("ELIXIR SAYISI GONDERILDI..")

def sElixir():
    btnStorage_clicked()
    ElixirChat()
def iElixir():
    btnInventory_clicked()
    ElixirChat()
def gElixir():
    btnGuildStorage_clicked()
    ElixirChat()

def CoinChat():
    player = str(QtBind.text(gui_, tbxplayer))
    if str(QtBind.text(gui_, qgold)) != "0" :
        phBotChat.Private(player, "Gold Coin : " + str(QtBind.text(gui_, qgold)))
        sleep(1.0)
    if str(QtBind.text(gui_, qiron)) != "0":
        phBotChat.Private(player, "Iron Coin : " + str(QtBind.text(gui_, qiron)))
        sleep(1.0)
    if str(QtBind.text(gui_, qsilver)) != "0" :
       phBotChat.Private(player, "Silver Coin : " + str(QtBind.text(gui_, qsilver)))
       sleep(1.0)
    if str(QtBind.text(gui_, qcopper)) != "0":
        phBotChat.Private(player, "Copper Coin : " + str(QtBind.text(gui_, qcopper)))
        sleep(1.0)
    if str(QtBind.text(gui_, qarena)) != "0":
        phBotChat.Private(player, "Arena Coin : " + str(QtBind.text(gui_, qarena)))
    else:
        phBotChat.Private(player,"COIN BULUNAMADI..")
    log("COIN SAYISI GONDERILDI..")

def sCoin():
    btnStorage_clicked()
    CoinChat()
def iCoin():
    btnInventory_clicked()
    CoinChat()
def gCoin():
    btnGuildStorage_clicked()
    CoinChat()

def StoneChat():
    player = str(QtBind.text(gui_, tbxplayer))
    if str(QtBind.text(gui_, qhp)) != "0":
        phBotChat.Private(player, "STR Stone : " + str(QtBind.text(gui_, qhp)))
    if str(QtBind.text(gui_, qmp)) != "0":
        phBotChat.Private(player, "INT Stone : " + str(QtBind.text(gui_, qmp)))
    if str(QtBind.text(gui_, qluck)) != "0":
        phBotChat.Private(player, "Luck Stone : " + str(QtBind.text(gui_, qluck)))
    if str(QtBind.text(gui_, qsteady)) != "0":
        phBotChat.Private(player, "Luck Stone : " + str(QtBind.text(gui_, qsteady)))
    if str(QtBind.text(gui_, qimmortal)) != "0":
        phBotChat.Private(player, "Immortal Stone : " + str(QtBind.text(gui_, qimmortal)))
    if str(QtBind.text(gui_, qmaster)) != "0":
        phBotChat.Private(player, "Master Stone : " + str(QtBind.text(gui_, qmaster)))
    if str(QtBind.text(gui_, qstamina)) != "0":
        phBotChat.Private(player, "Stamina Stone : " + str(QtBind.text(gui_, qstamina)))
    if str(QtBind.text(gui_, qmagic)) != "0":
        phBotChat.Private(player, "Magic Stone : " + str(QtBind.text(gui_, qmagic)))
    if str(QtBind.text(gui_, qstrikes)) != "0":
        phBotChat.Private(player, "Strikes Stone : " + str(QtBind.text(gui_, qstrikes)))
    if str(QtBind.text(gui_, qdiscipline)) != "0":
        phBotChat.Private(player, "Discipline Stone : " + str(QtBind.text(gui_, qdiscipline)))
    if str(QtBind.text(gui_, qpenetration)) != "0":
        phBotChat.Private(player, "Penetration Stone : " + str(QtBind.text(gui_, qpenetration)))
    if str(QtBind.text(gui_, qdodging)) != "0":
        phBotChat.Private(player, "Dodging Stone : " + str(QtBind.text(gui_, qdodging)))
    if str(QtBind.text(gui_, qfogs)) != "0":
        phBotChat.Private(player, "Fogs Stone : " + str(QtBind.text(gui_, qfogs)))
    if str(QtBind.text(gui_, qair)) != "0":
        phBotChat.Private(player, "Air Stone : " + str(QtBind.text(gui_, qair)))
    if str(QtBind.text(gui_, qfire)) != "0":
        phBotChat.Private(player, "Fire Stone : " + str(QtBind.text(gui_, qfire)))
    if str(QtBind.text(gui_, qimmunity)) != "0":
        phBotChat.Private(player, "Immunity Stone : " + str(QtBind.text(gui_, qimmunity)))
    if str(QtBind.text(gui_, qrevival)) != "0":
        phBotChat.Private(player, "Revival Stone : " + str(QtBind.text(gui_, qrevival)))        
    if str(QtBind.text(gui_, qcourage)) != "0":
        phBotChat.Private(player, "Courage Stone : " + str(QtBind.text(gui_, qcourage)))
    if str(QtBind.text(gui_, qwarriors)) != "0":
        phBotChat.Private(player, "Warriors Stone : " + str(QtBind.text(gui_, qwarriors)))
    if str(QtBind.text(gui_, qphilosophy)) != "0":
        phBotChat.Private(player, "Philosophy Stone : " + str(QtBind.text(gui_, qphilosophy)))
    if str(QtBind.text(gui_, qmeditation)) != "0":
        phBotChat.Private(player, "Meditation Stone : " + str(QtBind.text(gui_, qmeditation)))
    if str(QtBind.text(gui_, qchallenge)) != "0":
        phBotChat.Private(player, "Challenge Stone : " + str(QtBind.text(gui_, qchallenge)))
    if str(QtBind.text(gui_, qfocus)) != "0":
        phBotChat.Private(player, "Focus Stone : " + str(QtBind.text(gui_, qfocus)))
    if str(QtBind.text(gui_, qflesh)) != "0":
        phBotChat.Private(player, "Flesh Stone : " + str(QtBind.text(gui_, qflesh)))
    if str(QtBind.text(gui_, qlife)) != "0":
        phBotChat.Private(player, "Life Stone : " + str(QtBind.text(gui_, qlife)))
    if str(QtBind.text(gui_, qmind)) != "0":
        phBotChat.Private(player, "Mind Stone : " + str(QtBind.text(gui_, qmind)))
    if str(QtBind.text(gui_, qspirit)) != "0":
        phBotChat.Private(player, "Spirit Stone : " + str(QtBind.text(gui_, qspirit)))
    if str(QtBind.text(gui_, qdodging2)) != "0":
        phBotChat.Private(player, "ATT Dodging Stone : " + str(QtBind.text(gui_, qdodging2)))
    else:
        phBotChat.Private(player,"STONE BULUNAMADI..")
    log("STONE SAYISI GONDERILDI")
def iStone():
    btnInventory_clicked()
    StoneChat()
def sStone():
    btnStorage_clicked()
    StoneChat()
def gStone():
    btnGuildStorage_clicked()
    StoneChat()
                
def countItems(countIn):
    weapon = 0
    protector = 0
    accessory = 0
    shield = 0
    gold = 0
    silver = 0
    copper = 0
    iron = 0
    arena =0
    luck = 0
    steady = 0
    immortal = 0
    master = 0
    stamina = 0
    magic = 0
    strikes = 0
    discipline = 0
    penetration = 0
    dodging = 0
    fogs = 0
    air = 0
    fire = 0
    immunity = 0
    revival = 0
    courage = 0
    warriors = 0
    philosophy = 0
    meditation = 0
    challenge = 0
    focus = 0
    flesh = 0
    life = 0
    mind = 0
    spirit = 0
    dodging2 = 0
    MAGIC_STONE_OF_INT = 0
    MAGIC_STONE_OF_STR = 0
    
    items = []
    if countIn == "Storage":
        items = get_storage()["items"]
    elif countIn == "GuildStorage":
        items = get_guild_storage()["items"]
    elif countIn == "Inventory":
        items = get_inventory()["items"]
    degree = str(QtBind.text(gui_, tbxDegree))
    if items != []:
        for item in items:
            if item != None and "Intensifing" in item["name"] and "(weapon)" in item["name"]:
                weapon += item["quantity"]
            if item != None and "Intensifing" in item["name"] and "(protector)" in item["name"]:
                protector += item["quantity"]
            if item != None and "Intensifing" in item["name"] and "(accessory)" in item["name"]:
                accessory += item["quantity"]
            if item != None and "Intensifing" in item["name"] and "(Shield)" in item["name"]:
                shield += item["quantity"]
            if item != None and "Coin" in item["name"] and "Gold" in item["name"]:
                gold += item["quantity"]
            if item != None and "Coin" in item["name"] and "Silver" in item["name"]:
                silver += item["quantity"]
            if item != None and "Coin" in item["name"] and "Copper" in item["name"]:
                copper += item["quantity"]
            if item != None and "Coin" in item["name"] and "Iron" in item["name"]:
                iron += item["quantity"]
            if item != None and "Coin" in item["name"] and "Arena" in item["name"]:
                arena += item["quantity"]
            if item != None and degree in item["name"] and "tablet" not in item["name"] and 'stone' in item["name"]:
                if "steady" in item["name"]:
                    steady += item["quantity"]
                elif "luck" in item["name"]:
                    luck += item["quantity"]
                elif "immortal" in item["name"]:
                    immortal += item["quantity"]  
                elif "Magic stone of Str" in item["name"]:
                    MAGIC_STONE_OF_STR += item["quantity"]
                elif "Magic stone of Int" in item["name"]:
                    MAGIC_STONE_OF_INT += item["quantity"]
                elif "master" in item["name"]:
                    master += item["quantity"]
                elif "stamina" in item["name"]:
                    stamina += item["quantity"]
                elif "magic" in item["name"]:
                    magic += item["quantity"]
                elif "strikes" in item["name"]:
                    strikes += item["quantity"]
                elif "discipline" in item["name"]:
                    discipline += item["quantity"]
                elif "penetration" in item["name"]:
                    penetration += item["quantity"]
                elif "dodging" in item["name"]:
                    dodging += item["quantity"]
                elif "fogs" in item["name"]:
                    fogs += item["quantity"]
                elif "air" in item["name"]:
                    air += item["quantity"]
                elif "fire" in item["name"]:
                    fire += item["quantity"]
                elif "immunity" in item["name"]:
                    immunity += item["quantity"]
                elif "revival" in item["name"]:
                    revival += item["quantity"]                    
                elif "courage" in item["name"]:
                    courage += item["quantity"]
                elif "warriors" in item["name"]:
                    warriors += item["quantity"]
                elif "philosophy" in item["name"]:
                    philosophy += item["quantity"]
                elif "meditation" in item["name"]:
                    meditation += item["quantity"]
                elif "challenge" in item["name"]:
                    challenge += item["quantity"]
                elif "focus" in item["name"]:
                    focus += item["quantity"]
                elif "flest" in item["name"]:
                    flesh += item["quantity"]
                elif "life" in item["name"]:
                    life += item["quantity"]
                elif "mind" in item["name"]:
                    mind += item["quantity"]
                elif "spirit" in item["name"]:
                    spirit += item["quantity"]
                elif "attribute stone of dodging" in item["name"]:
                    dodging2 += item["quantity"]
    QtBind.setText(gui_, qweapon, str(weapon))
    QtBind.setText(gui_, qprotector, str(protector))
    QtBind.setText(gui_, qaccessory, str(accessory))
    QtBind.setText(gui_, qshield, str(shield))
    QtBind.setText(gui_, qgold, str(gold))
    QtBind.setText(gui_, qsilver, str(silver))
    QtBind.setText(gui_, qcopper, str(copper))
    QtBind.setText(gui_, qiron, str(iron))
    QtBind.setText(gui_, qarena, str(arena))
    QtBind.setText(gui_, qluck, str(luck))
    QtBind.setText(gui_, qsteady, str(steady))
    QtBind.setText(gui_, qimmortal, str(immortal))
    QtBind.setText(gui_, qhp, str(MAGIC_STONE_OF_STR))
    QtBind.setText(gui_, qmp, str(MAGIC_STONE_OF_INT))
    QtBind.setText(gui_, qmaster, str(master))
    QtBind.setText(gui_, qstamina, str(stamina))
    QtBind.setText(gui_, qmagic, str(magic))
    QtBind.setText(gui_, qstrikes, str(strikes))
    QtBind.setText(gui_, qdiscipline, str(discipline))
    QtBind.setText(gui_, qpenetration, str(penetration))
    QtBind.setText(gui_, qdodging, str(dodging))
    QtBind.setText(gui_, qfogs, str(fogs))
    QtBind.setText(gui_, qair, str(air))
    QtBind.setText(gui_, qfire, str(fire))
    QtBind.setText(gui_, qimmunity, str(immunity))
    QtBind.setText(gui_, qrevival, str(revival))
    QtBind.setText(gui_, qcourage, str(courage))
    QtBind.setText(gui_, qwarriors, str(warriors))
    QtBind.setText(gui_, qphilosophy, str(philosophy))
    QtBind.setText(gui_, qmeditation, str(meditation))
    QtBind.setText(gui_, qchallenge, str(challenge))
    QtBind.setText(gui_, qfocus, str(focus))
    QtBind.setText(gui_, qflesh, str(flesh))
    QtBind.setText(gui_, qlife, str(life))
    QtBind.setText(gui_, qmind, str(mind))
    QtBind.setText(gui_, qspirit, str(spirit))
    QtBind.setText(gui_, qdodging2, str(dodging2))

log('Plugin: '+pName+' v'+pVersion+' BASARIYLA YUKLENDI')

#CONFIG DOSYALARINI KONTROL ET
if os.path.exists(getPath()):
    useDefaultConfig = True 
    bot_args = get_command_line_args()
    if bot_args:
        for i in range(len(bot_args)):
            param = bot_args[i].lower()
            if param.startswith('-UltimateItemManager-config='):
                configName = param[17:]
                if loadConfigs(configName):
                    log("Plugin: "+pName+" PROFIL ["+configName+"] KOMUT ILE YIKLENDI.")
                    useDefaultConfig = False
                else:
                    log("Plugin: "+pName+" PROFIL ["+configName+"] BULUNAMADI.")
                break
    if useDefaultConfig:
        loadConfigs()
else:
    loadDefaultConfig()
    os.makedirs(getPath())
    log('Plugin: "'+pName+'" CONFIG KLASORU OLUSTURULDU..')
