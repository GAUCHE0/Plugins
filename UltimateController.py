from phBot import *

from threading import Timer

from time import localtime, strftime

import phBotChat

import QtBind

import struct

import random

import json

import os



pName = 'UltimateController'

pVersion = '1.3'

pUrl = "https://raw.githubusercontent.com/GAUCHE0/Plugins/main/UltimateController.py"



# ______________________________ Initializing ______________________________ #

# Globals

inGame = None

followActivated = False

followPlayer = ''

followDistance = 0

# KULLANICI ARAYUZU 1.SAYFA

gui = QtBind.init(__name__,pName+"1")

lblxControl01 = QtBind.createLabel(gui,' * GAUCHE TARAFINDAN DUZENLENMISTIR. \n * FEEDBACK SISTEMLI BIR YAZILIMDIR. \n * HATA VE ONERI BILDIRIMLERINIZI BANA ULASTIRABILIRSINIZ.\n         E-Mail : can.berk.cetin@hotmail.com.tr \n * LIDER LISTESINE KOMUT VERECEK CHARI EKLEYEREK KULLANILIR.\n\n DESTEK KOMUTLARI :\n - START : BOTU BASLAT.\n - STOP : BOTU DURDUR.\n - TRACE #OYUNCU : LIDERE YADA YAZDIGIN CHARA TRACE AT.\n - NOTRACE : TRACE DURDUR.\n - SETAREA #PosX? #PosY? #Range? #PosZ? :KASMA ALANI.\n - SETRADIUS #Radius? : RANGE DEGISTIR.\n - SIT : OTUR - KALK.\n - CAPE #RENK? : PVP MODU.\n - ZERK : ZERK HAZIRSA KULLAN.\n - RETURN : RETURN SCROLL KULLAN.\n - TP #A #B : A-B ARASI TELEPORT.\n - INJECT #Opcode #Encrypted? #Data? : PAKET ENJEKTE ET.\n - CHAT #CESIT #MESAJ : MESAJ GONDER.',21,11)

lblxControl02 = QtBind.createLabel(gui,' - MOVEON #RANGE? : MEVCUT KOOR. BELIRLE.\n - FOLLOW #OYUNCU? #MESAFE? :OYUN TRACE MODU.\n - NOFOLLOW : OYUN TRACE DURDUR.\n - PROFILE #ISIM? : PROFIL YUKLE.\n - JUMP : YATIR EFEKTÄ°.\n - DC : OYUNDAN DUSUR.\n - MOUNT #CESIT? : PET ACTIR.\n - DISMOUNT #CESIT? : PET KAPAT. \n - GETOUT : PARTIDEN AYRIL.\n - RECALL #SEHIR : SEHIRE KAYIT ET.\n - SETSCRIPT #DOSYA YOLU : SCRIPT DEGISTIR.\n - WALK : YURUME MODU.\n - RUN : KOSMA MODU ',345,101)

cbxEnabled = QtBind.createCheckBox(gui,'cbxDoNothing','TARGET MODUNU AKTIF ET',356,15)

cbxDefensive = QtBind.createCheckBox(gui,'cbxDoNothing','DEFANSIF MOD',356,30)

tbxLeaders = QtBind.createLineEdit(gui,"",511,11,100,20)

lstLeaders = QtBind.createList(gui,511,32,176,48)

btnAddLeader = QtBind.createButton(gui,'btnAddLeader_clicked',"    EKLE    ",612,10)

btnRemLeader = QtBind.createButton(gui,'btnRemLeader_clicked',"     SIL     ",560,79)

# KULLANICI ARAYUZU 2. SAYFA (+)

gui_ = QtBind.init(__name__,pName+"2")

lblxControl01 = QtBind.createLabel(gui_,' # DESTEK KOMUTLARI :\n - HXY : HOTAN FORTRESS TELEPORT KODU.\n - JXY : JANGAN FORTRESS TELEPORT KODU.\n #X : BULUNDUGUN GATE NUMARASI.\n #Y : GIDECEGIN GATE NUMRASI.\n \n - COME : MEYDAN OKUMA EFEKTI.\n - MERHABA : SELAMLAMA EFEKTI.\n - DRUG : DRUG SCROLL KULLANIMI.(ENVANTER 1.SAYFA 27.SLOT)\n - RES : RES SCROLL KULLANIMI.(ENVANTER 1.SAYFA 28.SLOT)\n - DAMAGEINC : DAMAGE INCREASE SCROLL KULLANIMI.(ENVANTER 1.SAYFA 29.SLOT)\n - DAMAGEABS : DAMAGE ABSORPTION SCROLL KULLANIMI.(ENVANTER 1.SAYFA 30.SLOT)\n - HP : HP SCROLL KULLANIMI.(ENVANTER 1.SAYFA 31.SLOT)\n - MP : MP SCROLL KULLANIMI.(ENVANTER 1.SAYFA 32.SLOT) \n * NOT: SCROLL KULLANIMI ICIN ENVANTERDE GEREKLI SLOTLARA KONULMALIDIR..',21,11)

lblxControl02 = QtBind.createLabel(gui_,' # TARGET MODU DESTEK KOMUTLARI : \n - TARGET ON : TARGET MODUNU AKTIF ET.\n - TARGET OFF : TARGET MODUNU DEAKTIF ET.\n - DEFF ON : DEFANS MODU AKTIF ET.\n - DEFF OFF : DEFANS MODU DEAKTIF ET. ',491,11)

lblxControl03 = QtBind.createLabel(gui_,' # JOV CAVE TELEPORT KODLARI : \n - CAVETHIEF : JOB CAVE THIEF KAPISI \n - CAVEHUNTER : JOB CAVE HUNTER KAPISI \n - SELKET : SELKET ODASINA GIRIS. \n - SELKETC : SELKET ODASINDAN CIKIS. \n - NEITH : NEITH ODASINA GIRIS. \n - NEITHC : NEITH ODASINDAN CIKIS. \n - ANUBIS : ANUBIS ODASINA GIRIS. \n - ANUBISC : ANUBIS ODASINDAN CIKIS. \n - ISIS : ISIS ODASINA GIRIS. \n - ISISC : ISIS ODASINDAN CIKIS.',491,101)

# ______________________________ Methods ______________________________ #

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

	# DATAYI TEMIZLEME

	QtBind.clear(gui,lstLeaders)

	QtBind.setChecked(gui,cbxEnabled,False)

	QtBind.setChecked(gui,cbxDefensive,False)

# ONCEKI KAYITLI TUM CONFIGLERI YUKLEME

def loadConfigs():

	loadDefaultConfig()

	if isJoined():

		# YUKLENEBILECEK CONFIG VAR MI KONTROL ET

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

	players = get_guild()

	if UniqueID == inGame['player_id']:

		return inGame['name']

	

	if players:

		for key, player in players.items():

			if player['player_id'] == UniqueID:

				return player['name']

	return ""

	players = get_guild_union()

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

				Timer(2.0, log, ("Plugin: Teleporting to ["+destination+"]")).start()

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

	log('Plugin: ENVANTERDE AT BULUNAMADI.')

	return False

# SECILMIS CESITTEKI PETI ACTIRMAK

def MountPet(petType):

	# ENVANTERDE PICK PET VARSA

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

	# Object skill action & Enabled xTargetSupport

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

	# KOMUTU VEREN LIDER LISTESINDE YA DA DC UZERINDE MI

	if player and lstLeaders_exist(player) or t == 100:

		# MESAJ KOMUTLARI

		if msg == "START":

			start_bot()

			log("Plugin: BOT BASLATILDI")

		elif msg == "STOP":

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

		elif msg.startswith("SETAREA"):

			# BOSLUK SILMEK ICIN

			msg = msg.rstrip()

			# API DATASI

			compatibility = tuple(map(int, (get_version().split(".")))) < (25,0,7)

			if msg == "SETAREA":

				p = get_position()

				if compatibility:

					set_training_position(p['region'], p['x'], p['y'])

				else:

					set_training_position(p['region'], p['x'], p['y'],p['z'])

				log("Plugin: MEVCUT POZISYON ATANDI. (X:%.1f,Y:%.1f)"%(p['x'],p['y']))

			else:

				try:

					# ARGUMENLERI KONTROL ET

					p = msg[7:].split()

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

					log("Plugin: TRADIUS DEGISTIRILDI. "+str(radius)+" m.")

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

			msg = msg[2:]

			if not msg:

				return

			# BOSLUK SILMEK ICIN

			msg = msg[1:]

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

					radius = int(float(msg[6:].split()[0]))

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

					log("Plugin:TAKIP MESAFESI YANLIS !")

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

				log("Plugin: PET ACILIYOR. ["+pet+"]")

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

		#GAUCHE EGLENCE KOMUTLARI

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

		#GAUCHE HOTAN FORTRESS KOMUTLARI

		elif msg == "H11":

			log("Plugin: HOTAN GATE1>GATE1")

			inject_joymax( 0x705A,b'\x02\x00\x00\x00\x02\x99\x00\x00\x00',False)

		elif msg == "H21":

			log("Plugin: HOTAN GATE2>GATE1")

			inject_joymax( 0x705A,b'\x03\x00\x00\x00\x02\x99\x00\x00\x00',False)

		elif msg == "H31":

			log("Plugin: HOTAN GATE3>GATE1")

			inject_joymax( 0x705A,b'\x04\x00\x00\x00\x02\x99\x00\x00\x00',False)

		elif msg == "H12":

			log("Plugin: HOTAN GATE1>GATE2")

			inject_joymax( 0x705A,b'\x02\x00\x00\x00\x02\x9A\x00\x00\x00',False)

		elif msg == "H22":

			log("Plugin: HOTAN GATE2>GATE2")

			inject_joymax( 0x705A,b'\x03\x00\x00\x00\x02\x9A\x00\x00\x00',False)

		elif msg == "H32":

			log("Plugin: HOTAN GATE3>GATE2")

			inject_joymax( 0x705A,b'\x04\x00\x00\x00\x02\x9A\x00\x00\x00',False)

		elif msg == "H13":

			log("Plugin: HOTAN GATE1>GATE3")

			inject_joymax( 0x705A,b'\x02\x00\x00\x00\x02\x9B\x00\x00\x00',False)

		elif msg == "H23":

			log("Plugin: HOTAN GATE2>GATE3")

			inject_joymax( 0x705A,b'\x03\x00\x00\x00\x02\x9B\x00\x00\x00',False)

		elif msg == "H33":

			log("Plugin: HOTAN GATE3>GATE3")

			inject_joymax( 0x705A,b'\x04\x00\x00\x00\x02\x9B\x00\x00\x00',False)

		elif msg == "H14":

			log("Plugin: HOTAN GATE1>GATE4")

			inject_joymax( 0x705A,b'\x02\x00\x00\x00\x02\x9C\x00\x00\x00',False)

		elif msg == "H24":

			log("Plugin: HOTAN GATE2>GATE4")

			inject_joymax( 0x705A,b'\x03\x00\x00\x00\x02\x9C\x00\x00\x00',False)

		elif msg == "H34":

			log("Plugin: HOTAN GATE3>GATE4")

			inject_joymax( 0x705A,b'\x04\x00\x00\x00\x02\x9C\x00\x00\x00',False)

	# GAUCHE JANGAN FORTRESS TELEPORTLARI

		elif msg == "J11":

			log("Plugin: JANGAN GATE1>GATE1")

			inject_joymax( 0x705A,b'\x03\x00\x00\x00\x02\x31\x00\x00\x00',False)

		elif msg == "J21":

			log("Plugin: JANGAN GATE2>GATE1")

			inject_joymax( 0x705A,b'\x04\x00\x00\x00\x02\x31\x00\x00\x00',False)

		elif msg == "J31":

			log("Plugin: JANGAN GATE3>GATE1")

			inject_joymax( 0x705A,b'\x05\x00\x00\x00\x02\x31\x00\x00\x00',False)

		elif msg == "J12":

			log("Plugin: JANGAN GATE1>GATE2")

			inject_joymax( 0x705A,b'\x03\x00\x00\x00\x02\x32\x00\x00\x00',False)

		elif msg == "J22":

			log("Plugin: JANGAN GATE2>GATE2")

			inject_joymax( 0x705A,b'\x04\x00\x00\x00\x02\x32\x00\x00\x00',False)

		elif msg == "J32":

			log("Plugin: JANGAN GATE3>GATE2")

			inject_joymax( 0x705A,b'\x05\x00\x00\x00\x02\x32\x00\x00\x00',False)

		elif msg == "J13":

			log("Plugin: JANGAN GATE1>GATE3")

			inject_joymax( 0x705A,b'\x03\x00\x00\x00\x02\x33\x00\x00\x00',False)

		elif msg == "J23":

			log("Plugin: JANGAN GATE2>GATE3")

			inject_joymax( 0x705A,b'\x04\x00\x00\x00\x02\x33\x00\x00\x00',False)

		elif msg == "J33":

			log("Plugin: JANGAN GATE3>GATE3")

			inject_joymax( 0x705A,b'\x05\x00\x00\x00\x02\x33\x00\x00\x00',False)

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

			log("Plugin: RES SCROLL KULLANILDI")

			inject_joymax( 0x704C,b'\x28\xED\x36',False)		
		#JOB CAVE TELEPORT KODLARI
		elif msg == "CAVETHIEF":

			log("Plugin: JOB CAVE(THIEF) ISINLANDI..")

			inject_joymax( 0x705A,b'\x03\x00\x00\x00\x02\xAE\x00\x00\x00',False)

		elif msg == "NEITH":

			log("Plugin: NEITH ODASINA ISINLANDI..")

			inject_joymax( 0x705A,b'\x0A\x89\x2D\x0B\x03\x00',False) #21.30 TELEPORTU
			inject_joymax( 0x705A,b'\x73\x31\x7D\x0B\x03\x00',False) #01.30 TELEPORTU
			inject_joymax( 0x705A,b'\x87\x59\x40\x0C\x03\x00',False) #11.30 TELEPORTU
		elif msg == "NEITHC":

			log("Plugin: NEITH ODASINDAN ISINLANDI..")

			inject_joymax( 0x705A,b'\x74\x31\x7D\x0B\x03\x00',False) #01.30 CIKIS TELEPORTU
			inject_joymax( 0x705A,b'\x88\x59\x40\x0C\x03\x00',False) #11.30 CIKIS TELEPORTU
		elif msg == "SELKET":

			log("Plugin: SELKET ODASINA ISINLANDI..")

			inject_joymax( 0x705A,b'\x08\x89\x2D\x0B\x03\x00',False) #21.30 TELEPORT
			inject_joymax( 0x705A,b'\x71\x31\x7D\x0B\x03\x00',False) #01.30 TELEPORTU
			inject_joymax( 0x705A,b'\x85\x59\x40\x0C\x03\x00',False) #11.30 TELEPORTU

		elif msg == "SELKETC":

			log("Plugin: SELKET ODASINDAN ISINLANDI..")

			inject_joymax( 0x705A,b'\x09\x89\x2D\x0B\x03\x00',False) #21.30 CIKIS TELEPORTU
			inject_joymax( 0x705A,b'\x72\x31\x7D\x0B\x03\x00',False) #01.30 CIKIS TELEPORTU
			inject_joymax( 0x705A,b'\x86\x59\x40\x0C\x03\x00',False) #11.30 CIKIS TELEPORTU

		elif msg == "ANUBIS":

			log("Plugin: ANUBIS ODASINA ISINLANDI..")

			inject_joymax( 0x705A,b'\x73\xA5\x54\x0B\x03\x00',False) #23.30 TELEPORTU
			inject_joymax( 0x705A,b'\x62\x70\xA4\x0B\x03\x00',False) #03.30 TELEPORTU

		elif msg == "ANUBISC":

			log("Plugin: ANUBIS ODASINDAN ISINLANDI..")

			inject_joymax( 0x705A,b'\x74\xA5\x54\x0B\x03\x00',False) #23.30 CIKIS TELEPORTU
			inject_joymax( 0x705A,b'\x63\x70\xA4\x0B\x03\x00',False) #03.30 CIKIS TELEPORTU
		elif msg == "ISIS":

			log("Plugin: ISIS ODASINA ISINLANDI..")
			
			inject_joymax( 0x705A,b'\x75\xA5\x54\x0B\x03\x00',False) #23.30 TELEPORTU
			inject_joymax( 0x705A,b'\x64\x70\xA4\x0B\x03\x00',False) #03.30 TELEPORTU
		elif msg == "ISISC":
		
			log("Plugin: ISIS ODASINDAN ISINLANDI..")
			
			inject_joymax( 0x705A,b'\x76\xA5\x54\x0B\x03\x00',False) #23.30 CIKIS TELEPORTU
			inject_joymax( 0x705A,b'\x65\x70\xA4\x0B\x03\x00',False) #03.30 CIKIS TELEPORTU
			
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

