from phBot import *
import QtBind
import struct
import json
import os

pName = 'UltimateChanger'
pVersion = '0.0.2'
pUrl = 'https://raw.githubusercontent.com/GAUCHE0/Plugins/main/UltimateChanger.py'

# ______________________________ KURULUM ______________________________ #
# KÜRSELLER
character_data = None
ExchangeStatus = ''
# OPCODE'LAR
CLIENT_GAME_PETITION_RESPONSE = 0x3080
SERVER_GAME_PETITION_REQUEST = 0x3080
SERVER_EXCHANGE_STARTED = 0x3085
SERVER_EXCHANGE_PLAYER_CONFIRMED = 0x3086
SERVER_EXCHANGE_COMPLETED = 0x3087
SERVER_EXCHANGE_CANCELED = 0x3088
CLIENT_EXCHANGE_CONFIRM_REQUEST = 0x7082
SERVER_EXCHANGE_CONFIRM_RESPONSE = 0xB082
CLIENT_EXCHANGE_APPROVE_REQUEST = 0x7083
SERVER_EXCHANGE_INVITATION_RESPONSE = 0xB081
SERVER_EXCHANGE_APPROVE_RESPONSE = 0xB083
SERVER_EXCHANGE_EXIT_RESPONSE = 0xB084
# ARAYUZ KURULUMU
gui = QtBind.init(__name__,pName)
_x=6
_y=9
QtBind.createLabel(gui,'GUVENILIR CHAR LISTESI (PT)',_x,_y)
_y+=20
tbxExchangerName = QtBind.createLineEdit(gui,"",_x,_y,100,20)
QtBind.createButton(gui,'btnAddExchanger_clicked',"   EKLE    ",_x+101,_y-2)
_y+=20
lvwExchangers = QtBind.createList(gui,_x,_y,176,60)
_y+=60
QtBind.createButton(gui,'btnRemExchanger_clicked'," 	 SIL	 ",_x+49,_y-2)
_y+=20 + 10
cbxReplyAccept = QtBind.createCheckBox(gui,'checkbox_changed','OTO "ACCEPT" CEVAPLA ',_x,_y)
_y+=20
cbxReplyApprove = QtBind.createCheckBox(gui,'checkbox_changed','OTO "APPROVE" CEVAPLA',_x,_y)
_x+=185
_y=9
cbxAcceptAll = QtBind.createCheckBox(gui,'checkbox_changed','HERKESE OTO EXCHANGE KABULU AC',_x,_y)
# ______________________________ METHODLAR ______________________________ #
# DOSYA YOLUNA DEVAM ET
def get_path():
	return get_config_dir()+pName+"\\"
# CHAR CONFIG YOLUAN DEVAM ET
def get_config():
	return get_path()+character_data['server'] + "_" + character_data['name'] + ".json"
# CHAR OYUNDA MI KONTROL ET
def is_joined():
	global character_data
	character_data = get_character_data()
	if not (character_data and "name" in character_data and character_data["name"]):
		character_data = None
	return character_data
# VARASAYILAN CONFIGLERI YUKLE
def load_default_config():
	# DATAYI TEMIZLE
	QtBind.setChecked(gui,cbxAcceptAll,False)
	QtBind.setChecked(gui,cbxReplyAccept,True)
	QtBind.setChecked(gui,cbxReplyApprove,True)
	QtBind.clear(gui,lvwExchangers)
# CONFIGLERI KAYDET
def save_configs():
	if is_joined():
		data = {}
		data["AcceptAll"] = QtBind.isChecked(gui,cbxAcceptAll)
		data["ReplyAccept"] = QtBind.isChecked(gui,cbxReplyAccept)
		data["ReplyApprove"] = QtBind.isChecked(gui,cbxReplyApprove)
		data["Exchangers"] = QtBind.getItems(gui,lvwExchangers)
		with open(get_config(),"w") as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))
		log("Plugin: "+pName+"CONFIG KAYIT EDILDI..")
# KAYITLI DATAYI YUKLE
def load_configs():
	load_default_config()
	if is_joined():
		if os.path.exists(get_config()):
			data = {}
			with open(get_config(),"r") as f:
				data = json.load(f)
			# Load data
			if "AcceptAll" in data and data['AcceptAll']:
				QtBind.setChecked(gui,cbxAcceptAll,True)
			if "ReplyAccept" in data and not data['ReplyAccept']:
				QtBind.setChecked(gui,cbxReplyAccept,False)
			if "ReplyApprove" in data and not data['ReplyApprove']:
				QtBind.setChecked(gui,cbxReplyApprove,False)
			if "Exchangers" in data:
				for charName in data["Exchangers"]:
					QtBind.append(gui,lvwExchangers,charName)
# CHECKBOX DEGERLERINDE DEGISIKLIK OLDUGUNDA KAYIT ICIN CAGIR
def checkbox_changed(newValue):
	save_configs()
# LISTEDE ISIM VARSA DEVAM ET 
def string_in_list(vString,vList,ModeSensitive=False):
	if not ModeSensitive:
		vString = vString.lower()
	for i in range(len(vList)):
		if not ModeSensitive:
			vList[i] = vList[i].lower()
		if vList[i] == vString:
			return True
	return False
# LISTEYE NICK EKLEME
def btnAddExchanger_clicked():
	if character_data:
		player = QtBind.text(gui,tbxExchangerName)
		if player and not string_in_list(player,QtBind.getItems(gui,lvwExchangers)):
			QtBind.append(gui,lvwExchangers,player)
			save_configs()
			QtBind.setText(gui,tbxExchangerName,"")
			log('Plugin: KISI GUVENILIR LISTEYE EKLENDI : ['+player+']')
# LISTEDEN NICK SILME
def btnRemExchanger_clicked():
	if character_data:
		selectedItem = QtBind.text(gui,lvwExchangers)
		if selectedItem:
			QtBind.remove(gui,lvwExchangers,selectedItem)
			save_configs()
			log("Plugin: KISI GUVENILIR LISTEDEN SILINDI : ["+selectedItem+"]")
# CHAR DATALARINDAN UNIQ ID ALMA
def get_charname(UniqueID):	
	if UniqueID == character_data['player_id']:
		return character_data['name']
	players = get_party()
	if players:
		for key, player in players.items():
			if player['player_id'] == UniqueID:
				return player['name']
	return ""
def Inject_GamePetitionResponse(Accept,Type):
	if Accept:
		p = b'\x01\x01'
	else:
		# Party Invitation or Party Creation
		if Type == 2 or Type == 3:
			p = b'\x02\x0C\x2C'
		# Default
		else:
			p = b'\x01\x00'
	inject_joymax(CLIENT_GAME_PETITION_RESPONSE,p,False)
# ______________________________ ETKINLIKLER ______________________________ #
# CHAR OYUNA GIRDIGINDE CAGIR
def joined_game():
	load_configs()

def handle_joymax(opcode, data):
	if opcode == SERVER_GAME_PETITION_REQUEST:
		t = data[0]
		if t == 1: 
			if QtBind.isChecked(gui,cbxAcceptAll):
				Inject_GamePetitionResponse(True,t)
				return True
			entityID = struct.unpack_from('<I', data, 1)[0]
			charName = get_charname(entityID)
			if string_in_list(charName,QtBind.getItems(gui,lvwExchangers)):
				Inject_GamePetitionResponse(True,t)
		return True
	global ExchangeStatus
	if opcode == SERVER_EXCHANGE_STARTED:
		ExchangeStatus = 'STARTED'
	elif opcode == SERVER_EXCHANGE_INVITATION_RESPONSE:
		if data[0] == 1: # success
			ExchangeStatus = 'STARTED'
	elif opcode == SERVER_EXCHANGE_PLAYER_CONFIRMED:
		if ExchangeStatus == 'STARTED':
			if QtBind.isChecked(gui,cbxReplyAccept):
				inject_joymax(CLIENT_EXCHANGE_CONFIRM_REQUEST,b'',False)
		elif ExchangeStatus == 'CONFIRMED':
			if QtBind.isChecked(gui,cbxReplyApprove):
				inject_joymax(CLIENT_EXCHANGE_APPROVE_REQUEST,b'',False)
	elif opcode == SERVER_EXCHANGE_CONFIRM_RESPONSE:
		if data[0] == 1: 
			ExchangeStatus = 'CONFIRMED'
			if QtBind.isChecked(gui,cbxReplyApprove):
				inject_joymax(CLIENT_EXCHANGE_APPROVE_REQUEST,b'',False)
	elif opcode == SERVER_EXCHANGE_APPROVE_RESPONSE:
		if data[0] == 1: 
			ExchangeStatus = 'APPROVED'
	elif opcode == SERVER_EXCHANGE_COMPLETED or opcode == SERVER_EXCHANGE_CANCELED:
		ExchangeStatus = ''
	elif opcode == SERVER_EXCHANGE_EXIT_RESPONSE:
		if data[0] == 1:
			ExchangeStatus = ''
	return True
# PLUGIN YUKLEME
log('Plugin: '+pName+' v'+pVersion+' BASARIYLA YUKLENDI.')
if os.path.exists(get_path()):
	load_configs()
else:
	# CONFIG DOSYASI OLUSTURMA
	os.makedirs(get_path())
	log('Plugin: '+pName+'  DOSYA OLUSTURULDU.')
