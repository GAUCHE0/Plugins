from phBot import *
import QtBind
from threading import Timer
from time import sleep
import sqlite3
import json
import struct
import os

pVersion = '0.0.1'
pName = 'UltimateDungeon'
pUrl = ''

# ______________________________ KURULUM ______________________________ #
DIMENSIONAL_COOLDOWN_DELAY = 18000 # SANIYE (2 SAAT)
WAIT_DROPS_DELAY_MAX = 10 # SANIYE
COUNT_MOBS_DELAY = 1.0 # SANIYE
# API UYUMLULUGU
API_COMPATIBILITY = tuple(map(int, (get_version().split(".")))) < (25,0,7)
# KURESELLER
character_data = None
itemUsedByPlugin = None
dimensionalItemActivated = None
# GUI
gui = QtBind.init(__name__,pName)
lblMobs = QtBind.createLabel(gui,'#   MOB SAYACINDAN GORMEZDEN     #\n#     GELINECEK MOBLARI EKLEYIN      #',6,6)
tbxMobs = QtBind.createLineEdit(gui,"",6,35,100,20)
lstMobs = QtBind.createList(gui,6,56,176,203)
lstMobsData = []
btnAddMob = QtBind.createButton(gui,'btnAddMob_clicked',"    EKLE    ",107,34)
btnRemMob = QtBind.createButton(gui,'btnRemMob_clicked',"     SIL     ",55,258)
lblMonsterCounter = QtBind.createLabel(gui,"#                 MOB SAYACI                 #",520,6)
lstMonsterCounter = QtBind.createList(gui,520,23,197,237)
QtBind.append(gui,lstMonsterCounter,'ISIM (CESIT)') # Header
lblPreferences = QtBind.createLabel(gui,"#             MOB SAYACI TERCIHLERI            #",240,6)
lstIgnore = []
lstOnlyCount = []
_y = 26
lblGeneral = QtBind.createLabel(gui,'General (0)',215,_y)
cbxIgnoreGeneral = QtBind.createCheckBox(gui,'cbxIgnoreGeneral_clicked','GORMEZDEN GEL',320,_y)
cbxOnlyCountGeneral = QtBind.createCheckBox(gui,'cbxOnlyCountGeneral_clicked','SADECE SAY',425,_y)
_y+=20
lblChampion = QtBind.createLabel(gui,'Champion (1)',215,_y)
cbxIgnoreChampion = QtBind.createCheckBox(gui,'cbxIgnoreChampion_clicked','GORMEZDEN GEL',320,_y)
cbxOnlyCountChampion = QtBind.createCheckBox(gui,'cbxOnlyCountChampion_clicked','SADECE SAY',425,_y)
_y+=20
lblGiant = QtBind.createLabel(gui,'Giant (4)',215,_y)
cbxIgnoreGiant = QtBind.createCheckBox(gui,'cbxIgnoreGiant_clicked','GORMEZDEN GEL',320,_y)
cbxOnlyCountGiant = QtBind.createCheckBox(gui,'cbxOnlyCountGiant_clicked','SADECE SAY',425,_y)
_y+=20
lblTitan = QtBind.createLabel(gui,'Titan (5)',215,_y)
cbxIgnoreTitan = QtBind.createCheckBox(gui,'cbxIgnoreTitan_clicked','GORMEZDEN GEL',320,_y)
cbxOnlyCountTitan = QtBind.createCheckBox(gui,'cbxOnlyCountTitan_clicked','SADECE SAY',425,_y)
_y+=20
lblStrong = QtBind.createLabel(gui,'Strong (6)',215,_y)
cbxIgnoreStrong = QtBind.createCheckBox(gui,'cbxIgnoreStrong_clicked','GORMEZDEN GEL',320,_y)
cbxOnlyCountStrong = QtBind.createCheckBox(gui,'cbxOnlyCountStrong_clicked','SADECE SAY',425,_y)
_y+=20
lblElite = QtBind.createLabel(gui,'Elite (7)',215,_y)
cbxIgnoreElite = QtBind.createCheckBox(gui,'cbxIgnoreElite_clicked','GORMEZDEN GEL',320,_y)
cbxOnlyCountElite = QtBind.createCheckBox(gui,'cbxOnlyCountElite_clicked','SADECE SAY',425,_y)
_y+=20
lblUnique = QtBind.createLabel(gui,'Unique (8)',215,_y)
cbxIgnoreUnique = QtBind.createCheckBox(gui,'cbxIgnoreUnique_clicked','GORMEZDEN GEL',320,_y)
cbxOnlyCountUnique = QtBind.createCheckBox(gui,'cbxOnlyCountUnique_clicked','SADECE SAY',425,_y)
_y+=20
lblParty = QtBind.createLabel(gui,'Party (16)',215,_y)
cbxIgnoreParty = QtBind.createCheckBox(gui,'cbxIgnoreParty_clicked','GORMEZDEN GEL',320,_y)
cbxOnlyCountParty = QtBind.createCheckBox(gui,'cbxOnlyCountParty_clicked','SADECE SAY',425,_y)
_y+=20
lblChampionParty = QtBind.createLabel(gui,'ChampionParty (17)',215,_y)
cbxIgnoreChampionParty = QtBind.createCheckBox(gui,'cbxIgnoreChampionParty_clicked','GORMEZDEN GEL',320,_y)
cbxOnlyCountChampionParty = QtBind.createCheckBox(gui,'cbxOnlyCountChampionParty_clicked','SADECE SAY',425,_y)
_y+=20
lblGiantParty = QtBind.createLabel(gui,'GiantParty (20)',215,_y)
cbxIgnoreGiantParty = QtBind.createCheckBox(gui,'cbxIgnoreGiantParty_clicked','GORMEZDEN GEL',320,_y)
cbxOnlyCountGiantParty = QtBind.createCheckBox(gui,'cbxOnlyCountGiantParty_clicked','SADECE SAY',425,_y)
_y+=30
cbxAcceptForgottenWorld = QtBind.createCheckBox(gui,'cbxAcceptForgottenWorld_checked','FGW DAVETLERINI KABUL ET',240,_y)

# ______________________________ METHODLAR ______________________________ #
def cbxIgnoreGeneral_clicked(checked):
	Checkbox_Checked(checked,"lstIgnore",0) # 0 = General
def cbxOnlyCountGeneral_clicked(checked):
	Checkbox_Checked(checked,"lstOnlyCount",0)
def cbxIgnoreChampion_clicked(checked):
	Checkbox_Checked(checked,"lstIgnore",1) # 1 = Champion
def cbxOnlyCountChampion_clicked(checked):
	Checkbox_Checked(checked,"lstOnlyCount",1)
def cbxIgnoreGiant_clicked(checked):
	Checkbox_Checked(checked,"lstIgnore",4) # 4 = Giant
def cbxOnlyCountGiant_clicked(checked):
	Checkbox_Checked(checked,"lstOnlyCount",4)
def cbxIgnoreTitan_clicked(checked):
	Checkbox_Checked(checked,"lstIgnore",5) # 5 = Titan
def cbxOnlyCountTitan_clicked(checked):
	Checkbox_Checked(checked,"lstOnlyCount",5)
def cbxIgnoreStrong_clicked(checked):
	Checkbox_Checked(checked,"lstIgnore",6) # 6 = Strong
def cbxOnlyCountStrong_clicked(checked):
	Checkbox_Checked(checked,"lstOnlyCount",6)
def cbxIgnoreElite_clicked(checked):
	Checkbox_Checked(checked,"lstIgnore",7) # 7 = Elite
def cbxOnlyCountElite_clicked(checked):
	Checkbox_Checked(checked,"lstOnlyCount",7)
def cbxIgnoreUnique_clicked(checked):
	Checkbox_Checked(checked,"lstIgnore",8) # 8 = Unique
def cbxOnlyCountUnique_clicked(checked):
	Checkbox_Checked(checked,"lstOnlyCount",8)
def cbxIgnoreParty_clicked(checked):
	Checkbox_Checked(checked,"lstIgnore",16) # 16 = Party
def cbxOnlyCountParty_clicked(checked):
	Checkbox_Checked(checked,"lstOnlyCount",16)
def cbxIgnoreChampionParty_clicked(checked):
	Checkbox_Checked(checked,"lstIgnore",17) # 17 = ChampionParty
def cbxOnlyCountChampionParty_clicked(checked):
	Checkbox_Checked(checked,"lstOnlyCount",17)
def cbxIgnoreGiantParty_clicked(checked):
	Checkbox_Checked(checked,"lstIgnore",20) # 20 = GiantParty
def cbxOnlyCountGiantParty_clicked(checked):
	Checkbox_Checked(checked,"lstOnlyCount",20)
def cbxAcceptForgottenWorld_checked(checked):
	saveConfigs()
# CHECKBOXLARI GENELLESTIRME METHODU
def Checkbox_Checked(checked,gListName,mobType):
	gListReference = globals()[gListName]
	if checked:
		gListReference.append(mobType)
	else:
		gListReference.remove(mobType)
	saveConfigs()
# DOSYA YOLUNDAN DEVAM ET
def getPath():
	return get_config_dir()+pName+"\\"
# CHAR CONFIG YOLUNDAN DEVAM ET
def getConfig():
	return getPath()+character_data['server'] + "_" + character_data['name'] + ".json"
# VARSAYILAN CONFIG YUKLE
def loadDefaultConfig():
	# DATAYI TEMIZLE
	global lstMobsData,lstIgnore,lstOnlyCount
	lstMobsData = []
	QtBind.clear(gui,lstMobs)
	lstIgnore = []
	QtBind.setChecked(gui,cbxIgnoreGeneral,False)
	QtBind.setChecked(gui,cbxIgnoreChampion,False)
	QtBind.setChecked(gui,cbxIgnoreGiant,False)
	QtBind.setChecked(gui,cbxIgnoreTitan,False)
	QtBind.setChecked(gui,cbxIgnoreStrong,False)
	QtBind.setChecked(gui,cbxIgnoreElite,False)
	QtBind.setChecked(gui,cbxIgnoreUnique,False)
	QtBind.setChecked(gui,cbxIgnoreParty,False)
	QtBind.setChecked(gui,cbxIgnoreChampionParty,False)
	QtBind.setChecked(gui,cbxIgnoreGiantParty,False)
	lstOnlyCount = []
	QtBind.setChecked(gui,cbxOnlyCountGeneral,False)
	QtBind.setChecked(gui,cbxOnlyCountChampion,False)
	QtBind.setChecked(gui,cbxOnlyCountGiant,False)
	QtBind.setChecked(gui,cbxOnlyCountTitan,False)
	QtBind.setChecked(gui,cbxOnlyCountStrong,False)
	QtBind.setChecked(gui,cbxOnlyCountElite,False)
	QtBind.setChecked(gui,cbxOnlyCountUnique,False)
	QtBind.setChecked(gui,cbxOnlyCountParty,False)
	QtBind.setChecked(gui,cbxOnlyCountChampionParty,False)
	QtBind.setChecked(gui,cbxOnlyCountGiantParty,False)
	QtBind.setChecked(gui,cbxAcceptForgottenWorld,False)
# YUKLENEBILIR CONFIG VARSA YUKLE
def loadConfigs():
	loadDefaultConfig()
	if isJoined() and os.path.exists(getConfig()):
		data = {}
		with open(getConfig(),"r") as f:
			data = json.load(f)
		if "Ignore Names" in data:
			global lstMobsData
			lstMobsData = data["Ignore Names"]
			for name in lstMobsData:
				QtBind.append(gui,lstMobs,name)
		if "Ignore Types" in data:
			global lstIgnore
			for t in data["Ignore Types"]:
				if t == 8:
					QtBind.setChecked(gui,cbxIgnoreUnique,True)
				elif t == 7:
					QtBind.setChecked(gui,cbxIgnoreElite,True)
				elif t == 6:
					QtBind.setChecked(gui,cbxIgnoreStrong,True)
				elif t == 5:
					QtBind.setChecked(gui,cbxIgnoreTitan,True)
				elif t == 4:
					QtBind.setChecked(gui,cbxIgnoreGiant,True)
				elif t == 1:
					QtBind.setChecked(gui,cbxIgnoreChampion,True)
				elif t == 0:
					QtBind.setChecked(gui,cbxIgnoreGeneral,True)
				elif t == 16:
					QtBind.setChecked(gui,cbxIgnoreParty,True)
				elif t == 17:
					QtBind.setChecked(gui,cbxIgnoreChampionParty,True)
				elif t == 20:
					QtBind.setChecked(gui,cbxIgnoreGiantParty,True)
				else:
					continue
				lstIgnore.append(t)
		if "OnlyCount Types" in data:
			global lstOnlyCount
			for t in data["OnlyCount Types"]:
				if t == 8:
					QtBind.setChecked(gui,cbxOnlyCountUnique,True)
				elif t == 7:
					QtBind.setChecked(gui,cbxOnlyCountElite,True)
				elif t == 6:
					QtBind.setChecked(gui,cbxOnlyCountStrong,True)
				elif t == 5:
					QtBind.setChecked(gui,cbxOnlyCountTitan,True)
				elif t == 4:
					QtBind.setChecked(gui,cbxOnlyCountGiant,True)
				elif t == 1:
					QtBind.setChecked(gui,cbxOnlyCountChampion,True)
				elif t == 0:
					QtBind.setChecked(gui,cbxOnlyCountGeneral,True)
				elif t == 16:
					QtBind.setChecked(gui,cbxOnlyCountParty,True)
				elif t == 17:
					QtBind.setChecked(gui,cbxOnlyCountChampionParty,True)
				elif t == 20:
					QtBind.setChecked(gui,cbxOnlyCountGiantParty,True)
				else:
					continue
				lstOnlyCount.append(t)
		if 'Accept ForgottenWorld' in data and data['Accept ForgottenWorld']:
			QtBind.setChecked(gui,cbxAcceptForgottenWorld,True)
# TUM CONFIGI KAYDET
def saveConfigs():
	if isJoined():
		data = {}
		data['OnlyCount Types'] = lstOnlyCount
		data['Ignore Types'] = lstIgnore
		data['Ignore Names'] = lstMobsData
		data['Accept ForgottenWorld'] = QtBind.isChecked(gui,cbxAcceptForgottenWorld)
		with open(getConfig(),"w") as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))
# CHAR OYUNDA MI KONTROL ET
def isJoined():
	global character_data
	character_data = get_character_data()
	if not (character_data and "name" in character_data and character_data["name"]):
		character_data = None
	return character_data
# LSITEYE MOB EKLEME
def btnAddMob_clicked():
	global lstMobsData
	text = QtBind.text(gui,tbxMobs)
	if text and not ListContains(text,lstMobsData):
		lstMobsData.append(text)
		QtBind.append(gui,lstMobs,text)
		QtBind.setText(gui,tbxMobs,"")
		saveConfigs()
		log('Plugin: MOB EKLENDI: ['+text+']')
# LISTEDEN MOB SILME
def btnRemMob_clicked():
	global lstMobsData
	selected = QtBind.text(gui,lstMobs)
	if selected:
		lstMobsData.remove(selected)
		QtBind.remove(gui,lstMobs,selected)
		saveConfigs()
		log('Plugin: MOB SILINDI: ['+selected+']')
# LISTEDE METIN VARSA "TRUE" DEVAM ET
def ListContains(text,lst):
	text = text.lower()
	for i in range(len(lst)):
		if lst[i].lower() == text:
			return True
	return False
def QtBind_ItemsContains(text,lst):
	return ListContains(text,QtBind.getItems(gui,lst))
# BOTTAN TUM YAPILANDIRMALARI KULLANARAK MOBLARA SALDIRMA
def AttackMobs(wait,isAttacking,position,radius):
	count = getMobCount(position,radius)
	if count > 0:
		if not isAttacking:
			start_bot()
			log("Plugin: BU ALANDA ("+str(count)+") MOB KESILMEYE BASLANDI. Radius: "+(str(radius) if radius != None else "Max."))
		Timer(wait,AttackMobs,[wait,True,position,radius]).start()
	else:
		log("Plugin: TUM MOBLAR TEMIZLENDI!")
		conn = GetFilterConnection()
		cursor = conn.cursor()
		WaitPickableDrops(cursor)
		conn.close()
		stop_bot()
		if API_COMPATIBILITY:
			set_training_position(0,0,0)
		else:
			set_training_position(0,0,0,0)
		log("Plugin: SCRIPTTE GERI GIDILIYOR..")
		Timer(2.5,move_to,[position['x'],position['y'],position['z']]).start()
		Timer(5.0,start_bot).start()
# ETRAFTAKI TUM MOBLARI VARSAYILAN RANGE'E GORE SAY (60 RANGE CIVARI)
def getMobCount(position,radius):
	# Clear
	QtBind.clear(gui,lstMonsterCounter)
	QtBind.append(gui,lstMonsterCounter,'Name (Type)') # Header
	count = 0
	p = position if radius != None else None
	monsters = get_monsters()
	if monsters:
		for key, mob in monsters.items():
			if mob['type'] in lstIgnore:
				continue
			if len(lstOnlyCount) > 0:
				if not mob['type'] in lstOnlyCount:
					continue
			elif ListContains(mob['name'],lstMobsData):
				continue
			if radius != None:
				if round(GetDistance(p['x'], p['y'],mob['x'],mob['y']),2) > radius:
					continue
			QtBind.append(gui,lstMonsterCounter,mob['name']+' ('+str(mob['type'])+')')
			count+=1
	return count
# A NOKTASINDAN B NOKTASINA MESAFE HESAPLA
def GetDistance(ax,ay,bx,by):
	return ((bx-ax)**2 + (by-ay)**2)**(0.5)
# CONFIG FILTRESI ICIN BIR VERITABANI BAGLANTISI OLUSTUR
def GetFilterConnection():
	path = get_config_dir()+character_data['server']+'_'+character_data['name']+'.db3'
	return sqlite3.connect(path)
def IsPickable(filterCursor,ItemID):
	return filterCursor.execute('SELECT EXISTS(SELECT 1 FROM pickfilter WHERE id=? AND pick=1 LIMIT 1)',(ItemID,)).fetchone()[0]
def WaitPickableDrops(filterCursor,waiting=0):
	if waiting >= WAIT_DROPS_DELAY_MAX:
		log("Plugin: TOPLAMA ZAMAN ASIMINA UGRADI!")
		return
	drops = get_drops()
	if drops:
		drop = None
		for key in drops:
			value = drops[key]
			if IsPickable(filterCursor,value['model']):
				drop = value
				break
		if drop:
			log('Plugin: ITEMIN ALINMASI ICIN BEKLENIYOR : "'+drop['name']+'"...')
			sleep(1.0)
			WaitPickableDrops(filterCursor,waiting+1)

def GetDimensionalHole(Name):
	searchByName = Name != ''
	items = get_inventory()['items']
	for slot, item in enumerate(items):
		if item:
			match = False
			if searchByName:
				match = (Name == item['name'])
			else:
				itemData = get_item(item['model'])
				match = (itemData['tid1'] == 3 and itemData['tid2'] == 12 and itemData['tid3'] == 7)

			if match:
				item['slot'] = slot
				return item
	return None
def GetDimensionalPillarUID(Name):
	# Load all talking objects around
	npcs = get_npcs()
	if npcs:
		for uid, npc in npcs.items():
			item = get_item(npc['model'])
			if item and item['name'] == Name:
				return uid
	return 0
def EnterToDimensional(Name):
	uid = GetDimensionalPillarUID(Name)
	if uid:
		log('Plugin: DMH SECILIYOR..')
		packet = struct.pack('I',uid)
		inject_joymax(0x7045,packet,False)
		sleep(1.0)
		log('Plugin: FGW GIRILIYOR..')
		inject_joymax(0x704B,packet,False)
		packet += struct.pack('H',3)
		inject_joymax(0x705A,packet,False)
		Timer(5.0,start_bot).start()
		return
	log('Plugin: "'+Name+'" ETRAFINDA BULUNAMADI..!')

def GoDimensionalThread(Name):
	if dimensionalItemActivated:
		Name = dimensionalItemActivated['name']
		log('Plugin: '+( '"'+Name+'"' if Name else 'Dimensional Hole')+' HALEN ACIK!')
		EnterToDimensional(Name)
		return
	item = GetDimensionalHole(Name)
	if item:
		log('Plugin: KULLANIYOR: "'+item['name']+'"...')
		p = struct.pack('B',item['slot'])
		locale = get_locale()
		if locale == 22 or locale == 18: # 
			p += b'\x30\x0C\x0C\x07'
		else:
			p += b'\x6C\x3E'
		global itemUsedByPlugin
		itemUsedByPlugin = item
		inject_joymax(0x704C,p,True)
	else:
		log('Plugin: '+( '"'+Name+'"' if Name else 'Dimensional Hole')+' ENVANTERDE BULUNAMADI!')
# ______________________________ ETKINLIKLER ______________________________ #
def AttackArea(args):
	radius = None
	if len(args) >= 2:
		radius = round(float(args[1]),2)
	p = get_position()
	if getMobCount(p,radius) > 0:
		stop_bot()
		if API_COMPATIBILITY:
			set_training_position(p['region'], p['x'], p['y'])
		else:
			set_training_position(p['region'], p['x'], p['y'],p['z'])
		if radius != None:
			set_training_radius(radius)
		else:
			set_training_radius(100.0)
		Timer(0.001,AttackMobs,[COUNT_MOBS_DELAY,False,p,radius]).start()
	else:
		log("Plugin: ALANDA MOB BULUNAMADI. Radius: "+(str(radius) if radius != None else "Max."))
	return 0
def GoDimensional(args):
	stop_bot()
	name = ''
	if len(args) > 1:
		name = args[1]
	Timer(0.001,GoDimensionalThread,[name]).start()
	return 0
def joined_game():
	loadConfigs()
def handle_joymax(opcode, data):
	# SERVER_DIMENSIONAL_INVITATION_REQUEST
	if opcode == 0x751A:
		if QtBind.isChecked(gui,cbxAcceptForgottenWorld):
			packet = data[:4] # Request ID
			packet += b'\x00\x00\x00\x00' # unknown ID
			packet += b'\x01' # Accept flag
			inject_joymax(0x751C,packet,False)
			log('Plugin: FGW KATILIMI KABUL EDILDI..!')
	# SERVER_INVENTORY_ITEM_USE
	elif opcode == 0xB04C:
		global itemUsedByPlugin
		if itemUsedByPlugin:
			if data[0] == 1:
				log('Plugin: "'+itemUsedByPlugin['name']+'" ACILDI')
				global dimensionalItemActivated
				dimensionalItemActivated = itemUsedByPlugin
				def DimensionalCooldown():
					global dimensionalItemActivated
					dimensionalItemActivated = None
				Timer(DIMENSIONAL_COOLDOWN_DELAY,DimensionalCooldown).start()
				Timer(1.0,EnterToDimensional,[itemUsedByPlugin['name']]).start()
			else:
				log('Plugin: "'+itemUsedByPlugin['name']+'" ACILAMIYOR')
			itemUsedByPlugin = None
	return True
# PLUGIN YUKLENDI
log('Plugin: '+pName+' v'+pVersion+' BASARIYLA YUKLENDI')

if os.path.exists(getPath()):
	try:
		loadConfigs()
	except:
		log('Plugin: '+pName+' CONFIG DOSYASI YUKLEME HATASI..')
else:
	# CONFIG DOSYASI OLUSTURULDU
	os.makedirs(getPath())
	log('Plugin: '+pName+' CONFIG DOSYASI OLUSTURULDU..')
