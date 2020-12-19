from phBot import *
import QtBind
import json
import os

pName = 'UltimatePacketTooL'
pVersion = '1.0'

# ______________________________ KURULUM ______________________________ #

# KULLANICI ARAYUZU
gui = QtBind.init(__name__,pName)
lblInject = QtBind.createLabel(gui,'PAKET ENJEKSIYON PLUGINI..',21,15)
lblInject1 = QtBind.createLabel(gui,'GAUCHE TARAFINDAN DUZENLENMISTIR.',300,100)

cbxSro = QtBind.createCheckBox(gui, 'cbxSro_clicked','CLIENT PAKETLERINI GOSTER [C->S]',250,13)
cbxSro_checked = False
cbxJmx = QtBind.createCheckBox(gui, 'cbxJmx_clicked','SERVER PAKETLERINI GOSTER [S->C]',450,13)
cbxJmx_checked = False

lblUsing = QtBind.createLabel(gui,'OPCODE:\t               DATA:',35,47)
txtOpcode = QtBind.createLineEdit(gui,"",85,45,40,20)
txtData = QtBind.createLineEdit(gui,"",163,45,450,20)
cbxEncrypted = QtBind.createCheckBox(gui, 'cbxEnc_clicked','ENCRYPTED',620,47)
btnInjectPacket = QtBind.createButton(gui,'btnInjectPacket_clicked',"  PAKETI ENJEKTE ET  ",348,65)

cbxDontShow = QtBind.createCheckBox(gui, 'cbxDontShow_clicked',"FILTRELE",25,90)
cbxOnlyShow = QtBind.createCheckBox(gui, 'cbxOnlyShow_clicked',"FILTRELEME",120,90)
QtBind.setChecked(gui,cbxDontShow,True) # using two checkbox like radiobutton
cbxDontShow_checked = True
lblOpcodes = QtBind.createLabel(gui,"EKLENEN OPCODE'LARI FILTRELE :",21,110)
tbxOpcodes = QtBind.createLineEdit(gui,"",21,129,100,20)
lstOpcodes = QtBind.createList(gui,21,151,176,109)
btnAddOpcode = QtBind.createButton(gui,'btnAddOpcode_clicked',"      EKLE     ",123,129)
btnRemOpcode = QtBind.createButton(gui,'btnRemOpcode_clicked',"      SIL       ",70,259)

lblNpcs = QtBind.createLabel(gui,"YAKINDAKI NPCLER :",250,135)
btnNpcs = QtBind.createButton(gui,'btnNpcs_clicked',"  LISTEYI YENILE  ",569,252)
lstNpcs = QtBind.createList(gui,250,151,400,100)

# ______________________________METHODLAR ______________________________ #

# CLIENT PAKETLERINI GOSTER CHECKBOX KONTROLU
def cbxSro_clicked(checked):
	global cbxSro_checked
	cbxSro_checked = checked

#  SERVER PAKETLERINI GOSTER CHECKBOX KONTROLU
def cbxJmx_clicked(checked):
	global cbxJmx_checked
	cbxJmx_checked = checked

# BUTONA BASILDIGINDA PAKET ENKEKTE ET
def btnInjectPacket_clicked():
	strOpcode = QtBind.text(gui,txtOpcode)
	strData = QtBind.text(gui,txtData)
	# OPCODE YA DA DATA BOSSA
	if strOpcode and strData:
		Packet = bytearray()
		opcode = int(strOpcode,16)
		data = strData.split()
		i = 0
		while i < len(data):
			Packet.append(int(data[i],16))
			i += 1
		encrypted = QtBind.isChecked(gui,cbxEncrypted)
		log("Plugin: PAKET ENJEKTE EDILIYOR : ("+pName+")")
		inject_joymax(opcode,Packet,encrypted)

# CONFIG DOSYASINDAN DEVAM ET (JSON)
def getConfig():
	return get_config_dir()+pName+".json"

# FILTRELEME CHECKBOX KONTROLU
def cbxDontShow_clicked(checked):
	cbxDontShow_editConfig(checked)
	QtBind.setChecked(gui,cbxOnlyShow,not checked)
	
# FILTRELE CHECKBOX KONTROLU
def cbxOnlyShow_clicked(checked):
	cbxDontShow_editConfig(not checked)
	QtBind.setChecked(gui,cbxDontShow,not checked)

# FILTRELEME ISARETLIYSE YAPILACAKLAR
def	cbxDontShow_editConfig(checked):
	global cbxDontShow_checked
	cbxDontShow_checked = checked
	# INIT DATASI
	data = {}
	# CONFIG VARSA
	if os.path.exists(getConfig()):
		with open(getConfig(),"r") as f:
			data = json.load(f)
			
	data["DontShow"] = checked
	# CONFIG YAPILANDIRMA
	with open(getConfig(),"w") as f:
		# JSON OLARAK KAYIT ETMEK
		f.write(json.dumps(data, indent=4, sort_keys=True))

# VARSAYILAN CONFIG AYARLARI
def loadDefaultConfig():
	# Clear data
	QtBind.clear(gui,lstOpcodes)

# CONFIDDE KAYITLI OPCODELARI TANIMLAMAK
def loadConfigs():
	loadDefaultConfig()
	if os.path.exists(getConfig()):
		data = {}
		with open(getConfig(),"r") as f:
			data = json.load(f)
		if "Opcodes" in data:
			for opcode in data["Opcodes"]:
				QtBind.append(gui,lstOpcodes,opcode)
		if "DontShow" in data:
			global cbxDontShow_checked
			cbxDontShow_checked = data["DontShow"]
			QtBind.setChecked(gui,cbxDontShow,data["DontShow"])
			QtBind.setChecked(gui,cbxOnlyShow,not data["DontShow"])
		
# LISTEDE OPCODE VARSA DEVAM ET
def lstOpcodes_exists(opcode):
	strOpcode = '0x{:02X}'.format(opcode)
	opcodes = QtBind.getItems(gui,lstOpcodes)
	for i in range(len(opcodes)):
		if opcodes[i] == strOpcode:
			return True
	return False
	
# EKLE BUTONUNA TIKLANDIGINDA
def btnAddOpcode_clicked():
	opcode = int(QtBind.text(gui,tbxOpcodes),16)
	if opcode and not lstOpcodes_exists(opcode):
		data = {}
		if os.path.exists(getConfig()):
			with open(getConfig(),"r") as f:
				data = json.load(f)
		# LISTEDE OPCODE VARSA
		if "Opcodes" in data:
			data["Opcodes"].append('0x{:02X}'.format(opcode))
		else:
			data["Opcodes"] = ['0x{:02X}'.format(opcode)]
		with open(getConfig(),"w") as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))
		QtBind.append(gui,lstOpcodes,'0x{:02X}'.format(opcode))
		# BARASIYLA KAYDEDILIRSE
		QtBind.setText(gui, tbxOpcodes,"")
		log("Plugin: OPCODE EKLENDI [0x"+'{:02X}'.format(opcode)+"]")

# SIL BUTONUNA BASILDIGINDA
def btnRemOpcode_clicked():
	selectedItem = QtBind.text(gui,lstOpcodes)
	if selectedItem:
		if os.path.exists(getConfig()):
			data = {}
			with open(getConfig(), 'r') as f:
				data = json.load(f)
			try:
				data["Opcodes"].remove(selectedItem)
				with open(getConfig(),"w") as f:
					f.write(json.dumps(data, indent=4, sort_keys=True))
			except:
				pass 
		QtBind.remove(gui,lstOpcodes,selectedItem)
		log("Plugin: OPCODE SILINDI ["+selectedItem+"]")

# LOGDA PAKETLERI GOSTERME
def show_packet(opcode):
	if lstOpcodes_exists(opcode):
		if not cbxDontShow_checked:
			return True
	elif cbxDontShow_checked:
		return True
	return False

# ______________________________ ETKINLIKLER ______________________________ #

def handle_silkroad(opcode, data):
	if cbxSro_checked:
		if show_packet(opcode):
			log("Client: (OPCODE) 0x" + '{:02X}'.format(opcode) + " (DATA) "+ ("None" if not data else ' '.join('{:02X}'.format(x) for x in data)))
	return True

def handle_joymax(opcode, data):
	if cbxJmx_checked:
		if show_packet(opcode):
			log("Server: (OPCODE) 0x" + '{:02X}'.format(opcode) + " (DATA) "+ ("None" if not data else ' '.join('{:02X}'.format(x) for x in data)))
	return True
		
def btnNpcs_clicked():
	npcs = get_npcs()
	QtBind.clear(gui,lstNpcs)
	QtBind.append(gui,lstNpcs,'[Name] [ServerName] [ModelID] (UniqueID)')
	if npcs:
		QtBind.append(gui,lstNpcs,' -')
		for UniqueID, NPC in npcs.items():
			QtBind.append(gui,lstNpcs,"["+NPC['name'] + "] ["+NPC['servername']+"] ["+str(NPC['model'])+"] ("+str(UniqueID)+")")
#PLUGIN YUKLEME
log('Plugin: '+pName+' v'+pVersion+' BASARIYLA YUKLENDI')
loadConfigs()