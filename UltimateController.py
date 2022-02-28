from phBot import *
from threading import Timer
import phBotChat
import QtBind
import struct
import random
import json
import os
from time import sleep

pName = 'UltimateController'
pVersion = '0.1.2'
pUrl = "https://raw.githubusercontent.com/GAUCHE0/Plugins/main/UltimateController.py"
# ______________________________ KURULUM______________________________ #
# KURESELLER
inGame = None
followActivated = False
followPlayer = ''
followDistance = 0
# KULLANICI ARAYUZU 1.SAYFA
gui = QtBind.init(__name__,pName)
lblxControl01 = QtBind.createLabel(gui,'UltimateController:\n * GAUCHE TARAFINDAN DUZENLENMISTIR. \n * FEEDBACK SISTEMLI BIR YAZILIMDIR. \n * HATA VE ONERI BILDIRIMLERINIZI BANA ULASTIRABILIRSINIZ. \n\n * KOMUT DETAYLARI ICIN "UltimateINFO" PLUGININE GOZ ATABILIRSINIZ..',200,150)
cbxEnabled = QtBind.createCheckBox(gui,'cbxTarget','TARGET MODUNU AKTIF ET',156,15)
cbxDefensive = QtBind.createCheckBox(gui,'cbxDefensive','DEFANSIF MODU AKTIF ET',156,30)
tbxLeaders = QtBind.createLineEdit(gui,"",311,11,100,20)
lstLeaders = QtBind.createList(gui,311,32,176,48)
btnAddLeader = QtBind.createButton(gui,'btnAddLeader_clicked',"LIDER EKLE",412,10)
btnRemLeader = QtBind.createButton(gui,'btnRemLeader_clicked',"LIDER SIL",360,79)
# ______________________________METHODLAR ______________________________ #
# UltimateController CONFIG YOLU
def getPath():
	return get_config_dir()+pName+"\\"
# KAYITLI CONFIG YOLU (JSON)
def getConfig():
	return getPath()+inGame['server'] + "_" + inGame['name'] + ".json"
# KARAKTER OYUNDAYSA KONTROL ET.
def isJoined():
	global inGame
	inGame = get_character_data()
	if not (inGame and "name" in inGame and inGame["name"]):
		inGame = None
	return inGame
# VARSAYILAN CONFIG AYARI YUKLEME
def loadDefaultConfig():
	QtBind.clear(gui,lstLeaders)
	QtBind.setChecked(gui,cbxEnabled,False)
	QtBind.setChecked(gui,cbxDefensive,False)
# ONCEKI KAYITLI TUM CONFIGLERI YUKLEME
def loadConfigs():
	loadDefaultConfig()
	if isJoined():
		if os.path.exists(getConfig()):
			data = {}
			with open(getConfig(),"r") as f:
				data = json.load(f)
			if "Leaders" in data:
				for nickname in data["Leaders"]:
					QtBind.append(gui,lstLeaders,nickname)
			if "Defensive" in data and data['Defensive']:
				QtBind.setChecked(gui,cbxDefensive,True)
# LISTEDE ISIM VARSA DEVAM ETTIRME
def ListContains(text,lst):
	text = text.lower()
	for i in range(len(lst)):
		if lst[i].lower() == text:
			return True
	return False
# LISTEYE LIDER EKLEME
def btnAddLeader_clicked():
	if inGame:
		player = QtBind.text(gui,tbxLeaders)
		# LISTEDE CHAR VARSA
		if player and not ListContains(player,QtBind.getItems(gui,lstLeaders)):
			# Init dictionary
			data = {}
			# CONFIG VARSA YUKLE
			if os.path.exists(getConfig()):
				with open(getConfig(), 'r') as f:
					data = json.load(f)
			# YENI LIDER EKLE
			if not "Leaders" in data:
				data['Leaders'] = []
			data['Leaders'].append(player)
			# CONFIGI YENIDEN YAPILANDIR
			with open(getConfig(),"w") as f:
				f.write(json.dumps(data, indent=4, sort_keys=True))
			QtBind.append(gui,lstLeaders,player)
			QtBind.setText(gui, tbxLeaders,"")
			log('Plugin: LIDER EKLENDI ['+player+']')
# LISTEDEN LIDER SILME
def btnRemLeader_clicked():
	if inGame:
		selectedItem = QtBind.text(gui,lstLeaders)
		if selectedItem:
			if os.path.exists(getConfig()):
				data = {"Leaders":[]}
				with open(getConfig(), 'r') as f:
					data = json.load(f)
				try:
					# MEVCUT ISIM VARKEN EKLENEN AYNI ISMI SILME
					data["Leaders"].remove(selectedItem)
					with open(getConfig(),"w") as f:
						f.write(json.dumps(data, indent=4, sort_keys=True))
				except:
					pass # DOSYA YOKSA GORMEZDEN GEL
			QtBind.remove(gui,lstLeaders,selectedItem)
			log('Plugin: LIDER SILINDI ['+selectedItem+']')
# CHAR BENZERSIZ ID YANINDAYSA TARGET AL		
def getnickname(UniqueID):
	#players = get_players() BLOKE KALKARSA
	players = get_party()
	# Checking if UID is mine
	if UniqueID == inGame['player_id']:
		return inGame['name']	
	if players:
		for key, player in players.items():
			if player['player_id'] == UniqueID:
				return player['name']
	return ""
# TARGET SECMEYI ENJEKTE ETMEK
def Inject_SelectTarget(targetUID):
	packet = struct.pack('<I',targetUID)
	inject_joymax(0x7045,packet,False)
# LIDER LISTESINDEYSE DEVAM ET
def lstLeaders_exist(nickname):
	nickname = nickname.lower()
	players = QtBind.getItems(gui,lstLeaders)
	for i in range(len(players)):
		if players[i].lower() == nickname:
			return True
	return False
# TELEPORT PAKETLERINI YUKLEME
def inject_teleport(source,destination):
	t = get_teleport_data(source, destination)
	if t:
		npcs = get_npcs()
		for key, npc in npcs.items():
			if npc['name'] == source or npc['servername'] == source:
				log("Plugin: TELEPORT SECILDI ["+source+"]")
				# TELEPORT BULUNDUGUNDA SECMEK ICIN.
				inject_joymax(0x7045, struct.pack('<I', key), False)
				# 2 SANIYE GECIKMELI TELEPORT BASLATICI
				Timer(2.0, inject_joymax, (0x705A,struct.pack('<IBI', key, 2, t[1]),False)).start()
				Timer(2.0, log, ("Plugin: TP : ["+destination+"]")).start()
				return
		log('Plugin: NPC BULUNAMADI. YANLIS NPC ADI VEYA SERVER ADI.')
	else:
		log('Plugin: TELEPORT DATA BULUNAMADI. YANLIS TELEPORT ADI VEYA SERVER ADI.')
# MESAJ GONDERMEK
def handleChatCommand(msg):
	# CESIT BELIRLEME
	args = msg.split(' ',1)
	# CESIT BULUNAMADIGINDA
	if len(args) != 2 or not args[0] or not args[1]:
		return
	# UYUMLU MESAJ BULUNDUGUNDA
	t = args[0].lower()
	if t == 'private' or t == 'note':
		# UYUMLU MESAJ BULUNAMADIGINDA
		argsExtra = args[1].split(' ',1)
		if len(argsExtra) != 2 or not argsExtra[0] or not argsExtra[1]:
			return
		args.pop(1)
		args += argsExtra
	# MESAJ CESIDINI KONTROL ET
	sent = False
	if t == "all":
		sent = phBotChat.All(args[1])
	elif t == "private":
		sent = phBotChat.Private(args[1],args[2])
	elif t == "party":
		sent = phBotChat.Party(args[1])
	elif t == "guild":
		sent = phBotChat.Guild(args[1])
	elif t == "union":
		sent = phBotChat.Union(args[1])
	elif t == "note":
		sent = phBotChat.Note(args[1],args[2])
	elif t == "stall":
		sent = phBotChat.Stall(args[1])
	elif t == "global":
		sent = phBotChat.Global(args[1])
	if sent:
		log('Plugin: MESAJ "'+t+'" GONDERILDI.')
# MAX RADIUSTA LOKASYON BELIRLEME
def randomMovement(radiusMax=10):
	# KARISIK POZIYON BELIRLEME
	pX = random.uniform(-radiusMax,radiusMax)
	pY = random.uniform(-radiusMax,radiusMax)
	# SECILEN POZISYONU BELIRLEME
	p = get_position()
	pX = pX + p["x"]
	pY = pY + p["y"]
	# YENI POZISYONU GITME
	move_to(pX,pY,p["z"])
	log("Plugin: POZISYON DEGISTIRILDI. (X:%.1f,Y:%.1f)"%(pX,pY))
# MESAFE KULLANARAK TAKIP BASLATMAK
def start_follow(player,distance):
	if party_player(player):
		global followActivated,followPlayer,followDistance
		followPlayer = player
		followDistance = distance
		followActivated = True
		return True
	return False
# PARTIDEYSE KOMUTLARI AL
def party_player(player):
	players = get_party()
	if players:
		for p in players:
			if players[p]['name'] == player:
				return True
	return False
# PARTY UYESINE RETURN (ISRO)
def near_party_player(player):
	players = get_party()
	if players:
		for p in players:
			if players[p]['name'] == player and players[p]['player_id'] > 0:
				return players[p]
	return None
# A-B NOKTALARI ARASINDA MESEFA HESAPLAMA
def GetDistance(ax,ay,bx,by):
	return ((bx-ax)**2 + (by-ay)**2)**0.5
# TAKIBI DURDUKMAK
def stop_follow():
	global followActivated,followPlayer,followDistance
	result = followActivated
	# stop
	followActivated = False
	followPlayer = ""
	followDistance = 0
	return result
# PET ACTIRMAK
def MountHorse():
	items = get_inventory()['items']
	for slot, item in enumerate(items):
		if item:
			sn = item['servername']
			if '_C_' in sn:
				packet = struct.pack('B',slot)
				packet += struct.pack('H',4588 + (1 if sn.endswith('_SCROLL') else 0)) # Silk scroll
				inject_joymax(0x704C,packet,True)
				return True
	log('Plugin:  ENVANTERDE AT BULUNAMADI.')
	return False
# SECILMIS CESITTEKI PETI ACTIRMAK
def MountPet(petType):
	if petType == 'pick':
		return False
	elif petType == 'horse':
		return MountHorse()
	# TUM ACILABILEN PETLER ICIN (ISRO)
	pets = get_pets()
	if pets:
		for uid,pet in pets.items():
			if pet['type'] == petType:
				p = b'\x01' # mount flag
				p += struct.pack('I',uid)
				inject_joymax(0x70CB,p, False)
				return True
	return False
# PET KAPATMAYI DENEMESI ICIN
def DismountPet(petType):
	petType = petType.lower()
	# ENVANTERDE PICK PET VARSA
	if petType == 'pick':
		return False
	# TUM ACILABILEN PETLER ICIN (ISRO)
	pets = get_pets()
	if pets:
		for uid,pet in pets.items():
			if pet['type'] == petType:
				p = b'\x00'
				p += struct.pack('I',uid)
				inject_joymax(0x70CB,p, False)
				return True
	return False
# SECILEN NPC IDLERI DATADA MEVCUTSA
def GetNPCUniqueID(name):
	NPCs = get_npcs()
	if NPCs:
		name = name.lower()
		for UniqueID, NPC in NPCs.items():
			NPCName = NPC['name'].lower()
			if name == NPCName:
				return UniqueID
	return 0
# ISIM VEYA SERVERDA ITEMI BULMAK
def GetItemByExpression(_lambda,start=0,end=0):
	inventory = get_inventory()
	items = inventory['items']
	if end == 0:
		end = inventory['size']
	# check items between intervals
	for slot, item in enumerate(items):
		if start <= slot and slot <= end:
			if item:
				# Search by lambda
				if _lambda(item['name'],item['servername']):
					# Save slot location
					item['slot'] = slot
					return item
	return None
# ENVANTER BOŞ SLOT VARSA
def GetEmptySlot():
	items = get_inventory()['items']
	for slot, item in enumerate(items):
		if slot >= 13:
			if not item:
				return slot
	return -1
# ENVANTER HAREKET ENJEKSIYONU
def Inject_InventoryMovement(movementType,slotInitial,slotFinal,logItemName,quantity=0):
	p = struct.pack('<B',movementType)
	p += struct.pack('<B',slotInitial)
	p += struct.pack('<B',slotFinal)
	p += struct.pack('<H',quantity)
	# CLIENT_INVENTORY_ITEM_MOVEMENT
	inject_joymax(0x7034,p,False)
# ITEM GIYMEYI DENE
def EquipItem(item):
	itemData = get_item(item['model'])
	if itemData['tid1'] != 1:
		log('Plugin: '+item['name']+' cannot be equiped!')
		return
	t = itemData['tid2']
	if t == 1 or t == 2 or t == 3 or t == 9 or t == 10 or t == 11:
		t = itemData['tid3']
		# head
		if t == 1:
			Inject_InventoryMovement(0,item['slot'],0,item['name'])
		# shoulders
		elif t == 2:
			Inject_InventoryMovement(0,item['slot'],2,item['name'])
		# chest
		elif t == 3:
			Inject_InventoryMovement(0,item['slot'],1,item['name'])
		# pants
		elif t == 4:
			Inject_InventoryMovement(0,item['slot'],4,item['name'])
		# gloves
		elif t == 5:
			Inject_InventoryMovement(0,item['slot'],3,item['name'])
		# boots
		elif t == 6:
			Inject_InventoryMovement(0,item['slot'],5,item['name'])
	# shields
	elif t == 4:
		Inject_InventoryMovement(0,item['slot'],7,item['name'])
	# accesories ch/eu
	elif t == 5 or t == 12:
		t = itemData['tid3']
		# earring
		if t == 1:
			Inject_InventoryMovement(0,item['slot'],9,item['name'])
		# necklace
		elif t == 2:
			Inject_InventoryMovement(0,item['slot'],10,item['name'])
		# ring
		elif t == 3:
			if not GetItemByExpression(lambda s,n: True,11):
				Inject_InventoryMovement(0,item['slot'],12,item['name'])
			else:
				Inject_InventoryMovement(0,item['slot'],11,item['name'])
	# weapon ch/eu
	elif t == 6:
		Inject_InventoryMovement(0,item['slot'],6,item['name'])
	# job
	elif t == 7:
		Inject_InventoryMovement(0,item['slot'],8,item['name'])
	# avatar
	elif t == 13:
		t = itemData['tid3']
		# hat
		if t == 1:
			Inject_InventoryMovement(36,item['slot'],0,item['name'])
		# dress
		elif t == 2:
			Inject_InventoryMovement(36,item['slot'],1,item['name'])
		# accesory
		elif t == 3:
			Inject_InventoryMovement(36,item['slot'],2,item['name'])
		# flag
		elif t == 4:
			Inject_InventoryMovement(36,item['slot'],3,item['name'])
	# devil spirit
	elif t == 14:
		Inject_InventoryMovement(36,item['slot'],4,item['name'])
# ITEM CIKARTMAYI DENE
def UnequipItem(item):
	slot = GetEmptySlot()
	if slot != -1:
		Inject_InventoryMovement(0,item['slot'],slot,item['name'])
# ______________________________ ETKINLIKLER ______________________________ #
# PLUGIN BAGLANTISI
def connected():
	global inGame
	inGame = None
# CHAR OYUNA BAGLANDIGINDA
def joined_game():
		loadConfigs()
#TARGET TEMEL FONKSIYONLAR
def handle_joymax(opcode, data):
	if opcode == 0xB070 and QtBind.isChecked(gui,cbxEnabled):
		if data[0] == 1:
			SkillType = data[1] # 2 = Attack
			packetIndex = 7
			AttackerID = struct.unpack_from("<I",data,packetIndex)[0]
			packetIndex += 8
			if get_locale() == 18: # iSRO
				packetIndex += 4
			TargetID = struct.unpack_from("<I",data,packetIndex)[0]
			if SkillType == 2:
				nickname = getnickname(AttackerID)
				if nickname and ListContains(nickname,QtBind.getItems(gui,lstLeaders)):
					log("Plugin: BU KISIDEN : ["+nickname+"], TARGET ALINDI.")
					Inject_SelectTarget(TargetID)
				elif QtBind.isChecked(gui,cbxDefensive):
					nickname = getnickname(TargetID)
					if nickname and ListContains(nickname,QtBind.getItems(gui,lstLeaders)):
						log("Plugin: BU KISIYE : ["+nickname+"], SALDIRAN KISI TARGET ALINDI. ")
						Inject_SelectTarget(AttackerID)
	return True		
# TUM MESAJ KANALLARINDA KONTROL EDILEBILIR DURUMDA
def handle_chat(t,player,msg):
	# UNION CHATI GORMESI ICIN GUILD ISMI SILME
	if t == 11:
		msg = msg.split(': ',1)[1]
	# KOMUTU VEREN LIDER LISTESINDE YA DA DC UZERINDE MI
	if player and lstLeaders_exist(player) or t == 100:
		# MESAJ KOMUTLARI
		if msg == "BASLAT":
			start_bot()
			log("Plugin: BOT BASLATILDI")
		elif msg == "DURDUR":
			stop_bot()
			log("Plugin: BOT DURDURULDU.")
		elif msg.startswith("TRACE"):
			# BOSLUK SILMEK ICIN
			msg = msg.rstrip()
			if msg == "TRACE":
				if start_trace(player):
					log("Plugin: TRACE BU KISIYE BASLATILDI : ["+player+"]")
			else:
				msg = msg[5:].split()[0]
				if start_trace(msg):
					log("Plugin: TRACE BASLATILDI. ["+msg+"]")
		elif msg == "NOTRACE":
			stop_trace()
			log("Plugin: TRACE DURDURULDU.")
		elif msg.startswith("KORKUR"):
			# BOSLUK SILMEK ICIN
			msg = msg.rstrip()
			# API DATASI
			compatibility = tuple(map(int, (get_version().split(".")))) < (25,0,7)
			if msg == "KORKUR":
				p = get_position()
				if compatibility:
					set_training_position(p['region'], p['x'], p['y'])
				else:
					set_training_position(p['region'], p['x'], p['y'],p['z'])
				log("Plugin: MEVCUT POZISYON ATANDI. (X:%.1f,Y:%.1f)"%(p['x'],p['y']))
			else:
				try:
					# ARGUMENLERI KONTROL ET
					p = msg[6:].split()
					x = float(p[0])
					y = float(p[1])
					# SECILMEMISSE OTOMATIK KONTROL ET
					region = int(p[2]) if len(p) >= 3 else 0
					if compatibility:
						set_training_position(region,x,y)
					else:
						z = float(p[3]) if len(p) >= 4 else 0
						set_training_position(region,x,y,z)
					log("Plugin: BURAYA POZISYON ATANDI : (X:%.1f,Y:%.1f)"%(x,y))
				except:
					log("Plugin: YANLIS KOORDINAT !")
		elif msg.startswith("SETRADIUS"):
			# BOSLUK SILMEK ICIN
			msg = msg.rstrip()
			if msg == "SETRADIUS":
				# VARSAYILAN RADIUS KUR
				radius = 35
				set_training_radius(radius)
				log("Plugin: RADIUS DEGISTIRILDI : "+str(radius)+" m.")
			else:
				try:
					# RADIUS BELIRLEMEK ICIN
					radius = int(float(msg[9:].split()[0]))
					# PY HATASI ALMAMASI ICIN RADIUS LIMIT BELIRLEME
					radius = (radius if radius > 0 else radius*-1)
					set_training_radius(radius)
					log("Plugin: RADIUS DEGISTIRILDI. "+str(radius)+" m.")
				except:
					log("Plugin: YANLIS RADIUS DEGERI !")
		elif msg.startswith('SETSCRIPT'):
			# BOSLUK SILMEK ICIN
			msg = msg.rstrip()
			if msg == 'SETSCRIPT':
				# SCRIPT SIFIRLAMA
				set_training_script('')
				log('Plugin: SCRIPT YOLU SIFIRLANDI')
			else:
				# SCRIPT DEGISTIRMEK
				set_training_script(msg[9:])
				log('Plugin: SCRIPT YOLU DEGISTIRILDI.')
		elif msg.startswith('SETAREA '):
			# BOSLUK SILMEK ICIN
			msg = msg[8:]
			if msg:
				# KASMA ALANI DEGISTIRMEYI DENE
				if set_training_script(msg):
					log('Plugin: KASILMA ALANI DEGISTIRILDI : ['+msg+']')
				else:
					log('Plugin: KASILMA ALANI ['+msg+'] LISTEDE BULUNAMADI.')
		elif msg == "SIT":
			log("Plugin: OTUR/KALK")
			inject_joymax(0x704F,b'\x04',False)
		elif msg == "JUMP":
			# EGLENCE ICIN
			log("Plugin: YATIR YEDIN IYI MI.")
			inject_joymax(0x3091,b'\x0c',False)
		elif msg.startswith("CAPE"):
			# BOSLUK SILMEK ICIN
			msg = msg.rstrip()
			if msg == "CAPE":
				log("Plugin: VARSAYILAN PVP MODU (Yellow)")
				inject_joymax(0x7516,b'\x05',False)
			else:
				# CAPE TIPLERINI BELIRLEMEK ICIN
				cape = msg[4:].split()[0].lower()
				if cape == "off":
					log("Plugin: PVP MODUNDAN CIKILIYOR.")
					inject_joymax(0x7516,b'\x00',False)
				elif cape == "red":
					log("Plugin: PVP MODUNA GECILIYOR. (Red)")
					inject_joymax(0x7516,b'\x01',False)
				elif cape == "gray":
					log("Plugin: PVP MODUNA GECILIYOR. (Gray)")
					inject_joymax(0x7516,b'\x02',False)
				elif cape == "blue":
					log("Plugin: PVP MODUNA GECILIYOR. (Blue)")
					inject_joymax(0x7516,b'\x03',False)
				elif cape == "white":
					log("Plugin: PVP MODUNA GECILIYOR. (White)")
					inject_joymax(0x7516,b'\x04',False)
				elif cape == "yellow":
					log("Plugin: PVP MODUNA GECILIYOR. (Yellow)")
					inject_joymax(0x7516,b'\x05',False)
				else:
					log("Plugin: YANLIS CAPE RENGI !")
		elif msg == "ZERK":
			log("Plugin: ZERK MODUNA GECILIYOR.")
			inject_joymax(0x70A7,b'\x01',False)
		elif msg == "RETURN":
			# OLU OLUP OLMADIGINI KONTROL ETTIRMEK
			character = get_character_data()
			if character['hp'] == 0:
				# OLUYSE
				log('Plugin: SEHRE DONULUYOR.')
				inject_joymax(0x3053,b'\x01',False)
			else:
				log('Plugin: RETURN SCROLL KULLANILIYOR.')
				# SISTEME GORE COK CHAR KULLANILDIGINDA CPU KULLANIMI ARTAR
				Timer(random.uniform(0.5,2),use_return_scroll).start()
		elif msg.startswith("TP"):
			# DEVAMI YOKSA RETURN ATAR
			msg = msg[3:]
			if not msg:
				return
			# FARKLI CHARLARDAN KOMUT ALABILMESI ICIN
			split = ',' if ',' in msg else ' '
			# ARGUMANLARI CIKARTMA
			source_dest = msg.split(split)
			# TP ESNASINDA 2 ISMINDE DOGRULUGUNU KONTROL ETME
			if len(source_dest) >= 2:
				inject_teleport(source_dest[0].strip(),source_dest[1].strip())
		elif msg.startswith("INJECT "):
			msgPacket = msg[7:].split()
			msgPacketLen = len(msgPacket)
			if msgPacketLen == 0:
				log("Plugin: ENJEKTE PAKETTE HATA !")
				return
			# PAKET KONTROLU
			opcode = int(msgPacket[0],16)
			data = bytearray()
			encrypted = False
			dataIndex = 1
			if msgPacketLen >= 2:
				enc = msgPacket[1].lower()
				if enc == 'true' or enc == 'false':
					encrypted = enc == "true"
					dataIndex +=1
			# PAKET DATA OLUSTURMA VE ENJEKTE ETMEK
			for i in range(dataIndex, msgPacketLen):
				data.append(int(msgPacket[i],16))
			inject_joymax(opcode,data,encrypted)
			log("Plugin: PAKET ENJEKTE EDILIYOR.\nOpcode: 0x"+'{:02X}'.format(opcode)+" - Encrypted: "+("Yes" if encrypted else "No")+"\nData: "+(' '.join('{:02X}'.format(int(msgPacket[x],16)) for x in range(dataIndex, msgPacketLen)) if len(data) else 'None'))
		elif msg.startswith("CHAT "):
			handleChatCommand(msg[5:])
		elif msg.startswith("MOVEON"):
			if msg == "MOVEON":
				randomMovement()
			else:
				try:
					# split and parse movement radius
					radius = int(float(msg[6:].split()[0]))
					# to positive
					radius = (radius if radius > 0 else radius*-1)
					randomMovement(radius)
				except:
					log("Plugin: MAKSIMUM RADIUS YANLIS !")
		elif msg.startswith("FOLLOW"):
			# VARSAYILAN VERILER
			charName = player
			distance = 10
			if msg != "FOLLOW":
				# PARAMETRE KONTROLU
				msg = msg[6:].split()
				try:
					if len(msg) >= 1:
						charName = msg[0]
					if len(msg) >= 2:
						distance = float(msg[1])
				except:
					log("Plugin: TAKIP MESAFESI YANLIS !")
					return
			# TAKIP BASLATMA
			if start_follow(charName,distance):
				log("Plugin: TAKIP  ["+charName+"] ISIMLI KISIYE ["+str(distance)+"] MESAFEDEN TAKIP BASLATILDI.")					
		elif msg == "NOFOLLOW":
			if stop_follow():
				log("Plugin: TAKIP DURDURULDU.")
		elif msg.startswith("PROFILE"):
			if msg == "PROFILE":
				if set_profile('Default'):
					log("Plugin: VARSAYILAN PROFIL KURULDU.")
			else:
				msg = msg[7:]
				if set_profile(msg):
					log("Plugin: "+msg+" ISIMLI PROFIL KURULDU.")
		elif msg == "DC":
			log("Plugin: BAGLANTI KESILIYOR.")
			disconnect()
		elif msg.startswith("MOUNT"):
			# VARSAYILAN DEGERLER
			pet = "horse"
			if msg != "MOUNT":
				msg = msg[5:].split()
				if msg:
					pet = msg[0]
			# PET ACMAYI DENE
			if MountPet(pet):
				log("Plugin: PET ACILIYOR.  ["+pet+"]")
		elif msg.startswith("DISMOUNT"):
			# VARSAYILAN DEGERLER
			pet = "horse"
			if msg != "DISMOUNT":
				msg = msg[8:].split()
				if msg:
					pet = msg[0]
			# PET KAPATMAYI DENEt
			if DismountPet(pet):
				log("Plugin: PET KAPATILIYOR. ["+pet+"]")
		elif msg == "GETOUT":
			# PARTIDE MI KONTROL ET
			if get_party():
				# CIKMASI ICIN
				log("Plugin: PARTIDEN AYRILIYOR.")
				inject_joymax(0x7061,b'',False)
		elif msg.startswith("RECALL "):
			msg = msg[7:]
			if msg:
				npcUID = GetNPCUniqueID(msg)
				if npcUID > 0:
					log("Plugin: YENIDEN DOGMA NOKTASI AYARLANIYOR : \""+msg.title()+"\"...")
					inject_joymax(0x7059, struct.pack('I',npcUID), False)
		elif msg.startswith("GIY "):
			msg = msg[6:]
			if msg:
				item = GetItemByExpression(lambda n,s: msg in n or msg == s,13)
				if item:
					EquipItem(item)
				log('Plugin: ITEM GIYILIYOR..')
		elif msg.startswith("CIKART "):
			msg = msg[8:]
			if msg:
				item = GetItemByExpression(lambda n,s: msg in n or msg == s,0,12)
				if item:
					UnequipItem(item)
				log('Plugin: ITEM CIKARILIYOR..')
		elif msg.startswith("REVERSE "):
			msg = msg[8:]
			if msg:
				msg = msg.split(' ',1)
				if msg[0] == 'RETURN':
					if reverse_return(0,''):
						log('Plugin: SON RETURN KULLANIM NOKTASINA REVERSE KULLANILIYOR')
				elif msg[0] == 'OLUM':
					if reverse_return(1,''):
						log('Plugin: SON OLUM NOKTASINA REVERSE KULLANILIYOR')
				elif msg[0] == 'PLAYER':
					if len(msg) >= 2:
						if reverse_return(2,msg[1]):
							log('Plugin: BU KISIYE REVERSE KULLANILIYOR : "'+msg[1]+'"')
				elif msg[0] == 'ALAN':
					if len(msg) >= 2:
						if reverse_return(3,msg[1]):
							log('Plugin: BU ALANA REVERSE ATILIYOR : "'+msg[1]+'" ')
	# GAUCHE EGLENCE KOMUTLARI
		if msg == "WALK":
			log("Plugin: YURUME MODU AKTIF")
			inject_joymax( 0x704F,b'\x02',False)
		elif msg == "RUN":
			log("Plugin: KOSMA MODU AKTIF")
			inject_joymax( 0x704F,b'\x03',False)
		elif msg == "COME":
			log("Plugin: COME ON BABE")
			inject_joymax( 0x3091,b'\x02',False)
		elif msg == "MERHABA":
			log("Plugin: MERHABA CINIM ")
			inject_joymax( 0x3091,b'\x00',False)
	# GAUCHE TARGET KODLARI
		elif msg == "TARGET ON":
			log("Plugin: TARGET AKTIF EDILDI.")
			QtBind.setChecked(gui,cbxEnabled,True)
		elif msg == "TARGET OFF":
			log("Plugin: TARGET DEAKTIF EDILDI.")
			QtBind.setChecked(gui,cbxEnabled,False)
		elif msg == "DEFF ON":
			log("Plugin: DEFANS MOD AKTIF EDILDI.")
			QtBind.setChecked(gui,cbxDefensive,True)
		elif msg == "DEFF OFF":
			log("Plugin: DEFANS MOD DEAKTIF EDILDI.")
			QtBind.setChecked(gui,cbxDefensive,False)
	# GAUCHE SCROLL KULLANIMLARI
		elif msg == "DRUG":
			log("Plugin: DRUG KULLANILDI")
			inject_joymax( 0x704C,b'\x27\xED\x0E',False)
		elif msg == "DAMAGEINC":
			log("Plugin: %20 DAMAGE INCREASE SCROLL KULLANILDI.")
			inject_joymax( 0x704C,b'\x29\xED\x0E',False)
		elif msg == "DAMAGEABS":
			log("Plugin: %20 DAMAGE ABSORPTION SCROLL KULLANILDI.")
			inject_joymax( 0x704C,b'\x2A\xED\x0E',False)
		elif msg == "MP":
			log("Plugin: MP+2800 SCROLL KULLANILDI.")
			inject_joymax( 0x704C,b'\x2C\xED\x0E',False)
		elif msg == "HP":
			log("Plugin: HP+2800 SCROLL KULLANILDI.")
			inject_joymax( 0x704C,b'\x2B\xED\x0E',False)
		elif msg == "RES":
			log("Plugin: RES SCROLL KULLANILDI.")
			inject_joymax( 0x704C,b'\x28\xED\x36',False)	
		elif msg == "ZERKPOT":
			log("Plugin: ZERK POTU ACILDI VE KULLANILDI.")
			inject_joymax( 0x704C,b'\x26\xEC\x76',False)
			Timer(2.0, inject_joymax, (0x715F,b'\x8B\x5D\x00\x00\x81\x5D\x00\x00',False)).start()
		elif msg == "PET":
			log("Plugin: PET ACILDI.")
			inject_joymax( 0x704C,b'\x22\xCD\x08',False)
#Hotan Fortress Teleport Kodları
		elif msg == "H11":
			log("Plugin: HOTAN FORTRESS 1>1")
			inject_joymax( 0x705A,b'\x02\x00\x00\x00\x02\x99\x00\x00\x00\x02\x00\x00\x00',False)
		elif msg == "H12":
			log("Plugin: HOTAN FORTRESS 1>2")
			inject_joymax( 0x705A,b'\x02\x00\x00\x00\x02\x9A\x00\x00\x00\x02\x00\x00\x00',False)
		elif msg == "H13":
			log("Plugin: HOTAN FORTRESS 1>3")
			inject_joymax( 0x705A,b'\x02\x00\x00\x00\x02\x9B\x00\x00\x00\x02\x00\x00\x00',False)
		elif msg == "H14":
			log("Plugin: HOTAN FORTRESS 1>4")
			inject_joymax( 0x705A,b'\x02\x00\x00\x00\x02\x9C\x00\x00\x00\x02\x00\x00\x00',False)
		elif msg == "H21":
			log("Plugin: HOTAN FORTRESS 2>1")
			inject_joymax( 0x705A,b'\x03\x00\x00\x00\x02\x99\x00\x00\x00\x03\x00\x00\x00',False)
		elif msg == "H22":
			log("Plugin: HOTAN FORTRESS 2>2")
			inject_joymax( 0x705A,b'\x03\x00\x00\x00\x02\x9A\x00\x00\x00\x03\x00\x00\x00',False)
		elif msg == "H23":
			log("Plugin: HOTAN FORTRESS 2>3")
			inject_joymax( 0x705A,b'\x03\x00\x00\x00\x02\x9B\x00\x00\x00\x03\x00\x00\x00',False)
		elif msg == "H24":
			log("Plugin: HOTAN FORTRESS 2>4")
			inject_joymax( 0x705A,b'\x03\x00\x00\x00\x02\x9C\x00\x00\x00\x03\x00\x00\x00',False)
		elif msg == "H31":
			log("Plugin: HOTAN FORTRESS 3>1")
			inject_joymax( 0x705A,b'\x04\x00\x00\x00\x02\x99\x00\x00\x00\x04\x00\x00\x00',False)
		elif msg == "H32":
			log("Plugin: HOTAN FORTRESS 3>2")
			inject_joymax( 0x705A,b'\x04\x00\x00\x00\x02\x9A\x00\x00\x00\x04\x00\x00\x00',False)
		elif msg == "H33":
			log("Plugin: HOTAN FORTRESS 3>3")
			inject_joymax( 0x705A,b'\x04\x00\x00\x00\x02\x9B\x00\x00\x00\x04\x00\x00\x00',False)
		elif msg == "H34":
			log("Plugin: HOTAN FORTRESS 3>4")
			inject_joymax( 0x705A,b'\x04\x00\x00\x00\x02\x9C\x00\x00\x00\x04\x00\x00\x00',False)
#Jangan Fortress Teleport Kodları
		elif msg == "J11":
			log("Plugin: JANGAN FORTRESS 1>1")
			inject_joymax( 0x705A,b'\x03\x00\x00\x00\x02\x31\x00\x00\x00\x03\x00\x00\x00',False)
		elif msg == "J12":
			log("Plugin: JANGAN FORTRESS 1>2")
			inject_joymax( 0x705A,b'\x03\x00\x00\x00\x02\x32\x00\x00\x00\x03\x00\x00\x00',False)
		elif msg == "J13":
			log("Plugin: JANGAN FORTRESS 1>3")
			inject_joymax( 0x705A,b'\x03\x00\x00\x00\x02\x33\x00\x00\x00\x03\x00\x00\x00',False)
		elif msg == "J21":
			log("Plugin: JANGAN FORTRESS 2>1")
			inject_joymax( 0x705A,b'\x04\x00\x00\x00\x02\x31\x00\x00\x00\x04\x00\x00\x00',False)
		elif msg == "J22":
			log("Plugin: JANGAN FORTRESS 2>2")
			inject_joymax( 0x705A,b'\x04\x00\x00\x00\x02\x32\x00\x00\x00\x04\x00\x00\x00',False)
		elif msg == "J23":
			log("Plugin: JANGAN FORTRESS 2>3")
			inject_joymax( 0x705A,b'\x04\x00\x00\x00\x02\x33\x00\x00\x00\x04\x00\x00\x00',False)
		elif msg == "J31":
			log("Plugin: JANGAN FORTRESS 3>1")
			inject_joymax( 0x705A,b'\x05\x00\x00\x00\x02\x31\x00\x00\x00\x05\x00\x00\x00',False)
		elif msg == "J32":
			log("Plugin: JANGAN FORTRESS 3>2")
			inject_joymax( 0x705A,b'\x05\x00\x00\x00\x02\x32\x00\x00\x00\x05\x00\x00\x00',False)
		elif msg == "J33":
			log("Plugin: JANGAN FORTRESS 3>3")
			inject_joymax( 0x705A,b'\x05\x00\x00\x00\x02\x33\x00\x00\x00\x05\x00\x00\x00',False)
# 500MS DE BIR KONTROL ETTIRME
def event_loop():
	if inGame and followActivated:
		player = near_party_player(followPlayer)
		# YANINDA MI
		if not player:
			return
		# MESAFE KONTROLU
		if followDistance > 0:
			p = get_position()
			playerDistance = round(GetDistance(p['x'],p['y'],player['x'],player['y']),2)
			# HAREKET ALGILAMA
			if followDistance < playerDistance:
				# X Y BELIRLEME
				x_unit = (player['x'] - p['x']) / playerDistance
				y_unit = (player['y'] - p['y']) / playerDistance
				# MESEFAYE YURUME
				movementDistance = playerDistance-followDistance
				log("TAKIPTE : "+followPlayer+"...")
				move_to(movementDistance * x_unit + p['x'],movementDistance * y_unit + p['y'],0)
		else:
			# NEGATIF NUMARALARI GORMEZDEN GEL
			log("TAKIPTE : "+followPlayer+"...")
			move_to(player['x'],player['y'],0)
# PLUGIN YUKLENIRSE
log("Plugin: "+pName+" v"+pVersion+" BASARIYLA YUKLENDI.")
if os.path.exists(getPath()):
	# CONFIG YUKLEME
	loadConfigs()
else:
	# CONFIG DOSYASI OLUSTURMA
	os.makedirs(getPath())
	log('Plugin: '+pName+' CONFIG KLASORU OLUSTURULDU.')
