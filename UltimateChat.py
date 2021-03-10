from phBot import *
from time import localtime, strftime
import phBotChat
import QtBind
import json
import os

pName = 'UltimateChat'
pVersion = '0.0.4'
pUrl = "https://raw.githubusercontent.com/GAUCHE0/Plugins/main/UltimateChat.py"

# ______________________________ KURULUM ______________________________ #
# KURESELLER
MESSAGES_DELAY = 10000 # MS MESAJ TEKRARLAMA SURESI
message_delay_counter = 0
character_data = None
# Graphic user interface
gui__ = QtBind.init(__name__,pName)
cbxMsg = QtBind.createCheckBox(gui__, 'cbxMsg_clicked','MESAJ GONDER: ', 21, 13)
cbxMsg_checked = False
tbxMsg = QtBind.createLineEdit(gui__,"",125,12,480,18)
lblSpamCounter = QtBind.createLabel(gui__,"MESAJ SAYACI:",620,13)
lblCounter = QtBind.createLabel(gui__,"0",700,13)
lblLog = QtBind.createLabel(gui__,"UltimateChat:\n * GAUCHE TARAFINDAN DUZENLENMISTIR. \n * FEEDBACK SISTEMLI BIR YAZILIMDIR. \n * HATA VE ONERI BILDIRIMLERINIZI BANA ULASTIRABILIRSINIZ.",385,220)
cbxLogsInOne = QtBind.createCheckBox(gui__, 'cbxLog_clicked','MESAJLARI DOSYA OLARAK KAYDET.(log.txt)', 420, 45)
cbxLogAll = QtBind.createCheckBox(gui__,'cbxLog_clicked','GENEL',21,64)
cbxLogPrivate = QtBind.createCheckBox(gui__,'cbxLog_clicked','OZEL',21,83)
cbxLogParty = QtBind.createCheckBox(gui__,'cbxLog_clicked','PARTI',21,102)
cbxLogguild = QtBind.createCheckBox(gui__,'cbxLog_clicked','GUILD',21,121)
cbxLogUnion = QtBind.createCheckBox(gui__,'cbxLog_clicked','UNION',21,140)
cbxLogAcademy = QtBind.createCheckBox(gui__,'cbxLog_clicked','AKADEMI',21,159)
cbxLogStall = QtBind.createCheckBox(gui__,'cbxLog_clicked','STALL',21,178)
cbxLogGlobal = QtBind.createCheckBox(gui__,'cbxLog_clicked','GLOBAL',21,197)
cbxLogNotice = QtBind.createCheckBox(gui__,'cbxLog_clicked','NOTICE',21,216)
cbxLogGM = QtBind.createCheckBox(gui__,'cbxLog_clicked','GM',21,235)
cbxLogUnknown = QtBind.createCheckBox(gui__,'cbxLog_clicked','DIGER HEPSI',21, 254)
cbxEvtSpawn_unique = QtBind.createCheckBox(gui__,'cbxLog_clicked','UNIQUE CIKTIGINDA',321, 64)
cbxEvtSpawn_hunter = QtBind.createCheckBox(gui__,'cbxLog_clicked','HUNTER / TRADER GORULDUGUNDE',321,83)
cbxEvtSpawn_thief = QtBind.createCheckBox(gui__,'cbxLog_clicked','THIEF GORULDUGUNDE',321,102)
cbxEvtChar_attacked = QtBind.createCheckBox(gui__,'cbxLog_clicked','CHARA ATAK GELDIGINDE',321,121)
cbxEvtChar_died = QtBind.createCheckBox(gui__,'cbxLog_clicked','CHAR OLDUGUNDE',321,140)
cbxEvtPet_transport_died = QtBind.createCheckBox(gui__,'cbxLog_clicked','TRANSPORT PET OLDUGUNDE',321,159)
cbxEvtDrop_item = QtBind.createCheckBox(gui__,'cbxLog_clicked','ITEM DUSTUGUNDE',321,178)
cbxEvtDrop_rare = QtBind.createCheckBox(gui__,'cbxLog_clicked','SOX DUSTUGUNDE',321,197)
# ______________________________ METHODLAR ______________________________ #
# CONFIGDEN DEVAM ET
def getPath():
	return get_config_dir()+pName+"\\"
def getConfig():
	return getPath()+character_data["server"]+"_"+character_data["name"]+".json"
#VARSAYILAN CONFIG AYARLARI
def loadDefaultConfig():
	# Clear data
	QtBind.setChecked(gui__,cbxLogsInOne,False)
	QtBind.setChecked(gui__,cbxLogAll,False)
	QtBind.setChecked(gui__,cbxLogPrivate,False)
	QtBind.setChecked(gui__,cbxLogParty,False)
	QtBind.setChecked(gui__,cbxLogguild,False)
	QtBind.setChecked(gui__,cbxLogUnion,False)
	QtBind.setChecked(gui__,cbxLogStall,False)
	QtBind.setChecked(gui__,cbxLogGlobal,False)
	QtBind.setChecked(gui__,cbxLogNotice,False)
	QtBind.setChecked(gui__,cbxLogGM,False)
	QtBind.setChecked(gui__,cbxLogUnknown,False)
	QtBind.setChecked(gui__,cbxEvtSpawn_unique,False)
	QtBind.setChecked(gui__,cbxEvtSpawn_hunter,False)
	QtBind.setChecked(gui__,cbxEvtSpawn_thief,False)
	QtBind.setChecked(gui__,cbxEvtChar_attacked,False)
	QtBind.setChecked(gui__,cbxEvtChar_died,False)
	QtBind.setChecked(gui__,cbxEvtPet_transport_died,False)
	QtBind.setChecked(gui__,cbxEvtDrop_item,False)
	QtBind.setChecked(gui__,cbxEvtDrop_rare,False)
	QtBind.setText(gui__,tbxMsg,"")
# KAYIT EDILEN CONFIGDEN DEVAM ET
def loadConfigs():
	loadDefaultConfig()
	if isJoined():
		if os.path.exists(getConfig()):
			data = {}
			with open(getConfig(),"r") as f:
				data = json.load(f)
			# KAYITLI CONFIGI KONTROL ETME
			if "cbxLogsInOne" in data and data["cbxLogsInOne"]:
				QtBind.setChecked(gui__,cbxLogsInOne,data["cbxLogsInOne"])
			if "cbxLogAll" in data and data["cbxLogAll"]:
				QtBind.setChecked(gui__,cbxLogAll,data["cbxLogAll"])
			if "cbxLogPrivate" in data and data["cbxLogPrivate"]:
				QtBind.setChecked(gui__,cbxLogPrivate,data["cbxLogPrivate"])
			if "cbxLogParty" in data and data["cbxLogParty"]:
				QtBind.setChecked(gui__,cbxLogParty,data["cbxLogParty"])
			if "cbxLogguild" in data and data["cbxLogguild"]:
				QtBind.setChecked(gui__,cbxLogguild,data["cbxLogguild"])
			if "cbxLogUnion" in data and data["cbxLogUnion"]:
				QtBind.setChecked(gui__,cbxLogUnion,data["cbxLogUnion"])
			if "cbxLogAcademy" in data and data["cbxLogAcademy"]:
				QtBind.setChecked(gui__,cbxLogAcademy,data["cbxLogAcademy"])
			if "cbxLogStall" in data and data["cbxLogStall"]:
				QtBind.setChecked(gui__,cbxLogStall,data["cbxLogStall"])
			if "cbxLogGlobal" in data and data["cbxLogGlobal"]:
				QtBind.setChecked(gui__,cbxLogGlobal,data["cbxLogGlobal"])
			if "cbxLogNotice" in data and data["cbxLogNotice"]:
				QtBind.setChecked(gui__,cbxLogNotice,data["cbxLogNotice"])
			if "cbxLogGM" in data and data["cbxLogGM"]:
				QtBind.setChecked(gui__,cbxLogGM,data["cbxLogGM"])
			if "cbxLogUnknown" in data and data["cbxLogUnknown"]:
				QtBind.setChecked(gui__,cbxLogUnknown,data["cbxLogUnknown"])
			if "cbxEvtSpawn_unique" in data and data["cbxEvtSpawn_unique"]:
				QtBind.setChecked(gui__,cbxEvtSpawn_unique,data["cbxEvtSpawn_unique"])
			if "cbxEvtSpawn_hunter" in data and data["cbxEvtSpawn_hunter"]:
				QtBind.setChecked(gui__,cbxEvtSpawn_hunter,data["cbxEvtSpawn_hunter"])
			if "cbxEvtSpawn_thief" in data and data["cbxEvtSpawn_thief"]:
				QtBind.setChecked(gui__,cbxEvtSpawn_thief,data["cbxEvtSpawn_thief"])
			if "cbxEvtChar_attacked" in data and data["cbxEvtChar_attacked"]:
				QtBind.setChecked(gui__,cbxEvtChar_attacked,data["cbxEvtChar_attacked"])
			if "cbxEvtChar_died" in data and data["cbxEvtChar_died"]:
				QtBind.setChecked(gui__,cbxEvtChar_died,data["cbxEvtChar_died"])
			if "cbxEvtPet_transport_died" in data and data["cbxEvtPet_transport_died"]:
				QtBind.setChecked(gui__,cbxEvtPet_transport_died,data["cbxEvtPet_transport_died"])
			if "cbxEvtDrop_item" in data and data["cbxEvtDrop_item"]:
				QtBind.setChecked(gui__,cbxEvtDrop_item,data["cbxEvtDrop_item"])
			if "cbxEvtDrop_rare" in data and data["cbxEvtDrop_rare"]:
				QtBind.setChecked(gui__,cbxEvtDrop_rare,data["cbxEvtDrop_rare"])
			if "MESAJ" in data:
				QtBind.setText(gui__,tbxMsg,data["MESAJ"])
# CONFIG KAYIT ETME
def saveConfigs():
	# DATA ERISIMI VARSA KAYDET
	if isJoined():
		# DATAYI KAYDET
		data = {}
		data["cbxLogsInOne"] = QtBind.isChecked(gui__,cbxLogsInOne)
		data["cbxLogAll"] = QtBind.isChecked(gui__,cbxLogAll)
		data["cbxLogPrivate"] = QtBind.isChecked(gui__,cbxLogPrivate)
		data["cbxLogParty"] = QtBind.isChecked(gui__,cbxLogParty)
		data["cbxLogguild"] = QtBind.isChecked(gui__,cbxLogguild)
		data["cbxLogUnion"] = QtBind.isChecked(gui__,cbxLogUnion)
		data["cbxLogAcademy"] = QtBind.isChecked(gui__,cbxLogAcademy)
		data["cbxLogStall"] = QtBind.isChecked(gui__,cbxLogStall)
		data["cbxLogGlobal"] = QtBind.isChecked(gui__,cbxLogGlobal)
		data["cbxLogNotice"] = QtBind.isChecked(gui__,cbxLogNotice)
		data["cbxLogGM"] = QtBind.isChecked(gui__,cbxLogGM)
		data["cbxLogUnknown"] = QtBind.isChecked(gui__,cbxLogUnknown)
		data["cbxEvtSpawn_unique"] = QtBind.isChecked(gui__,cbxEvtSpawn_unique)
		data["cbxEvtSpawn_hunter"] = QtBind.isChecked(gui__,cbxEvtSpawn_hunter)
		data["cbxEvtSpawn_thief"] = QtBind.isChecked(gui__,cbxEvtSpawn_thief)
		data["cbxEvtChar_attacked"] = QtBind.isChecked(gui__,cbxEvtChar_attacked)
		data["cbxEvtChar_died"] = QtBind.isChecked(gui__,cbxEvtChar_died)
		data["cbxEvtPet_transport_died"] = QtBind.isChecked(gui__,cbxEvtPet_transport_died)
		data["cbxEvtDrop_item"] = QtBind.isChecked(gui__,cbxEvtDrop_item)
		data["cbxEvtDrop_rare"] = QtBind.isChecked(gui__,cbxEvtDrop_rare)
		data["MESAJ"] = QtBind.text(gui__,tbxMsg)
		with open(getConfig(),"w") as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))
		log("Plugin: "+pName+" CONFIG KAYIT EDILDI.")
# CHAR OYUNDA MI KONTROL ET
def isJoined():
	global character_data
	character_data = get_character_data()
	return character_data and "name" in character_data and character_data["name"]
def cbxLog_clicked(checked):
	saveConfigs()
# OTO MESAJ STARTLAMAK ICIN BUTONU KONTROL ETME
def cbxMsg_clicked(checked):
	global cbxMsg_checked
	cbxMsg_checked = checked
	if checked:
		global message_delay_counter
		message_delay_counter = 0
		QtBind.setText(gui__,lblCounter,"0")
		log("Plugin: MESAJ GONDERME BASLATILIYOR..")
	else:
		log("Plugin: MESAJ GONDERME DURDURULUYOR..")
def FixEscapeComma(_array):
	_len = len(_array)
	i = 0
	while i < _len:
		if _array[i].endswith('\\') and i < (_len-1):
			_array[i] = _array[i][:-1]+','+_array[i+1]
			del _array[i+1]
			_len-=1
		else:
			i+=1
	return _array
# ______________________________ ETKINLIKLER ______________________________ #
def chat(args):
	args = FixEscapeComma(args)
	if len(args) < 3 or not args[1] or not args[2]:
		return
	sent = False
	t = args[1].lower()
	if t == "all":
		sent = phBotChat.All(args[2])
	elif t == "private":
		sent = phBotChat.Private(args[2],args[3])
	elif t == "party":
		sent = phBotChat.Party(args[2])
	elif t == "guild":
		sent = phBotChat.guild(args[2])
	elif t == "union":
		sent = phBotChat.Union(args[2])
	elif t == "note":
		sent = phBotChat.Note(args[2],args[3])
	elif t == "stall":
		sent = phBotChat.Stall(args[2])
	elif t == "global":
		sent = phBotChat.Global(args[2])
	if sent:
		log('Plugin: Message "'+t+'" BASARIYLA GONDERILDI.')
def logline(args):
	if len(args) == 2:
		path = "log.txt" if QtBind.isChecked(gui__,cbxLogsInOne) else character_data["server"]+"_"+character_data["name"]+"_log.txt"
		date = strftime("%d/%m %I:%M:%S %p", localtime())
		with open(getPath()+path, "a", encoding='utf-8') as f:
			f.write(date+" > "+args[1]+'\r\n')
def connected():
	global character_data
	character_data = None
def joined_game():
	loadConfig()
def handle_chat(t,p,msg):
	if t == 100:
		on_discord_command(msg)
		return
	if not p:
		p = ""
	if t == 1 and QtBind.isChecked(gui__,cbxLogAll):
		logline(["","[All]"+p+":"+msg])
	elif t == 2 and QtBind.isChecked(gui__,cbxLogPrivate):
		logline(["","[Private]"+p+":"+msg])
	elif t == 3 and QtBind.isChecked(gui__,cbxLogGM):
		logline(["","[GM]"+p+":"+msg])
	elif t == 4 and QtBind.isChecked(gui__,cbxLogParty):
		logline(["","[Party]"+p+":"+msg])
	elif t == 5 and QtBind.isChecked(gui__,cbxLogguild):
		logline(["","[guild]"+p+":"+msg])
	elif t == 6 and QtBind.isChecked(gui__,cbxLogGlobal):
		logline(["","[Global]"+p+":"+msg])
	elif t == 7 and QtBind.isChecked(gui__,cbxLogNotice):
		logline(["","[Notice]"+p+":"+msg])
	elif t == 9 and QtBind.isChecked(gui__,cbxLogStall):
		logline(["","[Stall]"+p+":"+msg])
	elif t == 11 and QtBind.isChecked(gui__,cbxLogUnion):
		logline(["","[Union]"+p+":"+msg])
	elif t == 16 and QtBind.isChecked(gui__,cbxLogAcademy):
		logline(["","[Academy]"+p+":"+msg])
	elif QtBind.isChecked(gui__,cbxLogUnknown):
		logline(["","[Other("+str(t)+")]"+p+":"+msg])
def handle_event(t, data):
	if t == 0 and QtBind.isChecked(gui__,cbxEvtSpawn_unique):
		logline(["","[Spawn][Unique]:"+data])
	elif t == 1 and QtBind.isChecked(gui__,cbxEvtSpawn_hunter):
		logline(["","[Spawn][Hunter/Trader]:"+data])
	elif t == 2 and QtBind.isChecked(gui__,cbxEvtSpawn_thief):
		logline(["","[Spawn][Thief]:"+data])
	elif t == 3 and QtBind.isChecked(gui__,cbxEvtPet_transport_died):
		t = get_pets()[data]
		logline(["","[Pet]["+(t['type'].title())+"]:Died"])
	elif t == 4 and QtBind.isChecked(gui__,cbxEvtChar_attacked):
		logline(["","[Character][Attacked]:"+data])
	elif t == 5 and QtBind.isChecked(gui__,cbxEvtDrop_rare):
		t = get_item(int(data))
		logline(["","[Drop][Rare]:"+t['name']])
	elif t == 6 and QtBind.isChecked(gui__,cbxEvtDrop_item):
		t = get_item(int(data))
		logline(["","[Drop]:"+t['name']])
	elif t == 7 and QtBind.isChecked(gui__,cbxEvtChar_died):
		logline(["","[Character][Died]"])
def on_discord_command(cmd):
	args = cmd.split(' ',2)
	if args[0].lower().startswith('chat'):
		if len(args) == 3 and args[1] and args[2]:
			t = args[1].lower()
			if t == 'private' or t == 'note':
				argsExtra = args[2].split(' ',1)
				if argsExtra[0] and argsExtra[1]:
					args.pop(2)
					chat(args+argsExtra)
			else:
				chat(args)
def event_loop():
	if character_data:
		if cbxMsg_checked:
			global message_delay_counter
			message_delay_counter += 500
			if message_delay_counter >= MESSAGES_DELAY:
				message_delay_counter = 0
				message = QtBind.text(gui__,tbxMsg)
				if message:
					phBotChat.All(QtBind.text(gui__,tbxMsg))
					QtBind.setText(gui__,lblCounter,str(int(QtBind.text(gui__,lblCounter))+1))
# PLUGIN YUKLENDI
log('Plugin: '+pName+' v'+pVersion+' BASARIYLA YUKLENDI')
if os.path.exists(getPath()):
	loadConfigs()
else:
	# CONFIG DOSYASI OLUSTURULDU
	os.makedirs(getPath())
	log('Plugin: '+pName+' DOSYASI OLUSTURULDU.')
