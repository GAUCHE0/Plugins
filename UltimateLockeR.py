from phBot import *
import phBotChat
import struct
import time
import QtBind

pName = 'UltimateLockeR'
pVersion = '1.0'
pUrl = "https://raw.githubusercontent.com/GAUCHE0/Plugins/main/UltimateLockeR.py"

# KULLANICI AYARLARI
MATCH_PARTY_MASTER = "" 
MATCH_ACADEMY_MASTER = "" 
MATCH_REPLY_DELAY_MAX = 10 
QUESTION_PASSWORD = ""
QUESTION_MESSAGE = ""
# ______________________________ YUKLEME ______________________________ #

# KURESELLER
questionPartyTime = None
questionPartyCharName = ""
questionPartyRID = 0
questionPartyJID = 0
questionAcademyTime = None
questionAcademyCharName = ""
questionAcademyRID = 0
questionAcademyJID = 0

gui = QtBind.init(__name__,pName)
lblxControl01 = QtBind.createLabel(gui,' * GAUCHE TARAFINDAN DUZENLENMISTIR. \n * FEEDBACK SISTEMLI BIR YAZILIMDIR. \n * HATA VE ONERI BILDIRIMLERINIZI BANA ULASTIRABILIRSINIZ.\n         E-Mail : can.berk.cetin@hotmail.com.tr \n\n *NASIL CALISIR : \n PLUGIN DOSYASINI METIN BELGESI ILE  ACIN. \n MATCH_PARTY_MASTER = "PT MASTERI CHARIN NICKI" \n MATCH_ACADEMY_MASTER = "AKADEMI MASTERI CHARIN NICKI" \n MATCH_REPLY_DELAY_MAX = CEVAP VERME SURE GECIKMESI (SANIYE) \n QUESTION_MESSAGE = "SORU" \n QUESTION_PASSWORD = "CEVAP" \n \n SISTEM HATALARI SEBEBIYLE DEGISKENLER BU EKRANA YANSITILAMAMAKTADIR.\n BU SEBEPLE METIN BELGESINDE DUZENLEMENIZ GEREKMEKTEDIR..',21,11)
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
	if opcode == 0x706D and QUESTION_PASSWORD:
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
			phBotChat.Private(questionPartyCharName,QUESTION_MESSAGE)

		except:
			log("Plugin: AYRISTIRMA HATASI,BU SERVERDA KULLANILAMAZ..")
			log("DESTEK ICIN ILETISIME GECINIZ..")
			log("Data [" + ("None" if not data else ' '.join('{:02X}'.format(x) for x in data))+"] Locale ["+str(get_locale())+"]")
	# AKADEMI KATILIM GONDERDIGINDE
	elif opcode == 0x747E and QUESTION_PASSWORD:
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
			phBotChat.Private(questionAcademyCharName,QUESTION_MESSAGE)

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
	if not QUESTION_PASSWORD:
		return

	# SORULARI KONTROL ET

	if message == QUESTION_MESSAGE:
		# MASTER OLMAYANLARA CEVAP HAZIRLAMA
		if MATCH_PARTY_MASTER == charName or MATCH_ACADEMY_MASTER == charName:
			phBotChat.Private(charName,QUESTION_PASSWORD)
		else:
			phBotChat.Private(charName,"UZGUNUM MASTER DEGILSIN..")
		return

	# CEVAPLARI KONTROL ET

	if charName == questionPartyCharName:
		# PT KATILIM BEKLEME SURESI
		now = time.time()
		if now - questionPartyTime < MATCH_REPLY_DELAY_MAX:
			# CEVAP KONTROLÜ
			if message == QUESTION_PASSWORD:
				log("Plugin: "+charName+" SIFRE ILE PT'YE GIRDI")
				Inject_PartyMatchJoinResponse(questionPartyRID,questionPartyJID,True)
			else:
				log("Plugin: "+charName+" YANLIS SIFRE,PT REDDEDILDI.")
				Inject_PartyMatchJoinResponse(questionPartyRID,questionPartyJID,False)
			return

	if charName == questionAcademyCharName:
		# AKADEMI KATILIM BEKLEME SURESI 
		now = time.time()
		if now - questionAcademyTime < MATCH_REPLY_DELAY_MAX:
			# CEVAP KONTROLÜ
			if message == QUESTION_PASSWORD:
				log("Plugin: "+charName+" SIFRE ILE AKADEMIYE GIRDI")
				Inject_AcademyMatchJoinResponse(questionAcademyRID,questionAcademyJID,True)
			else:
				log("Plugin: "+charName+" YANLIS SIFRE,AKADEMI REDDEDILDI.")
				Inject_AcademyMatchJoinResponse(questionAcademyRID,questionAcademyJID,False)
			return

# PLUGIN YUKLENDI MESAJI
log('Plugin: '+pName+' v'+pVersion+' BASARIYLA YUKLENDI')
