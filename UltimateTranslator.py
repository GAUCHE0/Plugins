from phBot import *
from threading import Timer
import urllib.request
import QtBind
from datetime import datetime
import struct
import json
import os

pName = 'UltimateTranslator'
pVersion = '0.0.2'
pUrl = 'https://raw.githubusercontent.com/GAUCHE0/Plugins/main/UltimateTranslator.py'

# ______________________________ KURULUM ______________________________ #
URL_HOST = "https://phbot-xtranslator.jellybitz.repl.co/api/translate" # API server
URL_REQUEST_TIMEOUT = 10 # sec
SUPPORTED_LANGUAGES = {'Afrikaans':'af','Albanian':'sq','Amharic':'am','Arabic':'ar','Armenian':'hy','Azerbaijani':'az','Basque':'eu','Belarusian':'be','Bengali':'bn','Bosnian':'bs','Bulgarian':'bg','Catalan':'ca','Cebuano':'ceb','Chinese (Simplified)':'zh-CN','Chinese (Traditional)':'zh-TW','Corsican':'co','Croatian':'hr','Czech':'cs','Danish':'da','Dutch':'nl','English':'en','Esperanto':'eo','Estonian':'et','Finnish':'fi','French':'fr','Frisian':'fy','Galician':'gl','Georgian':'ka','German':'de','Greek':'el','Gujarati':'gu','Haitian Creole':'ht','Hausa':'ha','Hawaiian':'haw','Hebrew':'he','Hindi':'hi','Hmong':'hmn','Hungarian':'hu','Icelandic':'is','Igbo':'ig','Indonesian':'id','Irish':'ga','Italian':'it','Japanese':'ja','Javanese':'jv','Kannada':'kn','Kazakh':'kk','Khmer':'km','Kinyarwanda':'rw','Korean':'ko','Kurdish':'ku','Kyrgyz':'ky','Lao':'lo','Latin':'la','Latvian':'lv','Lithuanian':'lt','Luxembourgish':'lb','Macedonian':'mk','Malagasy':'mg','Malay':'ms','Malayalam':'ml','Maltese':'mt','Maori':'mi','Marathi':'mr','Mongolian':'mn','Myanmar (Burmese)':'my','Nepali':'ne','Norwegian':'no','Nyanja (Chichewa)':'ny','Odia (Oriya)':'or','Pashto':'ps','Persian':'fa','Polish':'pl','Portuguese (Portugal, Brazil)':'pt','Punjabi':'pa','Romanian':'ro','Russian':'ru','Samoan':'sm','Scots Gaelic':'gd','Serbian':'sr','Sesotho':'st','Shona':'sn','Sindhi':'sd','Sinhala (Sinhalese)':'si','Slovak':'sk','Slovenian':'sl','Somali':'so','Spanish':'es','Sundanese':'su','Swahili':'sw','Swedish':'sv','Tagalog (Filipino)':'tl','Tajik':'tg','Tamil':'ta','Tatar':'tt','Telugu':'te','Thai':'th','Turkish':'tr','Turkmen':'tk','Ukrainian':'uk','Urdu':'ur','Uyghur':'ug','Uzbek':'uz','Vietnamese':'vi','Welsh':'cy','Xhosa':'xh','Yiddish':'yi','Yoruba':'yo','Zulu':'zu'}
# KURESELLER
character_data = None
locale = None
# ARAYUZ OLUSTURMA
gui = QtBind.init(__name__,pName)
cbxTranslateIncomingChat = QtBind.createCheckBox(gui,'','GELEN MESAJLARI CEVIR',10,8)
cmbxTranslateIncomingLang = QtBind.createCombobox(gui,165,8,130,19)
cbxTranslateOutgoingChat = QtBind.createCheckBox(gui,'','GIDEN MESAJLARI CEVIR',10,28)
cmbxTranslateOutgoingLang = QtBind.createCombobox(gui,167,28,128,19)
# DESTEKLENEN DILLERLE DOLDURMA
for key in SUPPORTED_LANGUAGES:
	QtBind.append(gui,cmbxTranslateIncomingLang,key)
	QtBind.append(gui,cmbxTranslateOutgoingLang,key)
lstTranslatedMessages = QtBind.createList(gui,10,54,710,226)
btnSaveConfig = QtBind.createButton(gui,'save_configs','     KAYIT ET     ',615,4)
btnClearChat = QtBind.createButton(gui,'btnClearChat_clicked','     CHATI TEMIZLE     ',615,30)
# ______________________________ MOTHODLAR ______________________________ #
# DOSYA YOLUNDAN DEVAM ET
def get_path():
	return get_config_dir()+pName+"\\"
# CHAR COFIG YOLUNDAN DEVAM ET (JSON)
def get_config():
	return get_path()+character_data['server'] + "_" + character_data['name'] + ".json"
# CHAR OYUNDA MI KONTROL ET
def is_joined():
	global character_data
	character_data = get_character_data()
	if not (character_data and "name" in character_data and character_data["name"]):
		character_data = None
	return character_data
# VARSAYILAN CONFIGLERI YUKLE
def load_default_config():
	# VARSAYILAN ARAYUZ AYARLARI
	QtBind.setChecked(gui,cbxTranslateIncomingChat,False)
	QtBind.setChecked(gui,cbxTranslateOutgoingChat,False)
# TUM CONFIGLERI KAYDET
def save_configs():
	# DATA YUKLENDIYSE KAYDET
	if is_joined():
		# TUM DATAYI KAYDET
		data = {}
		data["Incoming Messages"] = QtBind.isChecked(gui,cbxTranslateIncomingChat)
		data["Outgoing Messages"] = QtBind.isChecked(gui,cbxTranslateOutgoingChat)

		data["Incoming Language"] = QtBind.text(gui,cmbxTranslateIncomingLang)
		data["Outgoing Language"] = QtBind.text(gui,cmbxTranslateOutgoingLang)
		# UZERINE YAZMA
		with open(get_config(),"w") as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))
		log("Plugin: "+pName+" CONFIG KAYIT EDILDI.")
# ONCEDEN KAYITLI CONFIG YUKLME
def load_configs():
	load_default_config()
	if is_joined():
		# YEREK AYARI 1 KEZ KAYDET
		global locale
		locale = get_locale()
		# YUKLENECEK CONFIG VAR MI KONTROL ET 
		if os.path.exists(get_config()):
			data = {}
			with open(get_config(),"r") as f:
				data = json.load(f)
			# TUM DATAYI YUKLE
			if 'Incoming Messages' in data and data['Incoming Messages']:
				QtBind.setChecked(gui,cbxTranslateIncomingChat,True)
			if 'Outgoing Messages' in data and data['Outgoing Messages']:
				QtBind.setChecked(gui,cbxTranslateOutgoingChat,True)
			if "Incoming Language" in data:
				QtBind.setText(gui,cmbxTranslateIncomingLang,data["Incoming Language"])
			if "Outgoing Language" in data:
				QtBind.setText(gui,cmbxTranslateOutgoingLang,data["Outgoing Language"])
def get_lang(languageName):
	if languageName in SUPPORTED_LANGUAGES:
		return SUPPORTED_LANGUAGES[languageName]
	return ''
def translate_text(text,dest,src=''):
	if not text:
		return ''
	try:
		data = {"text":text,"dest":dest}
		if src:
			data['src'] = src
		data = json.dumps(data).encode()
		req = urllib.request.Request(URL_HOST,data=data,headers={'content-type':'application/json'})
		with urllib.request.urlopen(req,timeout=URL_REQUEST_TIMEOUT) as f:
			try:
				resp = json.loads(f.read().decode())
				if resp:
					if resp['success']:
						return resp['result']
					else:
						log("Plugin: CEVIRME BASARISIZ ["+resp['message']+"]")
			except Exception as ex2:
				log("Plugin: SERVERDAN OKUMA HATASI ["+str(ex2)+"]")
	except Exception as ex:
		log("Plugin: URL HATASI ["+str(ex)+"] MESAJ CEVIRILEMEDI.")
	return ''
# CHAT CESITLERI
def get_chat_type(t):
	if t == 1:
		return '(All)'
	elif t == 2:
		return '(Private)'
	elif t == 3:
		return '(GM)'
	elif t == 4:
		return '(Party)'
	elif t == 5:
		return '(Guild)'
	elif t == 6:
		return '(Global)'
	elif t == 7:
		return '(Notice)'
	elif t == 9:
		return '(Stall)'
	elif t == 11:
		return '(Union)'
	elif t == 16:
		return '(Academy)'
	return '(Unknown)'
def btnClearChat_clicked():
	QtBind.clear(gui,lstTranslatedMessages)
# ______________________________ ETKINLIKLER ______________________________ #
def handle_joymax(opcode,data):
	# SERVER_CHAT_UPDATE
	if opcode == 0x3026:
		if not QtBind.isChecked(gui,cbxTranslateIncomingChat):
			return True
		nickname = ''
		chatType = data[0]
		index=1 
		if chatType in [1,3,13]:
			index+=4
		elif chatType in [2,4,5,6,9,11,16]:
			nickLenght = struct.unpack_from('<H', data,index)[0]
			index+=2 # nickLenght
			nickname = struct.unpack_from('<' + str(nickLenght) + 's', data,index)[0].decode('cp1252')
			index+=nickLenght
		else:
			return True
		p = data[:index]
		msgLength = struct.unpack_from('<H',data,index)[0]
		encoding = 'cp1252'
		if locale == 18 or locale == 56:
			msgLength = msgLength*2
			encoding = 'utf-16'
		index+=2 
		msg = struct.unpack_from('<' + str(msgLength) + 's',data,index)[0].decode(encoding)
		def translate_thread():
			lang = get_lang(QtBind.text(gui,cmbxTranslateIncomingLang))
			newMsg = translate_text(msg,lang)
			newPacket = p + struct.pack('<H',len(newMsg))
			newPacket += newMsg.encode(encoding) if encoding == 'cp1252' else newMsg.encode(encoding)[2:]
			inject_silkroad(opcode,newPacket,False)
			text = '< ['+datetime.now().strftime('%H:%M:%S')+']'+ ( ' '+nickname if nickname else '')+' '+get_chat_type(chatType)+':'+newMsg
			QtBind.append(gui,lstTranslatedMessages,text)
		Timer(0.001,translate_thread).start()
		return False
	return True
def handle_silkroad(opcode,data):
	# CLIENT_CHAT_REQUEST
	if opcode == 0x7025:
		if not QtBind.isChecked(gui,cbxTranslateOutgoingChat):
			return True
		chatType = data[0]
		index=1 
		index+=1 
		if locale == 18 or locale == 56:
			index+=2
		if chatType == 2:
			index+=2+struct.unpack_from('<H',data,index)[0]
		p = data[:index]
		msgLength = struct.unpack_from('<H',data,index)[0]
		encoding = 'cp1252'
		if locale == 18 or locale == 56:
			msgLength = msgLength*2
			encoding = 'utf-16'
		index+=2
		msg = struct.unpack_from('<' + str(msgLength) + 's',data,index)[0].decode(encoding)
		def translate_thread():
			lang = get_lang(QtBind.text(gui,cmbxTranslateOutgoingLang))
			newMsg = translate_text(msg,lang)
			newPacket = p + struct.pack('<H',len(newMsg))
			newPacket += newMsg.encode(encoding) if encoding == 'cp1252' else newMsg.encode(encoding)[2:]
			inject_joymax(opcode,newPacket,False)
			text = '> ['+datetime.now().strftime('%H:%M:%S')+'] '+get_chat_type(chatType)+':'+newMsg
			QtBind.append(gui,lstTranslatedMessages,text)
		Timer(0.001,translate_thread).start()
		return False
	return True
# PLUGIN YUKLENDI
log("Plugin: "+pName+" v"+pVersion+" BASARIYLA YUKLENDI.")
# CONFIG DOSYASINI KONTROL ET
if os.path.exists(get_path()):
	load_configs()
else:
	# CONFIG DOSYASI OLUSTURMA
	os.makedirs(get_path())
	log('Plugin: '+pName+' CONFIG KLASORU OLUSTURULDU.')
