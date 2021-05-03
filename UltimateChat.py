from phBot import *
from time import localtime, strftime
import phBotChat
import QtBind
import json
import os

pName = 'UltimateChat'
pVersion = '0.0.6'
pUrl = "https://raw.githubusercontent.com/GAUCHE0/Plugins/main/UltimateChat.py"

# ______________________________ KURULUM ______________________________ #
# KURESELLER
MESSAGES_DELAY = 10000
message_delay_counter = 0
character_data = None
# GUI
gui = QtBind.init(__name__,pName)
cbxMsg = QtBind.createCheckBox(gui, 'cbxMsg_clicked','MESAJ GONDER: ', 21, 13)
cbxMsg_checked = False
tbxMsg = QtBind.createLineEdit(gui,"",125,12,480,18)
lblSpamCounter = QtBind.createLabel(gui,"MESAJ SAYACI :",620,13)
lblCounter = QtBind.createLabel(gui,"0",700,13)
lblLog = QtBind.createLabel(gui,"UltimateChat:\n * GAUCHE TARAFINDAN DUZENLENMISTIR. \n * FEEDBACK SISTEMLI BIR YAZILIMDIR. \n * HATA VE ONERI BILDIRIMLERINIZI BANA ULASTIRABILIRSINIZ.",385,220)
cbxLogsInOne = QtBind.createCheckBox(gui, 'cbxLog_clicked','MESAJLARI DOSYA OLARAK KAYDET.(log.txt)', 420, 45)
cbxLogAll = QtBind.createCheckBox(gui,'cbxLog_clicked','GENEL',21,64)
cbxLogPrivate = QtBind.createCheckBox(gui,'cbxLog_clicked','OZEL',21,83)
cbxLogParty = QtBind.createCheckBox(gui,'cbxLog_clicked','PARTI',21,102)
cbxLogGuild = QtBind.createCheckBox(gui,'cbxLog_clicked','GUILD',21,121)
cbxLogUnion = QtBind.createCheckBox(gui,'cbxLog_clicked','UNION',21,140)
cbxLogAcademy = QtBind.createCheckBox(gui,'cbxLog_clicked','AKADEMI',21,159)
cbxLogStall = QtBind.createCheckBox(gui,'cbxLog_clicked','STALL',21,178)
cbxLogGlobal = QtBind.createCheckBox(gui,'cbxLog_clicked','GLOBAL',21,197)
cbxLogNotice = QtBind.createCheckBox(gui,'cbxLog_clicked','BILDIRI',21,216)
cbxLogGM = QtBind.createCheckBox(gui,'cbxLog_clicked','GM',21,235)
cbxLogUnknown = QtBind.createCheckBox(gui,'cbxLog_clicked','DIGER HEPSI',21, 254)
cbxEvtSpawn_unique = QtBind.createCheckBox(gui,'cbxLog_clicked','UNIQUE SPAWN',321, 64)
cbxEvtSpawn_hunter = QtBind.createCheckBox(gui,'cbxLog_clicked','HUNTER/TRADER SPAWN',321,83)
cbxEvtSpawn_thief = QtBind.createCheckBox(gui,'cbxLog_clicked','THIEF SPAWN',321,102)
cbxEvtChar_attacked = QtBind.createCheckBox(gui,'cbxLog_clicked','KARAKTER ATAK ALDIGINDA',321,121)
cbxEvtChar_died = QtBind.createCheckBox(gui,'cbxLog_clicked','KARAKTER OLDUGUNDE',321,140)
cbxEvtPet_transport_died = QtBind.createCheckBox(gui,'cbxLog_clicked','TRANSPORT/PET OLDUGUNDE',321,159)
cbxEvtDrop_item = QtBind.createCheckBox(gui,'cbxLog_clicked','ITEM DUSTUGUNDE',321,178)
cbxEvtDrop_rare = QtBind.createCheckBox(gui,'cbxLog_clicked','SOX DUSTUGUNDE',321,197)
# ______________________________ METHODLAR ______________________________ #
# CONFIGDEN DEVAM ET
def getPath():
	return get_config_dir()+pName+"\\"
def getConfig():
	return getPath()+character_data["server"]+"_"+character_data["name"]+".json"
# VARSAYILAN CONFIGLERI YUKLE
def loadDefaultConfig():
	# DATAYI TEMIZLE
	QtBind.setChecked(gui,cbxLogsInOne,False)
	QtBind.setChecked(gui,cbxLogAll,False)
	QtBind.setChecked(gui,cbxLogPrivate,False)
	QtBind.setChecked(gui,cbxLogParty,False)
	QtBind.setChecked(gui,cbxLogGuild,False)
	QtBind.setChecked(gui,cbxLogUnion,False)
	QtBind.setChecked(gui,cbxLogStall,False)
	QtBind.setChecked(gui,cbxLogGlobal,False)
	QtBind.setChecked(gui,cbxLogNotice,False)
	QtBind.setChecked(gui,cbxLogGM,False)
	QtBind.setChecked(gui,cbxLogUnknown,False)
	QtBind.setChecked(gui,cbxEvtSpawn_unique,False)
	QtBind.setChecked(gui,cbxEvtSpawn_hunter,False)
	QtBind.setChecked(gui,cbxEvtSpawn_thief,False)
	QtBind.setChecked(gui,cbxEvtChar_attacked,False)
	QtBind.setChecked(gui,cbxEvtChar_died,False)
	QtBind.setChecked(gui,cbxEvtPet_transport_died,False)
	QtBind.setChecked(gui,cbxEvtDrop_item,False)
	QtBind.setChecked(gui,cbxEvtDrop_rare,False)
# KAYDEDILEN CONFIGLERI YUKLE
def loadConfigs():
	loadDefaultConfig()
	if isJoined():
		if os.path.exists(getConfig()):
			data = {}
			with open(getConfig(),"r") as f:
				data = json.load(f)

			if "cbxLogsInOne" in data and data["cbxLogsInOne"]:
				QtBind.setChecked(gui,cbxLogsInOne,data["cbxLogsInOne"])
			if "cbxLogAll" in data and data["cbxLogAll"]:
				QtBind.setChecked(gui,cbxLogAll,data["cbxLogAll"])
			if "cbxLogPrivate" in data and data["cbxLogPrivate"]:
				QtBind.setChecked(gui,cbxLogPrivate,data["cbxLogPrivate"])
			if "cbxLogParty" in data and data["cbxLogParty"]:
				QtBind.setChecked(gui,cbxLogParty,data["cbxLogParty"])
			if "cbxLogGuild" in data and data["cbxLogGuild"]:
				QtBind.setChecked(gui,cbxLogGuild,data["cbxLogGuild"])
			if "cbxLogUnion" in data and data["cbxLogUnion"]:
				QtBind.setChecked(gui,cbxLogUnion,data["cbxLogUnion"])
			if "cbxLogAcademy" in data and data["cbxLogAcademy"]:
				QtBind.setChecked(gui,cbxLogAcademy,data["cbxLogAcademy"])
			if "cbxLogStall" in data and data["cbxLogStall"]:
				QtBind.setChecked(gui,cbxLogStall,data["cbxLogStall"])
			if "cbxLogGlobal" in data and data["cbxLogGlobal"]:
				QtBind.setChecked(gui,cbxLogGlobal,data["cbxLogGlobal"])
			if "cbxLogNotice" in data and data["cbxLogNotice"]:
				QtBind.setChecked(gui,cbxLogNotice,data["cbxLogNotice"])
			if "cbxLogGM" in data and data["cbxLogGM"]:
				QtBind.setChecked(gui,cbxLogGM,data["cbxLogGM"])
			if "cbxLogUnknown" in data and data["cbxLogUnknown"]:
				QtBind.setChecked(gui,cbxLogUnknown,data["cbxLogUnknown"])
			if "cbxEvtSpawn_unique" in data and data["cbxEvtSpawn_unique"]:
				QtBind.setChecked(gui,cbxEvtSpawn_unique,data["cbxEvtSpawn_unique"])
			if "cbxEvtSpawn_hunter" in data and data["cbxEvtSpawn_hunter"]:
				QtBind.setChecked(gui,cbxEvtSpawn_hunter,data["cbxEvtSpawn_hunter"])
			if "cbxEvtSpawn_thief" in data and data["cbxEvtSpawn_thief"]:
				QtBind.setChecked(gui,cbxEvtSpawn_thief,data["cbxEvtSpawn_thief"])
			if "cbxEvtChar_attacked" in data and data["cbxEvtChar_attacked"]:
				QtBind.setChecked(gui,cbxEvtChar_attacked,data["cbxEvtChar_attacked"])
			if "cbxEvtChar_died" in data and data["cbxEvtChar_died"]:
				QtBind.setChecked(gui,cbxEvtChar_died,data["cbxEvtChar_died"])
			if "cbxEvtPet_transport_died" in data and data["cbxEvtPet_transport_died"]:
				QtBind.setChecked(gui,cbxEvtPet_transport_died,data["cbxEvtPet_transport_died"])
			if "cbxEvtDrop_item" in data and data["cbxEvtDrop_item"]:
				QtBind.setChecked(gui,cbxEvtDrop_item,data["cbxEvtDrop_item"])
			if "cbxEvtDrop_rare" in data and data["cbxEvtDrop_rare"]:
				QtBind.setChecked(gui,cbxEvtDrop_rare,data["cbxEvtDrop_rare"])
# TUM CONFIGLERI KAYDET
def saveConfigs():
	if isJoined():
		data = {}
		data["cbxLogsInOne"] = QtBind.isChecked(gui,cbxLogsInOne)
		data["cbxLogAll"] = QtBind.isChecked(gui,cbxLogAll)
		data["cbxLogPrivate"] = QtBind.isChecked(gui,cbxLogPrivate)
		data["cbxLogParty"] = QtBind.isChecked(gui,cbxLogParty)
		data["cbxLogGuild"] = QtBind.isChecked(gui,cbxLogGuild)
		data["cbxLogUnion"] = QtBind.isChecked(gui,cbxLogUnion)
		data["cbxLogAcademy"] = QtBind.isChecked(gui,cbxLogAcademy)
		data["cbxLogStall"] = QtBind.isChecked(gui,cbxLogStall)
		data["cbxLogGlobal"] = QtBind.isChecked(gui,cbxLogGlobal)
		data["cbxLogNotice"] = QtBind.isChecked(gui,cbxLogNotice)
		data["cbxLogGM"] = QtBind.isChecked(gui,cbxLogGM)
		data["cbxLogUnknown"] = QtBind.isChecked(gui,cbxLogUnknown)
		data["cbxEvtSpawn_unique"] = QtBind.isChecked(gui,cbxEvtSpawn_unique)
		data["cbxEvtSpawn_hunter"] = QtBind.isChecked(gui,cbxEvtSpawn_hunter)
		data["cbxEvtSpawn_thief"] = QtBind.isChecked(gui,cbxEvtSpawn_thief)
		data["cbxEvtChar_attacked"] = QtBind.isChecked(gui,cbxEvtChar_attacked)
		data["cbxEvtChar_died"] = QtBind.isChecked(gui,cbxEvtChar_died)
		data["cbxEvtPet_transport_died"] = QtBind.isChecked(gui,cbxEvtPet_transport_died)
		data["cbxEvtDrop_item"] = QtBind.isChecked(gui,cbxEvtDrop_item)
		data["cbxEvtDrop_rare"] = QtBind.isChecked(gui,cbxEvtDrop_rare)
		with open(getConfig(),"w") as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))
		log("Plugin: "+pName+" CONFIG KAYDEDILDI..")
# CHAR OYUNDAMI KONTROL ET
def isJoined():
	global character_data
	character_data = get_character_data()
	return character_data and "name" in character_data and character_data["name"]
def cbxLog_clicked(checked):
	saveConfigs()
# SPAM AKTIF KOMUTU
def cbxMsg_clicked(checked):
	global cbxMsg_checked
	cbxMsg_checked = checked
	if checked:
		# restart spamer counter
		global message_delay_counter
		message_delay_counter = 0
		QtBind.setText(gui,lblCounter,"0")
		log("Plugin: SPAM BASLATILDI..")
	else:
		log("Plugin: SPAM DURDURULDU")

def FixEscapeComma(_array):
	_len = len(_array)
	i = 0
	while i < _len:
		# Check if any argument ends with '\'
		if _array[i].endswith('\\') and i < (_len-1):
			_array[i] = _array[i][:-1]+','+_array[i+1]
			del _array[i+1]
			_len-=1
		else:
			i+=1
	return _array
# ______________________________ ETKINLIKLER______________________________ #

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
		sent = phBotChat.Guild(args[2])
	elif t == "union":
		sent = phBotChat.Union(args[2])
	elif t == "note":
		sent = phBotChat.Note(args[2],args[3])
	elif t == "stall":
		sent = phBotChat.Stall(args[2])
	elif t == "global":
		sent = phBotChat.Global(args[2])
	if sent:
		log('Plugin: MESAJ "'+t+'" BASARIYLA GONDERILDI..')
# LOG DOSYASI OLUSTURMA
def logline(args):
	if len(args) == 2:
		path = "log.txt" if QtBind.isChecked(gui,cbxLogsInOne) else character_data["server"]+"_"+character_data["name"]+"_log.txt"
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
	if t == 1 and QtBind.isChecked(gui,cbxLogAll):
		logline(["","[All]"+p+":"+msg])
	elif t == 2 and QtBind.isChecked(gui,cbxLogPrivate):
		logline(["","[Private]"+p+":"+msg])
	elif t == 3 and QtBind.isChecked(gui,cbxLogGM):
		logline(["","[GM]"+p+":"+msg])
	elif t == 4 and QtBind.isChecked(gui,cbxLogParty):
		logline(["","[Party]"+p+":"+msg])
	elif t == 5 and QtBind.isChecked(gui,cbxLogGuild):
		logline(["","[Guild]"+p+":"+msg])
	elif t == 6 and QtBind.isChecked(gui,cbxLogGlobal):
		logline(["","[Global]"+p+":"+msg])
	elif t == 7 and QtBind.isChecked(gui,cbxLogNotice):
		logline(["","[Notice]"+p+":"+msg])
	elif t == 9 and QtBind.isChecked(gui,cbxLogStall):
		logline(["","[Stall]"+p+":"+msg])
	elif t == 11 and QtBind.isChecked(gui,cbxLogUnion):
		logline(["","[Union]"+p+":"+msg])
	elif t == 16 and QtBind.isChecked(gui,cbxLogAcademy):
		logline(["","[Academy]"+p+":"+msg])
	elif QtBind.isChecked(gui,cbxLogUnknown):
		logline(["","[Other("+str(t)+")]"+p+":"+msg])
def handle_event(t, data):
	if t == 0 and QtBind.isChecked(gui,cbxEvtSpawn_unique):
		logline(["","[Spawn][Unique]:"+data])
	elif t == 1 and QtBind.isChecked(gui,cbxEvtSpawn_hunter):
		logline(["","[Spawn][Hunter/Trader]:"+data])
	elif t == 2 and QtBind.isChecked(gui,cbxEvtSpawn_thief):
		logline(["","[Spawn][Thief]:"+data])
	elif t == 3 and QtBind.isChecked(gui,cbxEvtPet_transport_died):
		t = get_pets()[data]
		logline(["","[Pet]["+(t['type'].title())+"]:Died"])
	elif t == 4 and QtBind.isChecked(gui,cbxEvtChar_attacked):
		logline(["","[Character][Attacked]:"+data])
	elif t == 5 and QtBind.isChecked(gui,cbxEvtDrop_rare):
		t = get_item(int(data))
		logline(["","[Drop][Rare]:"+t['name']])
	elif t == 6 and QtBind.isChecked(gui,cbxEvtDrop_item):
		t = get_item(int(data))
		logline(["","[Drop]:"+t['name']])
	elif t == 7 and QtBind.isChecked(gui,cbxEvtChar_died):
		logline(["","[Character][Died]"])
# DC UZERINDEN KONTROL ICIN
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
				message = QtBind.text(gui,tbxMsg)
				if message:
					phBotChat.All(QtBind.text(gui,tbxMsg))
					QtBind.setText(gui,lblCounter,str(int(QtBind.text(gui,lblCounter))+1))

log('Plugin: '+pName+' v'+pVersion+' BASARIYLA YUKLENDI')

if os.path.exists(getPath()):
	loadConfigs()
else:
	os.makedirs(getPath())
	log('Plugin: '+pName+' DOSYASI OLUSTURULDU..')
