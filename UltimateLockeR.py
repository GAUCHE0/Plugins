from phBot import *
import phBotChat
from threading import Timer
import struct
import time
import QtBind
import random
import json
import os
import subprocess

pName = 'UltimateLockeR'
pVersion = '0.0.1'
pUrl = "https://raw.githubusercontent.com/GAUCHE0/Plugins/main/UltimateLockeR.py"
gui = QtBind.init(__name__,pName)
lblPlugins2 = QtBind.createLabel(gui,"UltimateLockeR:\n * GAUCHE TARAFINDAN DUZENLENMISTIR. \n * FEEDBACK SISTEMLI BIR YAZILIMDIR. \n * HATA VE ONERI BILDIRIMLERINIZI BANA ULASTIRABILIRSINIZ.",11,31)
_x = 20
_y = 95
lblProfil = QtBind.createLabel(gui,"CONFIG PROFIL ISMI :",_x-15,_y)
tbxProfil = QtBind.createLineEdit(gui,"",_x+102,_y-3,110,19)
btnSaveConfig = QtBind.createButton(gui,'btnSaveConfig_clicked',"  KAYDET  ",_x+102+110+3,_y-5)
btnLoadConfig = QtBind.createButton(gui,'btnLoadConfig_clicked',"  YUKLE  ",_x+102+110+3+75,_y-5)
_y = 130
_x = 6
lblPTMaster = QtBind.createLabel(gui,"PARTI MASTER :",_x+10,_y)
tbxPTMaster = QtBind.createLineEdit(gui,"",113,_y-3,205,19)
lblAMaster = QtBind.createLabel(gui,"AKADEMI MASTER :",_x+10,_y+20)
tbxAMaster = QtBind.createLineEdit(gui,"",113,_y+17,205,19)
lblSoru = QtBind.createLabel(gui,"SORU :",_x+10,_y+40)
tbxSoru = QtBind.createLineEdit(gui,"",113,_y+37,205,19)
lblCevap = QtBind.createLabel(gui,"CEVAP :",_x+10,_y+60)
tbxCevap = QtBind.createLineEdit(gui,"",113,_y+57,205,19)
def getPath():
	return get_config_dir()+pName+"\\"
def getConfig(name):
	if not name:
		name = pName;
	return getPath()+name+".json"
def loadDefaultConfig():
	# Clear data
	QtBind.setText(gui,tbxProfil,"")
	QtBind.setText(gui,tbxPTMaster,"")
	QtBind.setText(gui,tbxAMaster,"")
	QtBind.setText(gui,tbxSoru,"")
	QtBind.setText(gui,tbxCevap,"")
def loadConfigs(fileName=""):
	loadDefaultConfig()
	if os.path.exists(getConfig(fileName)):
		data = {}
		with open(getConfig(fileName),"r") as f:
			data = json.load(f)
		QtBind.setText(gui,tbxProfil,fileName)
		if "PTMASTER" in data:
			QtBind.setText(gui,tbxPTMaster,data["PTMASTER"])
		if "AMASTER" in data:
			QtBind.setText(gui,tbxAMaster,data["AMASTER"])
		if "SORU" in data:
			QtBind.setText(gui,tbxSoru,data["SORU"])
		if "CEVAP" in data:
			QtBind.setText(gui,tbxCevap,data["CEVAP"])
		return True
	return False
def saveConfigs(fileName=""):
	data = {}
	data["PTMASTER"] = QtBind.text(gui,tbxPTMaster)
	data["AMASTER"] = QtBind.text(gui,tbxAMaster)
	data["SORU"] = QtBind.text(gui,tbxSoru)
	data["CEVAP"] = QtBind.text(gui,tbxCevap)
	with open(getConfig(fileName),"w") as f:
		f.write(json.dumps(data,indent=4,sort_keys=True))
def btnSaveConfig_clicked():
	strConfigName = QtBind.text(gui,tbxProfil)
	saveConfigs(strConfigName)
	if strConfigName:
		log('Plugin: ['+strConfigName+'] PROFILI KAYIT EDILDI.')
	else:
		log("Plugin: KAYIT EDILDI..")
def btnLoadConfig_clicked():
	strConfigName = QtBind.text(gui,tbxProfil)
	if loadConfigs(strConfigName):
		if strConfigName:
			log("Plugin: ["+strConfigName+"] PROFILI YUKLENDI.")
		else:
			log("Plugin: YUKLENDI..")
	elif strConfigName:
		log("Plugin: ["+strConfigName+"] PROFILI BULUNAMADI.")
questionPartyTime = None
questionPartyCharName = ""
questionPartyRID = 0
questionPartyJID = 0
questionAcademyTime = None
questionAcademyCharName = ""
questionAcademyRID = 0
questionAcademyJID = 0
# ______________________________ METHODLAR ______________________________ #
# PAKET ENJEKSIYON
def Inject_PartyMatchJoinResponse(requestID,joinID,response):
	p = struct.pack('I', requestID)
	p += struct.pack('I', joinID)
	p += struct.pack('B',1 if response else 0)
	inject_joymax(0x306E,p,False)
# PAKET ENJEKSIYON
def Inject_AcademyMatchJoinResponse(requestID,joinID,response):
	p = struct.pack('I', requestID)
	p += struct.pack('I', joinID)
	p += struct.pack('B',1 if response else 0)
	inject_joymax(0x347F,p,False)
# ______________________________ ETKINLIKLER ______________________________ #
def handle_joymax(opcode,data):
	# PT KATILIM GONDERDIGINDE
	if opcode == 0x706D and QtBind.text(gui,tbxCevap):
		try:
			# ISTEKLER YERINE GETIRILDIGINDE DATAYI KAYDET
			global questionPartyTime,questionPartyRID,questionPartyJID,questionPartyCharName
			questionPartyTime = time.time()
			index=0
			questionPartyRID = struct.unpack_from('<I',data,index)[0]
			index+=4
			questionPartyJID = struct.unpack_from('<I',data,index)[0]
			index+=22
			charLength = struct.unpack_from('<H',data,index)[0]
			index+=2
			questionPartyCharName = struct.unpack_from('<' + str(charLength) + 's',data,index)[0].decode('cp1252')
			# SIFREYI SORMAK ICIN SORU GONDERMEK
			phBotChat.Private(questionPartyCharName,QtBind.text(gui,tbxSoru))
		except:
			log("Plugin: AYRISTIRMA HATASI,BU SERVERDA KULLANILAMAZ..")
			log("DESTEK ICIN ILETISIME GECINIZ..")
			log("Data [" + ("None" if not data else ' '.join('{:02X}'.format(x) for x in data))+"] Locale ["+str(get_locale())+"]")
	# AKADEMI KATILIM GONDERDIGINDE
	elif opcode == 0x747E and QtBind.text(gui,tbxCevap):
		try:
			# ISTEKLER YERINE GETIRILDIGINDE DATAYI KAYDET
			global questionAcademyTime,questionAcademyRID,questionAcademyJID,questionAcademyCharName	
			questionAcademyTime = time.time()
			index=0
			questionAcademyRID = struct.unpack_from('<I',data,index)[0]
			index+=4
			questionAcademyJID = struct.unpack_from('<I',data,index)[0]
			index+=18
			charLength = struct.unpack_from('<H',data,index)[0]
			index+=2
			questionAcademyCharName = struct.unpack_from('<' + str(charLength) + 's',data,index)[0].decode('cp1252')
			# SIFREYI SORMAK ICIN SORU GONDERMEK
			phBotChat.Private(questionAcademyCharName,QtBind.text(gui,tbxSoru))
		except:
			log("Plugin: AYRISTIRMA HATASI,BU SERVERDA KULLANILAMAZ..")
			log("DESTEK ICIN ILETISIME GECINIZ..")
			log("Data [" + ("None" if not data else ' '.join('{:02X}'.format(x) for x in data))+"] Locale ["+str(get_locale())+"]")
	return True
# SORU CEVAPLAMA KOSULLARI
def handle_chat(t,charName,message):
	# OZEL MESAJ KONTROLU
	if t != 2:
		return
	# SIFRE KURULDUYSA DEVAM ET
	if not QtBind.text(gui,tbxCevap):
		return
	# SORULARI KONTROL ET
	if message == QtBind.text(gui,tbxSoru):
		# MASTER OLMAYANLARA CEVAP HAZIRLAMA
		if QtBind.text(gui,tbxPTMaster) == charName or QtBind.text(gui,tbxAMaster) == charName:
			phBotChat.Private(charName,QtBind.text(gui,tbxCevap))
		else:
			phBotChat.Private(charName,"UZGUNUM MASTER DEGILSIN..")
		return
	# CEVAPLARI KONTROL ET
	if charName == questionPartyCharName:
		# PT KATILIM BEKLEME SURESI
		now = time.time()
		if now - questionPartyTime < 10:
			# CEVAP KONTROLÜ
			if message == QtBind.text(gui,tbxCevap):
				log("Plugin: "+charName+" SIFRE ILE PT'YE GIRDI")
				Inject_PartyMatchJoinResponse(questionPartyRID,questionPartyJID,True)
			else:
				log("Plugin: "+charName+" YANLIS SIFRE,PT REDDEDILDI.")
				Inject_PartyMatchJoinResponse(questionPartyRID,questionPartyJID,False)
			return
	if charName == questionAcademyCharName:
		# AKADEMI KATILIM BEKLEME SURESI 
		now = time.time()
		if now - questionAcademyTime < 10:
			# CEVAP KONTROLÜ
			if message == QtBind.text(gui,tbxCevap):
				log("Plugin: "+charName+" SIFRE ILE AKADEMIYE GIRDI")
				Inject_AcademyMatchJoinResponse(questionAcademyRID,questionAcademyJID,True)
			else:
				log("Plugin: "+charName+" YANLIS SIFRE,AKADEMI REDDEDILDI.")
				Inject_AcademyMatchJoinResponse(questionAcademyRID,questionAcademyJID,False)
			return
# PLUGIN YUKLENDI MESAJI
log('Plugin: '+pName+' v'+pVersion+' BASARIYLA YUKLENDI.')
#CONFIG DOSYALARINI KONTROL ET
if os.path.exists(getPath()):
	useDefaultConfig = True 
	bot_args = get_command_line_args()
	if bot_args:
		for i in range(len(bot_args)):
			param = bot_args[i].lower()
			if param.startswith('-UltimateLockeR-config='):
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
