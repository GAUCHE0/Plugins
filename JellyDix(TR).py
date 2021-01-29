from phBot import *
import QtBind
from datetime import datetime
from threading import Timer
import urllib.request
import urllib.parse
import struct
import json
import time
import os
import re

pName = 'JellyDix(TR)'
pVersion = '0.0.1'
pUrl = 'https://raw.githubusercontent.com/GAUCHE0/Plugins/main/JellyDix(TR).py'

# ______________________________ KURULUM ______________________________ #

URL_HOST = "https://jellydix.ddns.net" # API server
URL_REQUEST_TIMEOUT = 15 # SANIYE
DISCORD_FETCH_DELAY = 5000 # MILI SANIYE
# KURESELLER
character_data = None
party_data = None
chat_data = {}
isOnline = False
hasStall = False
discord_fetch_counter = 0
discord_chat_handlers = []
# GUI
gui = QtBind.init(__name__,pName)
QtBind.createLabel(gui,"DISCORD KANAL ID :",6,10)
tbxChannels = QtBind.createLineEdit(gui,"",6,25,80,19)
lstChannels = QtBind.createList(gui,6,46,156,90)
btnAddChannel = QtBind.createButton(gui,'btnAddChannel_clicked',"   EKLE   ",86,25)
btnRemChannel = QtBind.createButton(gui,'btnRemChannel_clicked',"     SIL     ",45,135)
# DC SECENEKLERI
QtBind.createLabel(gui,"TOKEN:",6,165)
tbxToken = QtBind.createLineEdit(gui,"",43,163,119,19)
cbxAddTimestamp = QtBind.createCheckBox(gui,'cbxDoNothing','PHBOT SAATI EKLE',6,185)
cbxDiscord_interactions = QtBind.createCheckBox(gui,'cbxDoNothing','DC ETKILESIMLERINI KULLAN',6,205)
tbxDiscord_guild_id = QtBind.createLineEdit(gui,'',6,225,145,19)
cbxDiscord_check_all = QtBind.createCheckBox(gui,'cbxDoNothing','ETKILESIMLERI KONTROL ET',6,245)
# AYIRICI CIZGI
QtBind.createLineEdit(gui,"",169,10,1,262)
# TETIKLEYICI
QtBind.createLabel(gui,"BILDIRIM GONDERMEK ICIN DISCORD KANAL KODOUNU GIRIN..",175,10)
btnSaveConfig = QtBind.createButton(gui,'saveConfigs',"    DEGISIKLIKLERI KAYDET     ",560,4)
# GUI HIZLI DUZENLEMESI ICIN KOORDINAT TANIMLAMASI
_x = 180
_y = 30
_Height = 19
_cmbxWidth = 131
_tbxWidth = 118
# LOGIN ISTATISTIKLERI
QtBind.createLabel(gui,'OYUNA GIRDI',_x+_cmbxWidth+4,_y+3)
cmbxEvtChar_joined = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui,'DC VERDI',_x+_cmbxWidth+4,_y+3)
cmbxEvtChar_disconnected = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20
# UNIQUELER
_y += 5
QtBind.createLabel(gui,'UNIQUE SPAWN',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_uniqueSpawn = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20
cbxEvtMessage_uniqueSpawn_filter = QtBind.createCheckBox(gui,'cbxDoNothing','',_x,_y+3)
tbxEvtMessage_uniqueSpawn_filter = QtBind.createLineEdit(gui,"",_x+13,_y,_tbxWidth,_Height)
_y+=20
QtBind.createLabel(gui,'UNIQUE KESILDI',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_uniqueKilled = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20
cbxEvtMessage_uniqueKilled_filter = QtBind.createCheckBox(gui,'cbxDoNothing','',_x,_y+3)
tbxEvtMessage_uniqueKilled_filter = QtBind.createLineEdit(gui,"",_x+13,_y,_tbxWidth,_Height)
_y+=20
# ETKINLIKLER
_y += 5
QtBind.createLabel(gui,'CAPTURE THE FLAG',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_ctf = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui,'BATTLE ARENA',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_battlearena = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui,'FTW',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_fortress = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui,'CONSIGNMENT HUNTER',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_consignmenthunter = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui,'CONSIGNMENT THIEF',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_consignmentthief = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
# UYARILAR
_x += _cmbxWidth * 2 + 10
_y = 30
QtBind.createLabel(gui,'GM YANINDA',_x+_cmbxWidth+4,_y+3)
cmbxEvtNear_gm = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui,'UNIQUE YANINDA',_x+_cmbxWidth+4,_y+3)
cmbxEvtNear_unique = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui,'HUNTER/TRADER YANINDA',_x+_cmbxWidth+4,_y+3)
cmbxEvtNear_hunter = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui,'THIEF YANINDA',_x+_cmbxWidth+4,_y+3)
cmbxEvtNear_thief = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui,'SALDIRI GELDI',_x+_cmbxWidth+4,_y+3)
cmbxEvtChar_attacked = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui,'CHAR OLDU ',_x+_cmbxWidth+4,_y+3)
cmbxEvtChar_died = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui,'TRANSPORT OLDU',_x+_cmbxWidth+4,_y+3)
cmbxEvtPet_died = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20
# DIGER
_y+=5
QtBind.createLabel(gui,'GOREV TAMAMLANDI',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_quest = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui,'SIMYA TAMAMLANDI',_x+_cmbxWidth+4,_y+3)
cmbxEvtBot_alchemy = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui,'STALLDAN ITEM SATILDI',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_item_sold = QtBind.createCombobox(gui,_x,_y,_cmbxWidth,_Height)
_y+=20
# YINELEMEK ICIN KAYDIR
cmbxTriggers={'cmbxEvtChar_joined':cmbxEvtChar_joined,'cmbxEvtChar_disconnected':cmbxEvtChar_disconnected,'cmbxEvtMessage_uniqueSpawn':cmbxEvtMessage_uniqueSpawn,'cmbxEvtMessage_uniqueKilled':cmbxEvtMessage_uniqueKilled,'cmbxEvtMessage_ctf':cmbxEvtMessage_ctf,'cmbxEvtMessage_battlearena':cmbxEvtMessage_battlearena,'cmbxEvtMessage_fortress':cmbxEvtMessage_fortress,'cmbxEvtMessage_consignmenthunter':cmbxEvtMessage_consignmenthunter,'cmbxEvtMessage_consignmentthief':cmbxEvtMessage_consignmentthief,'cmbxEvtNear_gm':cmbxEvtNear_gm,'cmbxEvtNear_unique':cmbxEvtNear_unique,'cmbxEvtNear_hunter':cmbxEvtNear_hunter,'cmbxEvtNear_thief':cmbxEvtNear_thief,'cmbxEvtChar_attacked':cmbxEvtChar_attacked,'cmbxEvtChar_died':cmbxEvtChar_died,'cmbxEvtPet_died':cmbxEvtPet_died,'cmbxEvtMessage_quest':cmbxEvtMessage_quest,'cmbxEvtBot_alchemy':cmbxEvtBot_alchemy,'cmbxEvtMessage_item_sold':cmbxEvtMessage_item_sold}
# GUI (+)
gui_ = QtBind.init(__name__,pName+"(+)")
# KOORDINAT TEMELLERI
_x = 6
_y = 7
_cmbxWidth = 131
_tbxWidth = 118
# CHAT MESAJLARI
QtBind.createLabel(gui_,'GENEL CHAT',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_all = QtBind.createCombobox(gui_,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui_,'OZEL CHAT',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_private = QtBind.createCombobox(gui_,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui_,'STALL CHAT',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_stall = QtBind.createCombobox(gui_,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui_,'PT CHAT',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_party = QtBind.createCombobox(gui_,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui_,'AKADEMI CHAT',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_academy = QtBind.createCombobox(gui_,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui_,'GUILD CHAT',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_guild = QtBind.createCombobox(gui_,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui_,'UNION CHAT',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_union = QtBind.createCombobox(gui_,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui_,'GLOBAL CHAT',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_global = QtBind.createCombobox(gui_,_x,_y,_cmbxWidth,_Height)
_y+=20
cbxEvtMessage_global_filter = QtBind.createCheckBox(gui_,'cbxDoNothing','',_x,_y+3)
tbxEvtMessage_global_filter = QtBind.createLineEdit(gui_,"",_x+13,_y,_tbxWidth,_Height)
_y+=20
QtBind.createLabel(gui_,'NOTICE',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_notice = QtBind.createCombobox(gui_,_x,_y,_cmbxWidth,_Height)
_y+=20
cbxEvtMessage_notice_filter = QtBind.createCheckBox(gui_,'cbxDoNothing','',_x,_y+3)
tbxEvtMessage_notice_filter = QtBind.createLineEdit(gui_,"",_x+13,_y,_tbxWidth,_Height)
_y+=20
QtBind.createLabel(gui_,'GM CHAT',_x+_cmbxWidth+4,_y+3)
cmbxEvtMessage_gm = QtBind.createCombobox(gui_,_x,_y,_cmbxWidth,_Height)
# PT
_x += int(_cmbxWidth*1.5) 
_y = 7
QtBind.createLabel(gui_,'PT KATILDI',_x+_cmbxWidth+19,_y+3)
cmbxEvtParty_joined = QtBind.createCombobox(gui_,_x+15,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui_,'PT AYRILDI',_x+_cmbxWidth+19,_y+3)
cmbxEvtParty_left = QtBind.createCombobox(gui_,_x+15,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui_,'PT UYESI KATILDI',_x+_cmbxWidth+19,_y+3)
cmbxEvtParty_memberJoin = QtBind.createCombobox(gui_,_x+15,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui_,'PT UYESI AYRILDI',_x+_cmbxWidth+19,_y+3)
cmbxEvtParty_memberLeft = QtBind.createCombobox(gui_,_x+15,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui_,'PT UYESI LVL ATLADI',_x+_cmbxWidth+19,_y+3)
cmbxEvtParty_memberLvlUp = QtBind.createCombobox(gui_,_x+15,_y,_cmbxWidth,_Height)
_y+=20
# GUILD
_y+=5
QtBind.createLabel(gui_,'GUILD NOTU DEGISTI',_x+_cmbxWidth+19,_y+3)
cmbxEvtGuild_noticechanged = QtBind.createCombobox(gui_,_x+15,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui_,'GUILD UYESI OYUNA GIRDI',_x+_cmbxWidth+19,_y+3)
cmbxEvtGuild_memberLogin = QtBind.createCombobox(gui_,_x+15,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui_,'GUILD UYESI OYUNDAN CIKTI',_x+_cmbxWidth+19,_y+3)
cmbxEvtGuild_memberLogout = QtBind.createCombobox(gui_,_x+15,_y,_cmbxWidth,_Height)
_y+=20
# TOPLAMALAR
_x += _cmbxWidth * 2 + 10
_y = 7
QtBind.createLabel(gui_,'ITEM TOPLANDI(vSRO)',_x+_cmbxWidth+4,_y+3)
cmbxEvtPick_item = QtBind.createCombobox(gui_,_x,_y,_cmbxWidth,_Height)
_y+=20
cbxEvtPick_name_filter = QtBind.createCheckBox(gui_,'cbxDoNothing','',_x,_y+3)
tbxEvtPick_name_filter = QtBind.createLineEdit(gui_,"",_x+13,_y,_tbxWidth,_Height)
_y+=20
cbxEvtPick_servername_filter = QtBind.createCheckBox(gui_,'cbxDoNothing','',_x,_y+3)
tbxEvtPick_servername_filter = QtBind.createLineEdit(gui_,"",_x+13,_y,_tbxWidth,_Height)
_y+=20
QtBind.createLabel(gui_,'ITEM (SOX) TOPLANDI',_x+_cmbxWidth+4,_y+3)
cmbxEvtPick_rare = QtBind.createCombobox(gui_,_x,_y,_cmbxWidth,_Height)
_y+=20
QtBind.createLabel(gui_,'GIYILEBILIR ITEM\nTOPLANDI',_x+_cmbxWidth+4,_y+3)
cmbxEvtPick_equip = QtBind.createCombobox(gui_,_x,_y+6,_cmbxWidth,_Height)
_y+=20
#INFO
lblinfo = QtBind.createLabel(gui_,"JellyDix (TR):\n * GAUCHE TARAFINDAN DUZENLENMISTIR. \n  * HATA VE ONERI BILDIRIMLERINIZI BANA ULASTIRABILIRSINIZ.\n   # DISCORD: |GAUCHE#8710| \n   # E-MAIL: |can.berk.cetin@hotmail.com.tr|",220,190)
# YINELEMEK ICIN KAYDIR
cmbxTriggers_={'cmbxEvtMessage_all':cmbxEvtMessage_all,'cmbxEvtMessage_private':cmbxEvtMessage_private,'cmbxEvtMessage_stall':cmbxEvtMessage_stall,'cmbxEvtMessage_party':cmbxEvtMessage_party,'cmbxEvtMessage_academy':cmbxEvtMessage_academy,'cmbxEvtMessage_guild':cmbxEvtMessage_guild,'cmbxEvtMessage_union':cmbxEvtMessage_union,'cmbxEvtMessage_global':cmbxEvtMessage_global,'cmbxEvtMessage_notice':cmbxEvtMessage_notice,'cmbxEvtMessage_gm':cmbxEvtMessage_gm,'cmbxEvtParty_joined':cmbxEvtParty_joined,'cmbxEvtParty_left':cmbxEvtParty_left,'cmbxEvtParty_memberJoin':cmbxEvtParty_memberJoin,'cmbxEvtParty_memberLeft':cmbxEvtParty_memberLeft,'cmbxEvtParty_memberLvlUp':cmbxEvtParty_memberLvlUp,'cmbxEvtGuild_noticechanged':cmbxEvtGuild_noticechanged,'cmbxEvtGuild_memberLogin':cmbxEvtGuild_memberLogin,'cmbxEvtGuild_memberLogout':cmbxEvtGuild_memberLogout,'cmbxEvtPick_item':cmbxEvtPick_item,'cmbxEvtPick_rare':cmbxEvtPick_rare,'cmbxEvtPick_equip':cmbxEvtPick_equip}
# ______________________________ METHODLAR ______________________________ #
# DOSYA YOLUNDAN DEVAM ET
def getPath():
	return get_config_dir()+pName+"\\"
# CHAR CONFIG YOLUNDAN DEVAM ET (JSON)
def getConfig():
	return getPath()+character_data['server'] + "_" + character_data['name'] + ".json"
# VARSAYILAN CONFIG YUKLE
def loadDefaultConfig():
	QtBind.setText(gui,tbxChannels,"")
	QtBind.clear(gui,lstChannels)
	QtBind.setChecked(gui,cbxAddTimestamp,False)
	QtBind.setChecked(gui,cbxDiscord_interactions,False)
	QtBind.setText(gui,tbxDiscord_guild_id," DISCORD SUNUCU ID...")
	QtBind.setChecked(gui,cbxDiscord_check_all,False)
	QtBind.setText(gui,tbxToken,'')
	for name,cmbx in cmbxTriggers.items():
		QtBind.clear(gui,cmbx)
		QtBind.append(gui,cmbx,"")
	QtBind.setChecked(gui,cbxEvtMessage_uniqueSpawn_filter,False)
	QtBind.setText(gui,tbxEvtMessage_uniqueSpawn_filter,"ISIM FILITRELE")
	QtBind.setChecked(gui,cbxEvtMessage_uniqueKilled_filter,False)
	QtBind.setText(gui,tbxEvtMessage_uniqueKilled_filter,"ISIM FILITRELE")
	for name,cmbx in cmbxTriggers_.items():
		QtBind.clear(gui_,cmbx)
		QtBind.append(gui_,cmbx,"")
	QtBind.setChecked(gui_,cbxEvtMessage_global_filter,False)
	QtBind.setText(gui_,tbxEvtMessage_global_filter,"ISIM FILITRELE")
	QtBind.setChecked(gui_,cbxEvtMessage_notice_filter,False)
	QtBind.setText(gui_,tbxEvtMessage_notice_filter,"MESAJ FILITRELE")

	QtBind.setChecked(gui_,cbxEvtPick_name_filter,False)
	QtBind.setText(gui_,tbxEvtPick_name_filter,"ISIM FILITRELE")
	QtBind.setChecked(gui_,cbxEvtPick_servername_filter,False)
	QtBind.setText(gui_,tbxEvtPick_servername_filter,"SV ISIM FILITRELE")
# TUM CONFIGI KAYDET
def saveConfigs():
	if isJoined():
		data = {}
		data["Channels"] = QtBind.getItems(gui,lstChannels)
		data["AddTimeStamp"] = QtBind.isChecked(gui,cbxAddTimestamp)
		data["DiscordInteractions"] = QtBind.isChecked(gui,cbxDiscord_interactions)
		data["DiscordInteractionGuildID"] = QtBind.text(gui,tbxDiscord_guild_id)
		data["DiscordInteractionCheckAll"] = QtBind.isChecked(gui,cbxDiscord_check_all)
		data["Token"] = QtBind.text(gui,tbxToken)
		triggers = {}
		data["Triggers"] = triggers
		for name,cmbx in cmbxTriggers.items():
			triggers[name] = QtBind.text(gui,cmbx)
		triggers["cbxEvtMessage_uniqueSpawn_filter"] = QtBind.isChecked(gui,cbxEvtMessage_uniqueSpawn_filter)
		triggers["tbxEvtMessage_uniqueSpawn_filter"] = QtBind.text(gui,tbxEvtMessage_uniqueSpawn_filter)
		triggers["cbxEvtMessage_uniqueKilled_filter"] = QtBind.isChecked(gui,cbxEvtMessage_uniqueKilled_filter)
		triggers["tbxEvtMessage_uniqueKilled_filter"] = QtBind.text(gui,tbxEvtMessage_uniqueKilled_filter)
		for name,cmbx in cmbxTriggers_.items():
			triggers[name] = QtBind.text(gui_,cmbx)
		triggers["cbxEvtMessage_global_filter"] = QtBind.isChecked(gui_,cbxEvtMessage_global_filter)
		triggers["tbxEvtMessage_global_filter"] = QtBind.text(gui_,tbxEvtMessage_global_filter)
		triggers["cbxEvtMessage_notice_filter"] = QtBind.isChecked(gui_,cbxEvtMessage_notice_filter)
		triggers["tbxEvtMessage_notice_filter"] = QtBind.text(gui_,tbxEvtMessage_notice_filter)
		triggers["cbxEvtPick_name_filter"] = QtBind.isChecked(gui_,cbxEvtPick_name_filter)
		triggers["tbxEvtPick_name_filter"] = QtBind.text(gui_,tbxEvtPick_name_filter)
		triggers["cbxEvtPick_servername_filter"] = QtBind.isChecked(gui_,cbxEvtPick_servername_filter)
		triggers["tbxEvtPick_servername_filter"] = QtBind.text(gui_,tbxEvtPick_servername_filter)
		with open(getConfig(),"w") as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))
		log("Plugin: "+pName+" CONFIG KAYIT EDILDI..")
# KAYIT EDILEN CONFIGI YUKLE
def loadConfigs():
	loadDefaultConfig()
	if isJoined():
		global isOnline
		isOnline = True
		if os.path.exists(getConfig()):
			data = {}
			with open(getConfig(),"r") as f:
				data = json.load(f)
			if "Channels" in data:
				for channel_id in data["Channels"]:
					QtBind.append(gui,lstChannels,channel_id)
					for name,cmbx in cmbxTriggers.items():
						QtBind.append(gui,cmbx,channel_id)
					for name,cmbx in cmbxTriggers_.items():
						QtBind.append(gui_,cmbx,channel_id)
			if "AddTimeStamp" in data and data["AddTimeStamp"]:
				QtBind.setChecked(gui,cbxAddTimestamp,True)
			if "DiscordInteractions" in data and data["DiscordInteractions"]:
				QtBind.setChecked(gui,cbxDiscord_interactions,True)
			if "DiscordInteractionGuildID" in data and data["DiscordInteractionGuildID"]:
				QtBind.setText(gui,tbxDiscord_guild_id,data["DiscordInteractionGuildID"])
			if "DiscordInteractionCheckAll" in data and data["DiscordInteractionCheckAll"]:
				QtBind.setChecked(gui,cbxDiscord_check_all,True)
			if "Token" in data:
				QtBind.setText(gui,tbxToken,data["Token"])
			if "Triggers" in data:
				triggers = data["Triggers"]
				if "cmbxEvtChar_joined" in triggers:
					QtBind.setText(gui,cmbxEvtChar_joined,triggers["cmbxEvtChar_joined"])
				if "cmbxEvtChar_disconnected" in triggers:
					QtBind.setText(gui,cmbxEvtChar_disconnected,triggers["cmbxEvtChar_disconnected"])
				if "cmbxEvtMessage_uniqueSpawn" in triggers:
					QtBind.setText(gui,cmbxEvtMessage_uniqueSpawn,triggers["cmbxEvtMessage_uniqueSpawn"])
				if "cbxEvtMessage_uniqueSpawn_filter" in triggers and triggers["cbxEvtMessage_uniqueSpawn_filter"]:
					QtBind.setChecked(gui,cbxEvtMessage_uniqueSpawn_filter,True)
				if "tbxEvtMessage_uniqueSpawn_filter" in triggers and triggers["tbxEvtMessage_uniqueSpawn_filter"]:
					QtBind.setText(gui,tbxEvtMessage_uniqueSpawn_filter,triggers["tbxEvtMessage_uniqueSpawn_filter"])
				if "cmbxEvtMessage_uniqueKilled" in triggers:
					QtBind.setText(gui,cmbxEvtMessage_uniqueKilled,triggers["cmbxEvtMessage_uniqueKilled"])
				if "cbxEvtMessage_uniqueKilled_filter" in triggers and triggers["cbxEvtMessage_uniqueKilled_filter"]:
					QtBind.setChecked(gui,cbxEvtMessage_uniqueKilled_filter,True)
				if "tbxEvtMessage_uniqueKilled_filter" in triggers and triggers["tbxEvtMessage_uniqueKilled_filter"]:
					QtBind.setText(gui,tbxEvtMessage_uniqueKilled_filter,triggers["tbxEvtMessage_uniqueKilled_filter"])
				if "cmbxEvtMessage_battlearena" in triggers:
					QtBind.setText(gui,cmbxEvtMessage_battlearena,triggers["cmbxEvtMessage_battlearena"])
				if "cmbxEvtMessage_ctf" in triggers:
					QtBind.setText(gui,cmbxEvtMessage_ctf,triggers["cmbxEvtMessage_ctf"])
				if "cmbxEvtMessage_fortress" in triggers:
					QtBind.setText(gui,cmbxEvtMessage_fortress,triggers["cmbxEvtMessage_fortress"])
				if "cmbxEvtMessage_consignmenthunter" in triggers:
					QtBind.setText(gui,cmbxEvtMessage_consignmenthunter,triggers["cmbxEvtMessage_consignmenthunter"])
				if "cmbxEvtMessage_consignmentthief" in triggers:
					QtBind.setText(gui,cmbxEvtMessage_consignmentthief,triggers["cmbxEvtMessage_consignmentthief"])
				if "cmbxEvtNear_gm" in triggers:
					QtBind.setText(gui,cmbxEvtNear_gm,triggers["cmbxEvtNear_gm"])
				if "cmbxEvtNear_unique" in triggers:
					QtBind.setText(gui,cmbxEvtNear_unique,triggers["cmbxEvtNear_unique"])
				if "cmbxEvtNear_hunter" in triggers:
					QtBind.setText(gui,cmbxEvtNear_hunter,triggers["cmbxEvtNear_hunter"])
				if "cmbxEvtNear_thief" in triggers:
					QtBind.setText(gui,cmbxEvtNear_thief,triggers["cmbxEvtNear_thief"])
				if "cmbxEvtChar_attacked" in triggers:
					QtBind.setText(gui,cmbxEvtChar_attacked,triggers["cmbxEvtChar_attacked"])
				if "cmbxEvtChar_died" in triggers:
					QtBind.setText(gui,cmbxEvtChar_died,triggers["cmbxEvtChar_died"])
				if "cmbxEvtPet_died" in triggers:
					QtBind.setText(gui,cmbxEvtPet_died,triggers["cmbxEvtPet_died"])
				if "cmbxEvtMessage_quest" in triggers:
					QtBind.setText(gui,cmbxEvtMessage_quest,triggers["cmbxEvtMessage_quest"])
				if "cmbxEvtBot_alchemy" in triggers:
					QtBind.setText(gui,cmbxEvtBot_alchemy,triggers["cmbxEvtBot_alchemy"])
				if "cmbxEvtMessage_item_sold" in triggers:
					QtBind.setText(gui,cmbxEvtMessage_item_sold,triggers["cmbxEvtMessage_item_sold"])
				# (+)
				if "cmbxEvtMessage_all" in triggers:
					QtBind.setText(gui_,cmbxEvtMessage_all,triggers["cmbxEvtMessage_all"])
				if "cmbxEvtMessage_private" in triggers:
					QtBind.setText(gui_,cmbxEvtMessage_private,triggers["cmbxEvtMessage_private"])
				if "cmbxEvtMessage_stall" in triggers:
					QtBind.setText(gui_,cmbxEvtMessage_stall,triggers["cmbxEvtMessage_stall"])
				if "cmbxEvtMessage_party" in triggers:
					QtBind.setText(gui_,cmbxEvtMessage_party,triggers["cmbxEvtMessage_party"])
				if "cmbxEvtMessage_academy" in triggers:
					QtBind.setText(gui_,cmbxEvtMessage_academy,triggers["cmbxEvtMessage_academy"])
				if "cmbxEvtMessage_guild" in triggers:
					QtBind.setText(gui_,cmbxEvtMessage_guild,triggers["cmbxEvtMessage_guild"])
				if "cmbxEvtMessage_union" in triggers:
					QtBind.setText(gui_,cmbxEvtMessage_union,triggers["cmbxEvtMessage_union"])
				if "cmbxEvtMessage_global" in triggers:
					QtBind.setText(gui_,cmbxEvtMessage_global,triggers["cmbxEvtMessage_global"])
				if "cbxEvtMessage_global_filter" in triggers and triggers["cbxEvtMessage_global_filter"]:
					QtBind.setChecked(gui_,cbxEvtMessage_global_filter,True)
				if "tbxEvtMessage_global_filter" in triggers and triggers["tbxEvtMessage_global_filter"]:
					QtBind.setText(gui_,tbxEvtMessage_global_filter,triggers["tbxEvtMessage_global_filter"])
				if "cmbxEvtMessage_notice" in triggers:
					QtBind.setText(gui_,cmbxEvtMessage_notice,triggers["cmbxEvtMessage_notice"])
				if "cbxEvtMessage_notice_filter" in triggers and triggers["cbxEvtMessage_notice_filter"]:
					QtBind.setChecked(gui_,cbxEvtMessage_notice_filter,True)
				if "tbxEvtMessage_notice_filter" in triggers and triggers["tbxEvtMessage_notice_filter"]:
					QtBind.setText(gui_,tbxEvtMessage_notice_filter,triggers["tbxEvtMessage_notice_filter"])
				if "cmbxEvtMessage_gm" in triggers:
					QtBind.setText(gui_,cmbxEvtMessage_gm,triggers["cmbxEvtMessage_gm"])
				if "cmbxEvtParty_joined" in triggers:
					QtBind.setText(gui_,cmbxEvtParty_joined,triggers["cmbxEvtParty_joined"])
				if "cmbxEvtParty_left" in triggers:
					QtBind.setText(gui_,cmbxEvtParty_left,triggers["cmbxEvtParty_left"])
				if "cmbxEvtParty_memberJoin" in triggers:
					QtBind.setText(gui_,cmbxEvtParty_memberJoin,triggers["cmbxEvtParty_memberJoin"])
				if "cmbxEvtParty_memberLeft" in triggers:
					QtBind.setText(gui_,cmbxEvtParty_memberLeft,triggers["cmbxEvtParty_memberLeft"])
				if "cmbxEvtParty_memberLvlUp" in triggers:
					QtBind.setText(gui_,cmbxEvtParty_memberLvlUp,triggers["cmbxEvtParty_memberLvlUp"])
				if "cmbxEvtGuild_noticechanged" in triggers:
					QtBind.setText(gui_,cmbxEvtGuild_noticechanged,triggers["cmbxEvtGuild_noticechanged"])
				if "cmbxEvtGuild_memberLogin" in triggers:
					QtBind.setText(gui_,cmbxEvtGuild_memberLogin,triggers["cmbxEvtGuild_memberLogin"])
				if "cmbxEvtGuild_memberLogout" in triggers:
					QtBind.setText(gui_,cmbxEvtGuild_memberLogout,triggers["cmbxEvtGuild_memberLogout"])
				if "cmbxEvtPick_item" in triggers:
					QtBind.setText(gui_,cmbxEvtPick_item,triggers["cmbxEvtPick_item"])
				if "cbxEvtPick_name_filter" in triggers and triggers["cbxEvtPick_name_filter"]:
					QtBind.setChecked(gui_,cbxEvtPick_name_filter,True)
				if "tbxEvtPick_name_filter" in triggers and triggers["tbxEvtPick_name_filter"]:
					QtBind.setText(gui_,tbxEvtPick_name_filter,triggers["tbxEvtPick_name_filter"])
				if "cbxEvtPick_servername_filter" in triggers and triggers["cbxEvtPick_servername_filter"]:
					QtBind.setChecked(gui_,cbxEvtPick_servername_filter,True)
				if "tbxEvtPick_servername_filter" in triggers and triggers["tbxEvtPick_servername_filter"]:
					QtBind.setText(gui_,tbxEvtPick_servername_filter,triggers["tbxEvtPick_servername_filter"])
				if "cmbxEvtPick_rare" in triggers:
					QtBind.setText(gui_,cmbxEvtPick_rare,triggers["cmbxEvtPick_rare"])
				if "cmbxEvtPick_equip" in triggers:
					QtBind.setText(gui_,cmbxEvtPick_equip,triggers["cmbxEvtPick_equip"])
# METIN MEVCUTSA TRUE DONDUR
def ListContains(list,text):
	text = text.lower()
	for i in range(len(list)):
		if list[i].lower() == text:
			return True
	return False
# DC KANAL YUKLEME
def btnAddChannel_clicked():
	if character_data:
		channel_id = QtBind.text(gui,tbxChannels)
		if not channel_id:
			return
		if channel_id.isnumeric():
			if not ListContains(QtBind.getItems(gui,lstChannels),channel_id):
				QtBind.append(gui,lstChannels,channel_id)
				for name,cmbx in cmbxTriggers.items():
					QtBind.append(gui,cmbx,channel_id)
				for name,cmbx in cmbxTriggers_.items():
					QtBind.append(gui_,cmbx,channel_id)
				QtBind.setText(gui,tbxChannels,"")
				log('Plugin: KANAL EKLENDI ['+channel_id+']')
		else:
			log('Plugin: HATA! DC KANAL ID RAKAM OLMAK ZORUNDA !')
# DC KANAL SILME
def btnRemChannel_clicked():
	if character_data:
		channelItem = QtBind.text(gui,lstChannels)
		if channelItem:
			for name,cmbx in cmbxTriggers.items():
				channelReset = False
				if QtBind.text(gui,cmbx) == channelItem:
					channelReset = True
				QtBind.remove(gui,cmbx,channelItem)
				if channelReset:
					QtBind.setText(gui,cmbx,"")
			for name,cmbx in cmbxTriggers_.items():
				channelReset = False
				if QtBind.text(gui_,cmbx) == channelItem:
					channelReset = True
				QtBind.remove(gui_,cmbx,channelItem)
				if channelReset:
					QtBind.setText(gui_,cmbx,"")
			QtBind.remove(gui,lstChannels,channelItem)
			log('Plugin: KANAL SILINDI ['+channelItem+']')
# BILDIRI GONDERMEK ICIN INFO PAKETI OLUSTUR
def CreateInfo(t,data):
	info = {}
	info["type"] = t
	info["data"] = data
	info["source"] = 'phBot'
	return info
def Notify(channel_id,message,info=None,colour=None):
	Timer(0.001,_Notify,(channel_id,message,info,colour)).start()

# DC KANALINA BILDIRIM GONDERME
def _Notify(channel_id,message,info,colour):
	if not channel_id or not message:
		return
	url = URL_HOST
	if not url:
		return
	token = QtBind.text(gui,tbxToken)
	try:
		# PHBOT SAATI GONDERME
		if QtBind.isChecked(gui,cbxAddTimestamp):
			message = "||"+datetime.now().strftime('%H:%M:%S')+"|| "+message
		data = {"token":token,"channel":channel_id,"message":message}
		if info:
			data['info'] = info
		if colour != None:
			data['colour'] = colour
		data = json.dumps(data).encode()
		if not url.endswith("/"):
			url += "/"
		req = urllib.request.Request(url+"api/notify",data=data,headers={'content-type':'application/json'})
		with urllib.request.urlopen(req,timeout=URL_REQUEST_TIMEOUT) as f:
			try:
				resp = json.loads(f.read().decode())
				if resp:
					if resp['success']:
						log("Plugin: DISCORDA BILDIRI GONDERILDI.")
					else:
						log("Plugin: DISCORDA BILDIRI GONDERILEMEDI : ["+resp['message']+"]")
			except Exception as ex2:
				log("Plugin: SUNUCUDAN OKUMA HATASI ["+str(ex2)+"]")
	except Exception as ex:
		log("Plugin: URL YUKLEME HATASI: ["+str(ex)+"] ")
def Fetch(guild_id):
	Timer(0.001,_Fetch,(guild_id,)).start()
def _Fetch(guild_id):
	if not guild_id or not guild_id.isnumeric():
		return
	url = URL_HOST
	if not url:
		return
	token = QtBind.text(gui,tbxToken)
	try:
		params = json.dumps({'guild':guild_id,'token':token,'charname':character_data['name'],'fetch_all':QtBind.isChecked(gui,cbxDiscord_check_all)}).encode()
		if not url.endswith("/"):
			url += "/"
		req = urllib.request.Request(url+"api/fetch",data=params,headers={'content-type': 'application/json'})
		with urllib.request.urlopen(req,timeout=URL_REQUEST_TIMEOUT) as f:
			try:
				resp = json.loads(f.read().decode())
				if resp:
					if resp['success']:
						on_discord_fetch(resp['data'])
					else:
						log("Plugin: GETIRME BASARISIZ ["+resp['message']+"]")
			except Exception as ex2:
				log("Plugin: SUNUCUDAN OKUMA HATASI ["+str(ex2)+"]")
	except Exception as ex:
		log("Plugin: URL YUKLEME HATASI: ["+str(ex)+"] ")
# CHAR OYUNDA MI KONTROL ET
def isJoined():
	global character_data
	character_data = get_character_data()
	if not (character_data and "name" in character_data and character_data["name"]):
		character_data = None
	return character_data
# BATTLE ARENA CESITLERI
def getBattleArenaText(t):
	if t == 0:
		return 'Random'
	if t == 1:
		return 'Party'
	if t == 2:
		return 'Guild'
	if t == 3:
		return 'Job'
	return 'Unknown['+str(t)+']'
# KALE CEISTLERI
def getFortressText(fw_id):
	if fw_id == 1:
		return "Jangan"
	if fw_id == 3:
		return "Hotan"
	if fw_id == 3:
		return "Constantinople"
	if fw_id == 6:
		return "Bandit"
	return 'Fortress (#'+str(fw_id)+')'
# PT LISTESINI DC FORMATINDA LISTELE
def getPartyTextList(party):
	if not party:
		return ''
	txt = '```\n'
	for joinId, member in party.items():
		txt += member['name'].ljust(13)
		txt += (' (Lvl.'+str(member['level'])+')').ljust(10)
		if member['guild']:
			txt += ' ['+member['guild']+']'
		txt += '\n'
	txt += '```'
	return txt
# GUILD LISTESINI DC FORMATINDA LISTELE
def getGuildTextList(guild):
	if not guild:
		return ''
	txt = '```\n'
	for memberID, member in guild.items():
		# name + padding
		txt += member['name'].ljust(13)
		# lvl. + padding
		txt += (' (Lvl.'+str(member['level'])+')').ljust(10)
		# online
		if member['online']:
			txt += ' - [On]'
		else:
			txt += ' - [Off]'
		txt += '\n'
	txt += '```'
	return txt
# MEVCUT GOLDU METIN HALINE GETIRMEK
def getGoldText():
	global character_data
	character_data = get_character_data()
	return "{:,}".format(character_data['gold'])
# IRK AYRISTIRMASI
def getRaceText(servername):
	if '_CH_' in servername:
		return '(CH)'
	if '_EU_' in servername:
		return '(EU)'
	return ''
# CINSIYET AYRISTIRMASI
def getGenreText(servername):
	if '_M_' in servername:
		return '[M]'
	if '_W_' in servername:
		return '[F]'
	return ''
# SOX AYRISTIRMASI
def getSoXText(servername,level):
	if level < 101:
		if servername.endswith('A_RARE'):
			return '^Star'
		elif servername.endswith('B_RARE'):
			return '^Moon'
		elif servername.endswith('C_RARE'):
			return '^Sun'
	else:
		if servername.endswith('A_RARE'):
			return '^Nova'
		elif servername.endswith('B_RARE'):
			return '^Rare'
		elif servername.endswith('C_RARE'):
			return '^Legend'
		elif servername.endswith('SET_A'):
			return '^Egy A'
		elif servername.endswith('SET_B'):
			return '^Egy B'
	return ''
# CHAT SISTEMI ICEREN TUM PLUGINLERI YUKLER
def GetChatHandlers():
	import importlib
	handlers = []
	plugin_name = os.path.basename(__file__)
	plugin_dir = os.path.dirname(__file__)
	for path in os.scandir(plugin_dir):
		if path.is_file() and path.name.endswith(".py") and path.name != plugin_name:
			try:
				plugin = importlib.import_module(path.name[:-3])
				if hasattr(plugin,'handle_chat'):
					handlers.append(getattr(plugin,'handle_chat'))
					log('Plugin: DISCORD ETKILESIMCISI BURADAN YUKLENDI : '+path.name)
			except Exception as ex:
				log('Plugin: PLUGIN YUKLEME HATASI : '+path.name+' '+str(ex))
	return handlers
def ParseItem(data,index):
	rentID = struct.unpack_from('<I', data, index)[0]
	index += 4 # Rent id
	# TO DO: Parse rentability stuffs
	index += 4 # UnkUInt01
	itemID = struct.unpack_from('<I', data, index)[0]
	index += 4 # Item ID
	itemData = get_item(itemID)
	# IsEquipable
	if itemData['tid1'] == 1:
		index += 1 # plus
		index += 8 # stats
		index += 4 # durability
		count = data[index]
		index += 1 # magic options
		for i in range(count):
			index += 4 # id
			index += 4 # value
		index += 1 # (1)
		count = data[index]
		index += 1 # sockets
		for i in range(count):
			index += 1 # slot
			index += 4 # id
			index += 4 # value
		index += 1 # (2)
		count = data[index]
		index += 1 # adv
		for i in range(count):
			index += 1 # slot
			index += 4 # id
			index += 4 # value
		index += 4 # UnkUint02
	# IsCOS
	elif itemData['tid1'] == 2:
		# IsPet
		if itemData['tid2'] == 1:
			state = data[index]
			index += 1 # state
			if state != 1:
				index += 4 # model
				index += 2 + struct.unpack_from('<H', data, index)[0] # name
				# NeedsTime
				if data['tid3'] == 2:
					index += 4 # endtime
				index += 1 # UnkByte01
		# IsTransform
		elif itemData['tid2'] == 2:
			index += 4 # model
		# IsCube?
		elif itemData['tid2'] == 3:
			index += 4 # quantity
	# IsETC
	elif itemData['tid1'] == 3:
		index += 2 # quantity
		# IsAlchemy
		if itemData['tid2'] == 11:
			# IsStone
			if itemData['tid3'] == 1 or itemData['tid3'] == 2:
				index += 1 # assimilation
		# IsCard
		elif itemData['tid2'] == 14 and itemData['tid3'] == 2:
			count = data[index]
			index += 1 # params
			for i in range(count):
				index += 4 # id
				index += 4 # value
	return index,itemData
# ______________________________ ETKINLIKLER ______________________________ #
# SCRIPT UZERINDEN BILDIRIM GONDEREBILIRSINIZ YONTEM :"JellyDix,Channel ID,Message"
def JellyDix(args):
	if len(args) >= 3:
		Notify(args[1],"|`"+character_data['name']+"`| - "+args[2])
	return 0
# CHAR OYUNA GIRDIGINDE CAGIR
def joined_game():
	loadConfigs()
	Notify(QtBind.text(gui,cmbxEvtChar_joined),"|`"+character_data['name']+"`| - OYUNA GIRDI.")
# CHAR DC YEDIGINDE CAGIR
def disconnected():
	global isOnline
	if isOnline:
		isOnline = False
		channel_id = QtBind.text(gui,cmbxEvtChar_disconnected)
		if channel_id:
			Notify(channel_id,"|`"+character_data['name']+"`| DC VERDI.")
#CHAT PAKET AYRISTIRMA
def handle_chat(t,player,msg):
	itemLink = re.search('([0-9]*)',msg)
	if itemLink:
		global chat_data
		links = itemLink.groups()
		for i in range(len(links)):
			uid = int(links[i])
			if uid in chat_data:
				item = chat_data[uid]
				race = getRaceText(item['servername'])
				genre = getGenreText(item['servername'])
				sox = getSoXText(item['servername'],item['level'])
				msg = msg.replace(''+links[i]+'','`< '+item['name']+(' '+race if race else '')+(' '+genre if genre else '')+(' '+sox if sox else '')+' >`')
			else:
				msg = msg.replace(''+links[i]+'','`< '+links[i]+' >`')
	# MESAJ CESIDINI KONTROL ET
	if t == 1:
		Notify(QtBind.text(gui_,cmbxEvtMessage_all),"|`"+character_data['name']+"`| - [**General**] from `"+player+"`: "+msg)
	elif t == 2:
		Notify(QtBind.text(gui_,cmbxEvtMessage_private),"|`"+character_data['name']+"`| - [**Private**] from `"+player+"`: "+msg)
	elif t == 9:
		Notify(QtBind.text(gui_,cmbxEvtMessage_stall),"|`"+character_data['name']+"`| - [**Stall**] from `"+player+"`: "+msg)
	elif t == 4:
		Notify(QtBind.text(gui_,cmbxEvtMessage_party),"|`"+character_data['name']+"`| - "+"[**Party**] `"+player+"`: "+msg)
	elif t == 16:
		Notify(QtBind.text(gui_,cmbxEvtMessage_academy),"|`"+character_data['name']+"`| - "+"[**Academy**] `"+player+"`: "+msg)
	elif t == 5:
		Notify(QtBind.text(gui_,cmbxEvtMessage_guild),"[**Guild**] `"+player+"`: "+msg)
	elif t == 11:
		Notify(QtBind.text(gui_,cmbxEvtMessage_union),"[**Union**] `"+player+"`: "+msg)
	elif t == 6:
		if QtBind.isChecked(gui_,cbxEvtMessage_global_filter):
			searchMessage = QtBind.text(gui_,tbxEvtMessage_global_filter)
			if searchMessage:
				try:
					if re.search(searchMessage,msg):
						Notify(QtBind.text(gui_,cmbxEvtMessage_global),"[**Global**] `"+player+"`: "+msg,colour=0xffeb3b)
				except Exception as ex:
					log("Plugin: REGEX HATASI ["+str(ex)+"]")
		else:
			Notify(QtBind.text(gui_,cmbxEvtMessage_global),"[**Global**] `"+player+"`: "+msg,colour=0xffeb3b)
	elif t == 7:
		if QtBind.isChecked(gui_,cbxEvtMessage_notice_filter):
			searchMessage = QtBind.text(gui_,tbxEvtMessage_notice_filter)
			if searchMessage:
				try:
					if re.search(searchMessage,msg):
						Notify(QtBind.text(gui_,cmbxEvtMessage_notice),"[**Notice**] : "+msg)
				except Exception as ex:
					log("Plugin: REGEX HATASI ["+str(ex)+"]")
		else:
			Notify(QtBind.text(gui_,cmbxEvtMessage_notice),"[**Notice**] : "+msg)
	elif t == 3:
		Notify(QtBind.text(gui_,cmbxEvtMessage_gm),"[**GameMaster**] `"+player+"`: "+msg)
# OZEL ETKINLIKLERI OLDUGUNDA CAGIR
def handle_event(t, data):
	if t == 9:
		Notify(QtBind.text(gui,cmbxEvtNear_gm),"|`"+character_data['name']+"`| - **GM** `"+data+"` YANINDA!",CreateInfo("position",get_position()))
	elif t == 0:
		Notify(QtBind.text(gui,cmbxEvtNear_unique),"|`"+character_data['name']+"`| - **"+data+"** UNIQUE YANINDA!",CreateInfo("position",get_position()))
	elif t == 1:
		Notify(QtBind.text(gui,cmbxEvtNear_hunter),"|`"+character_data['name']+"`| - **HUNTER / TRADER** `"+data+"` YANINDA!",CreateInfo("position",get_position()))
	elif t == 2:
		Notify(QtBind.text(gui,cmbxEvtNear_thief),"|`"+character_data['name']+"`| - **THIEF** `"+data+"` YANINDA!",CreateInfo("position",get_position()))
	elif t == 4:
		Notify(QtBind.text(gui,cmbxEvtChar_attacked),"|`"+character_data['name']+"`| - `"+data+"` SANA SALDIRDI!",colour=0xFF5722)
	elif t == 7:
		Notify(QtBind.text(gui,cmbxEvtChar_died),"|`"+character_data['name']+"`| - OLDUN",CreateInfo("position",get_position()))
	elif t == 3:
		pet = get_pets()[data]
		Notify(QtBind.text(gui,cmbxEvtPet_died),"|`"+character_data['name']+"`| - PET OLDU :`"+(pet['type'].title())+"`")
	elif t == 5:
		channel_id = QtBind.text(gui_,cmbxEvtPick_rare)
		if channel_id:
			item = get_item(int(data))
			race = getRaceText(item['servername'])
			genre = getGenreText(item['servername'])
			sox = getSoXText(item['servername'],item['level'])
			Notify(channel_id,"|`"+character_data['name']+"`| - **ITEM (SOX)** TOPLADIN! ***"+item['name']+(' '+race if race else '')+(' '+genre if genre else '')+(' '+sox if sox else '')+"***")
	elif t == 6:
		channel_id = QtBind.text(gui_,cmbxEvtPick_equip)
		if channel_id:
			item = get_item(int(data))
			race = getRaceText(item['servername'])
			genre = getGenreText(item['servername'])
			sox = getSoXText(item['servername'],item['level'])
			Notify(channel_id,"|`"+character_data['name']+"`| - **ITEM (GIYILEBILIR)** TOPLADIN! ***"+item['name']+(' '+race if race else '')+(' '+genre if genre else '')+(' '+sox if sox else '')+"***")
	elif t == 8:
		Notify(QtBind.text(gui,cmbxEvtBot_alchemy),"|`"+character_data['name']+"`| - *OTO SIMYA** TAMAMLANDI.")
def handle_joymax(opcode, data):
	global party_data,hasStall
	# SERVER_NOTICE_UPDATE
	if opcode == 0x300C:
		updateType = data[0]
		if updateType == 5:
			channel_id = QtBind.text(gui,cmbxEvtMessage_uniqueSpawn)
			if channel_id:
				modelID = struct.unpack_from("<I",data,2)[0]
				uniqueName = get_monster(int(modelID))['name']
				if QtBind.isChecked(gui,cbxEvtMessage_uniqueSpawn_filter):
					searchName = QtBind.text(gui,tbxEvtMessage_uniqueSpawn_filter)
					if searchName:
						try:
							if re.search(searchName,uniqueName):
								Notify(channel_id,"**"+uniqueName+"** CIKTI!",colour=0x9C27B0)
						except Exception as ex:
							log("Plugin: REGEX HATASI: ["+str(ex)+"]")
				else:
					Notify(channel_id,"**"+uniqueName+"** CIKTI!",colour=0x9C27B0)
		elif updateType == 6:
			channel_id = QtBind.text(gui,cmbxEvtMessage_uniqueKilled)
			if channel_id:
				modelID = struct.unpack_from("<I",data,2)[0]
				killerNameLength = struct.unpack_from('<H', data, 6)[0]
				killerName = struct.unpack_from('<' + str(killerNameLength) + 's', data, 8)[0].decode('cp1252')
				uniqueName = get_monster(int(modelID))['name']
				if QtBind.isChecked(gui,cbxEvtMessage_uniqueKilled_filter):
					searchName = QtBind.text(gui,tbxEvtMessage_uniqueKilled_filter)
					if searchName:
						try:
							if re.search(searchName,uniqueName):
								Notify(channel_id,"**"+uniqueName+"** `"+killerName+"` TARAFINDAN OLDURULDU.",colour=0x9C27B0)
						except Exception as ex:
							log("Plugin: Error at regex ["+str(ex)+"]")
				else:
					Notify(channel_id,"**"+uniqueName+"** `"+killerName+"`TARAFINDAN OLDURULDU.",colour=0x9C27B0)
		elif updateType == 29:
			eventType = data[2]
			if eventType == 1:
				channel_id = QtBind.text(gui,cmbxEvtMessage_consignmenthunter)
				if channel_id:
					progressType = data[3]
					if progressType == 0:
						Notify(channel_id,"[**Consignment**] HUNTER CONSIGNMENT 10 DAKIKA ICINDE BASLAYACAK")
					elif progressType == 1:
						Notify(channel_id,"[**Consignment**] HUNTER CONSIGNMENT BASLADI")
					elif progressType == 2:
						Notify(channel_id,"[**Consignment**] HUNTER CONSIGNMENT SONLANDI.")
			elif eventType == 2:
				channel_id = QtBind.text(gui,cmbxEvtMessage_consignmentthief)
				if channel_id:
					progressType = data[3]
					if progressType == 0:
						Notify(channel_id,"[**Consignment**] THIEF CONSIGNMENT 10 DAKIKA ICINDE BASLAYACAK")
					elif progressType == 1:
						Notify(channel_id,"[**Consignment**] THIEF CONSIGNMENT BASLADI")
					elif progressType == 2:
						Notify(channel_id,"[**Consignment**] THIEF CONSIGNMENT SONLANDI.")
	# SERVER_BA_NOTICE
	elif opcode == 0x34D2:
		channel_id = QtBind.text(gui,cmbxEvtMessage_battlearena)
		if channel_id:
			updateType = data[0]
			if updateType == 2:
				Notify(channel_id,"[**Battle Arena**] ("+getBattleArenaText(data[1])+") 10 DAKIKA ICINDE BASLAYACAK.")
			elif updateType == 13:
				Notify(channel_id,"[**Battle Arena**] ("+getBattleArenaText(data[1])+") 5 DAKIKA ICINDE BASLAYACAK.")
			elif updateType == 14:
				Notify(channel_id,"[**Battle Arena**] ("+getBattleArenaText(data[1])+") 1 DAKIKA ICINDE BASLAYACAK.")
			elif updateType == 3:
				Notify(channel_id,"[**Battle Arena**] KATILIM SURESI SONLANDI")
			elif updateType == 4:
				Notify(channel_id,"[**Battle Arena**] BASLADI")
			elif updateType == 5:
				Notify(channel_id,"[**Battle Arena**] BITTI")
	# SERVER_CTF_NOTICE
	elif opcode == 0x34B1:
		channel_id = QtBind.text(gui,cmbxEvtMessage_ctf)
		if channel_id:
			updateType = data[0]
			if updateType == 2:
				Notify(channel_id,"[**Capture the Flag**] 10 DAKIKA ICINDE BASLAYACAK.")
			elif updateType == 13:
				Notify(channel_id,"[**Capture the Flag**] 5 DAKIKA ICINDE BASLAYACAK.")
			elif updateType == 14:
				Notify(channel_id,"[**Capture the Flag**] 1 DAKIKA ICINDE BASLAYACAK.")
			elif updateType == 3:
				Notify(channel_id,"[**Capture the Flag**] BASLADI")
			elif updateType == 9:
				Notify(channel_id,"[**Capture the Flag**] BITTI")
	# SERVER_QUEST_UPDATE
	elif opcode == 0x30D5:
		channel_id = QtBind.text(gui,cmbxEvtMessage_quest)
		if channel_id:
			# Quest update & Quest completed
			if data[0] == 2 and data[10] == 2:
				questID = struct.unpack_from("<I",data,1)[0]
				quest = get_quests()[questID]
				Notify(channel_id,"|`"+character_data['name']+"`| - **GOREV** TAMAMLANDI. ***"+quest['name']+"***")
	# SERVER_INVENTORY_ITEM_MOVEMENT
	elif opcode == 0xB034:
		# vSRO filter
		locale = get_locale()
		if locale == 22:
			channel_id = QtBind.text(gui_,cmbxEvtPick_item)
			if channel_id:
				# parse
				updateType = data[1]
				if updateType == 6: # Ground
					notify_pickup(channel_id,struct.unpack_from("<I",data,7)[0])
				elif updateType == 17: # Pet
					notify_pickup(channel_id,struct.unpack_from("<I",data,11)[0])
				elif updateType == 28: # Pet (Full/Quest)
					slotInventory = data[6]
					if slotInventory != 254:
						notify_pickup(channel_id,struct.unpack_from("<I",data,11)[0])
	# SERVER_FW_NOTICE
	elif opcode == 0x385F:
		channel_id = QtBind.text(gui,cmbxEvtMessage_fortress)
		if channel_id:
			updateType = data[0]
			if updateType == 1:
				Notify(channel_id,"[**Fortress War**] 30 DAKIKA ICINDE BASLAYACAK")
			elif updateType == 2:
				Notify(channel_id,"[**Fortress War**] BASLADI")
			elif updateType == 3:
				Notify(channel_id,"[**Fortress War**] 30 DAKIKA ICINDE BITECEK")
			elif updateType == 4:
				Notify(channel_id,"[**Fortress War**] 20 DAKIKA ICINDE BITECEK")
			elif updateType == 5:
				Notify(channel_id,"[**Fortress War**] 10 DAKIKA ICINDE BITECEK")
			elif updateType == 8:
				fortressID = struct.unpack_from("<I",data,1)[0]
				guildNameLength = struct.unpack_from("<H",data,5)[0]
				guildName = data[7:7+guildNameLength].decode('cp1252')
				Notify(channel_id,"[**Fortress War**] "+getFortressText(fortressID)+" `"+guildName+"` TARAFINDAN ALINDI..")
			elif updateType == 9:
				Notify(channel_id,"[**Fortress War**] 1 DAKIKA ICINDE BITECEK")
			elif updateType == 6:
				Notify(channel_id,"[**Fortress War**] BITTI")
	# SERVER_PARTY_DATA
	elif opcode == 0x3065:
		party_data = get_party()
		channel_id = QtBind.text(gui_,cmbxEvtParty_joined)
		if channel_id:
			Notify(channel_id,"|`"+character_data['name']+"`| PTYE KATILDIN\n"+getPartyTextList(party_data))
	# SERVER_PARTY_UPDATE
	elif opcode == 0x3864:
		updateType = data[0]
		if updateType == 1:
			Notify(QtBind.text(gui_,cmbxEvtParty_left),"|`"+character_data['name']+"`| PTDEN AYRILDIN!")
		elif updateType == 2:
			party_data = get_party()
			channel_id = QtBind.text(gui_,cmbxEvtParty_memberJoin)
			if channel_id:
				memberNameLength = struct.unpack_from('<H',data,6)[0]
				memberName = struct.unpack_from('<'+str(memberNameLength)+'s',data,8)[0].decode('cp1252')
				Notify(channel_id,"|`"+character_data['name']+"`| `"+memberName+"` PTYE KATILDI\n"+getPartyTextList(party_data))
		elif updateType == 3:
			joinID = struct.unpack_from("<I",data,1)[0]
			memberName = party_data[joinID]['name']
			party_data = get_party()
			if memberName == character_data['name']:
				Notify(QtBind.text(gui_,cmbxEvtParty_left),"|`"+character_data['name']+"`| PTDEN AYRILDI")
			else:
				channel_id = QtBind.text(gui_,cmbxEvtParty_memberLeft)
				if channel_id:
					Notify(channel_id,"|`"+character_data['name']+"`| `"+memberName+"` PTDEN AYRILDI\n"+getPartyTextList(party_data))
		elif updateType == 6: # update member
			if data[5] == 2: # level
				channel_id = QtBind.text(gui_,cmbxEvtParty_memberLvlUp)
				if channel_id:
					joinID = struct.unpack_from("<I",data,1)[0]
					newLevel = data[6]
					oldLevel = party_data[joinID]['level']
					party_data[joinID]['level'] = newLevel
					if oldLevel < newLevel:
						Notify(channel_id,"|`"+character_data['name']+"`| `"+party_data[joinID]['name']+"` LEVEL ATLADI.\n"+getPartyTextList(party_data))
	# SERVER_STALL_CREATE_RESPONSE
	elif opcode == 0xB0B1:
		if data[0] == 1:
			hasStall = True
	# SERVER_STALL_DESTROY_RESPONSE
	elif opcode == 0xB0B2:
		if data[0] == 1:
			hasStall = False
	# SERVER_STALL_ENTITY_ACTION
	elif opcode == 0x30B7:
		if data[0] == 3 and hasStall:
			channel_id = QtBind.text(gui,cmbxEvtMessage_item_sold)
			if channel_id:
				playerNameLength = struct.unpack_from('<H', data, 2)[0]
				playerName = struct.unpack_from('<' + str(playerNameLength) + 's', data, 4)[0].decode('cp1252')
				Notify(channel_id,"|`"+character_data['name']+"`| `"+playerName+"` STALLDAN ALISVERIS YAPTI.\n```ANLIK GOLD: "+getGoldText()+"```")
	# SERVER_CHAT_ITEM_DATA
	elif opcode == 0xB504:
		global chat_data
		index = 2
		for i in range(data[1]):
			uid = struct.unpack_from('<I', data, index)[0]
			index += 4 # Unique ID
			try:
				index, item = ParseItem(data,index)
				chat_data[uid] = item
			except Exception as ex:
				# Make easy log file for user
				with open(getPath()+"error.log","a") as f:
					f.write("["+str(ex)+"] Server: (Opcode) 0x" + '{:02X}'.format(opcode) + " (Data) "+ ("None" if not data else ' '.join('{:02X}'.format(x) for x in data))+'\r\n')
	# GUILD_INFO_UPDATE
	elif opcode == 0x38F5:
		updateType = data[0]
		if updateType == 6: # member update
			memberID = struct.unpack_from("<I",data,1)[0]
			infoType = data[5]
			if infoType == 2: # session
				if data[6]:
					channel_id = QtBind.text(gui_,cmbxEvtGuild_memberLogout)
					if channel_id:
						member = get_guild()[memberID]
						Notify(channel_id,"|`"+character_data['name']+"`| GUILD UYESI `"+member['name']+"` OYUNDAN CIKTI")
				else:
					channel_id = QtBind.text(gui_,cmbxEvtGuild_memberLogin)
					if channel_id:
						member = get_guild()[memberID]
						Notify(channel_id,"|`"+character_data['name']+"`|  GUILD UYESI `"+member['name']+"` OYUNA GIRDI")
		elif updateType == 5: # general info
			infoType = data[1]
			if infoType == 16: # notice changed
				channel_id = QtBind.text(gui_,cmbxEvtGuild_noticechanged)
				if channel_id:
					index = 2
					titleLength = struct.unpack_from('<H', data, index)[0]
					title = struct.unpack_from('<' + str(titleLength) + 's', data,index+2)[0].decode('cp1252')
					index+=2+titleLength
					textLength = struct.unpack_from('<H', data,index)[0]
					text = struct.unpack_from('<' + str(textLength) + 's', data, index+2)[0].decode('cp1252')
					Notify(channel_id,"|`"+character_data['name']+"`| GUILD NOTU GUNCELLENDI : **`"+title+"`**\n"+text)
	return True
# TOPLAMA ETKINLIKLERI OLDUGUNDA CAGIR
def notify_pickup(channel_id,itemID):
	item = get_item(itemID)
	usefilterName = QtBind.isChecked(gui_,cbxEvtPick_name_filter)
	usefilterServerName = QtBind.isChecked(gui_,cbxEvtPick_servername_filter)
	if not usefilterName and not usefilterServerName:
		race = getRaceText(item['servername'])
		genre = getGenreText(item['servername'])
		sox = getSoXText(item['servername'],item['level'])
		Notify(channel_id,"|`"+character_data['name']+"`| - **ITEM** TOPLANDI ***"+item['name']+(' '+race if race else '')+(' '+genre if genre else '')+(' '+sox if sox else '')+"***")
		return
	if usefilterName:
		searchName = QtBind.text(gui_,tbxEvtPick_name_filter)
		if searchName:
			try:
				if re.search(searchName,item['name']):
					# Filtered by Name
					race = getRaceText(item['servername'])
					genre = getGenreText(item['servername'])
					sox = getSoXText(item['servername'],item['level'])
					Notify(channel_id,"|`"+character_data['name']+"`| - **ITEM (FILITRELI)** TOPLANDI ***"+item['name']+(' '+race if race else '')+(' '+genre if genre else '')+(' '+sox if sox else '')+"***")
					return
			except Exception as ex:
				log("Plugin: REGEX HATASI (ISIM) ["+str(ex)+"]")
	if usefilterServerName:
		searchServername = QtBind.text(gui_,tbxEvtPick_servername_filter)
		if searchServername:
			try:
				if re.search(searchServername,item['servername']):
					# Filtered by server name
					race = getRaceText(item['servername'])
					genre = getGenreText(item['servername'])
					sox = getSoXText(item['servername'],item['level'])
					Notify(channel_id,"|`"+character_data['name']+"`| - **ITEM (FILITRELI)** TOPLANDI ***"+item['name']+(' '+race if race else '')+(' '+genre if genre else '')+(' '+sox if sox else '')+"***")
					return
			except Exception as ex:
				log("Plugin: REGEX HATASI (SV ISMI) ["+str(ex)+"]")

# 500MS DE BIR CAGIR
def event_loop():
	if character_data:
		global discord_fetch_counter
		discord_fetch_counter += 500
		if discord_fetch_counter >= DISCORD_FETCH_DELAY:
			discord_fetch_counter = 0
			if QtBind.isChecked(gui,cbxDiscord_interactions):
				Fetch(QtBind.text(gui,tbxDiscord_guild_id))

# DC FETCH GELDIKCE CAGIR
def on_discord_fetch(data):
	if not data:
		return
	fetched_at = time.strptime(str(data['fetched_at']), '%m/%d/%Y, %H:%M:%S')
	fetched_at = time.mktime(fetched_at)
	messages = data['messages']
	for message in messages:
		created_at = time.strptime(str(message['created_at']), '%m/%d/%Y, %H:%M:%S')
		created_at = time.mktime(created_at)
		seconds_difference = int(fetched_at-created_at)
		if seconds_difference <= 15:
			content = message['content']
			for handler in discord_chat_handlers:
				try:
					handler(100,'',content)
				except Exception as ex:
					pass
			on_discord_message(content,message['channel_id'])
# DCDAN ETKILESIM GONDERILDIKCE CAGIR
def on_discord_message(msg,channel_id):
	channel_id = str(channel_id)
	msgLower = msg.lower()
	if msgLower.startswith('get '):
		msgLower = msgLower[4:].rstrip()
		if msgLower == 'position':
			p = get_position()
			Notify(channel_id,'|`'+character_data['name']+'`| - GERCEK POZISYON : ( X:%.1f, Y:%.1f, Region:%d )'%(p['x'],p['y'],p['region']),CreateInfo('position',p))
		elif msgLower == 'party':
			party = get_party()
			if party:
				Notify(channel_id,'|`'+character_data['name']+'`| - PT UYELERIN : :\n'+getPartyTextList(party))
			else:
				Notify(channel_id,'|`'+character_data['name']+'`| - PT DE DEGILSIN!')
		elif msgLower == 'guild':
			guild = get_guild()
			if guild:
				Notify(channel_id,'|`'+character_data['name']+'`| - GUILD UYELERIN `'+character_data['guild']+'` are :\n'+getGuildTextList(guild))
			else:
				Notify(channel_id,'|`'+character_data['name']+'`| - GUILDDE DEGILSIN!')

# PLUGIN YUKLENDI
log('Plugin: '+pName+' v'+pVersion+' BASARIYLA YUKLENDI')
if os.path.exists(getPath()):
	loadConfigs()
else:
	# CONFIG DOSYASI OLUSTURULDU
	os.makedirs(getPath())
	log('Plugin: '+pName+' CONFIG KLASORU OLUSTURULDU.')

# DISCORD 
discord_chat_handlers = GetChatHandlers()
