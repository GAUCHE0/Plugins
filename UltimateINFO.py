from phBot import *
import QtBind
from threading import Timer
import struct
import random
import json
import os
import subprocess

pVersion = '0.0.5'
pName = 'UltimateINFO'
pUrl = 'https://raw.githubusercontent.com/GAUCHE0/Plugins/main/UltimateINFO.py'

#GUI YAPILANDIRMASI
gui = QtBind.init(__name__,pName)
lblInfo = QtBind.createLabel(gui,"ULTIMATE PLUGINLERI HAKKINDA ACIKLAMALAR:",21,11)
lblInfo2 = QtBind.createLabel(gui," - SPECIAL THANKS TO |JellyBitz| ABOUT PYTHON DEVELOPMENT..",400,11)
btnUltimateController = QtBind.createButton(gui,'btnUltimateController_clicked',"  UltimateController  ",493,30)
btnUltimateChat = QtBind.createButton(gui,'btnUltimateChat_clicked',"      UltimateChat      ",493,55)
btnUltimateLocker = QtBind.createButton(gui,'btnUltimateLocker_clicked',"     UltimateLockeR   ",493,80)
btnUltimatePacketTool = QtBind.createButton(gui,'btnUltimatePacketTool_clicked',"  UltimatePacketTooL",493,105)
btnUltimateUpdater = QtBind.createButton(gui,'btnUltimateUpdater_clicked',"    UltimateUpdater   ",493,130)
btnUltimateTombala = QtBind.createButton(gui,'btnUltimateTombala_clicked',"    UltimateTombala    ",493,155)
btnUltimateArena = QtBind.createButton(gui,'btnUltimateArena_clicked',"      UltimateArena     ",493,180)
btnUltimateAcademy = QtBind.createButton(gui,'btnUltimateAcademy_clicked',"    UltimateAcademy   ",493,205)
btnUltimatechanger = QtBind.createButton(gui,'btnUltimateChanger_clicked',"    UltimateChanger   ",601,30)
btnUltimateItemManager = QtBind.createButton(gui,'btnUltimateItemManager_clicked',"  UltimateItemManager ",601,55)
btnUltimateTranslator = QtBind.createButton(gui,'btnUltimateTranslator_clicked',"  UltimateTranslator ",601,80)
btnUltimateDungeon = QtBind.createButton(gui,'btnUltimateDungeon_clicked',"  UltimateDungeon ",601,105)
btnIletisim = QtBind.createButton(gui,'btnIletisim_clicked',"   GAUCHE ILETISIM   ",547,250)
lstInfo = QtBind.createList(gui,21,30,470,250)
#BUTON ISLEVLERI	
def btnUltimateController_clicked():
	QtBind.clear(gui,lstInfo)
	QtBind.append(gui,lstInfo,'UltimateController:\n   # BU PLUGIN LIDER LISTESINE EKLENMIS CHARLARIN CHAT EKRANINDAN DIGER\nCHARLARA CESITLI ISLEMLER YAPTIRIR.\n# GENEL DESTEK KOMUTLARI:\n - BASLAT : BOTU BASLAT.\n - DURDUR : BOTU DURDUR.\n - TRACE #OYUNCU : LIDERE YADA YAZDIGIN CHARA TRACE AT.\n - NOTRACE : TRACE DURDUR.\n - ZERK : ZERK HAZIRSA KULLAN.\n - RETURN : RETURN SCROLL KULLAN.\n - TP #A #B : A-B ARASI TELEPORT.\n - CHAT #CESIT #MESAJ : MESAJ GONDER\n - KUR #PosX? #PosY? #Range? #PosZ? :KASMA ALANI KURMAK.\n - SETRADIUS #Radius? : RANGE DEGISTIR.\n - CAPE #RENK? : PVP MODU.')
	QtBind.append(gui,lstInfo,'- INJECT #Opcode #Encrypted? #Data? : PAKET ENJEKTE ET.\n# FORTRESS DESTEK KOMUTLARI:\n - HXY : HOTAN FORTRESS TELEPORT KODU.\n - JXY : JANGAN FORTRESS TELEPORT KODU.\n    # X : BULUNDUGUN GATE NUMARASI.\n    # Y : GIDECEGIN GATE NUMARASI.\n# SCROLL KOMUTLARI:\n - DRUG : DRUG SCROLL KULLANIMI.(ENVANTER 1.SAYFA 27.SLOT)\n - RES : RES SCROLL KULLANIMI.(ENVANTER 1.SAYFA 28.SLOT)\n - DAMAGEINC : DAMAGE INCREASE SCROLL KULLANIMI.\n(ENVANTER 1.SAYFA 29.SLOT)\n - DAMAGEABS : DAMAGE ABSORPTION SCROLL KULLANIMI.\n(ENVANTER 1.SAYFA 30.SLOT)\n - HP : HP SCROLL KULLANIMI.(ENVANTER 1.SAYFA 31.SLOT)\n - MP : MP SCROLL KULLANIMI.(ENVANTER 1.SAYFA 32.SLOT)')
	QtBind.append(gui,lstInfo,'#NOT: SCROLL KULLANIMI ICIN ENVANTERDE GEREKLI SLOTLARA KONULMALIDIR.\n # EGLENCE KOMUTLARI:\n - SIT : OTUR - KALK.\n - COME : MEYDAN OKUMA EFEKTI.\n- MERHABA : SELAMLAMA EFEKTI.\n # TARGET MODU :\nLIDERIN SECTIGI TARGETI OTOMATIK SECME FONKSIYONUDUR.\nDEFANSIF MODU SECENEGI ILE LIDERE ATACK YAPAN KISIYE TARGET ALINABILIR.\n# TARGET MODU DESTEK KOMUTLARI: \n - TARGET ON : TARGET MODUNU AKTIF ET.\n - TARGET OFF : TARGET MODUNU DEAKTIF ET.\n - DEFF ON : DEFANS MODU AKTIF ET.\n - DEFF OFF : DEFANS MODU DEAKTIF ET.')
def btnUltimateChat_clicked():
	QtBind.clear(gui,lstInfo)
	QtBind.append(gui,lstInfo,'UltimateChat:\n   # BU PLUGIN ILE 10 SANIYEDE BIR SPAM MESAJ ATILABILIR, SECILEN KOSULA GORE\nISTEDIGINIZ CHAT EKRANINA MESAJ GONDEREBILIRSINIZ.\n   # BUNA EK OLARAK SCRIPTE EKLEYECEGINIZ BASIT BIR KODLA SCRIPT ESNASINDA\nOTO MESAJ ATTIRABILIRSINIZ..\n   # ORNEK: "chat,all,SELAM" VEYA "chat,private,GAUCHE,SELAM"')
def btnUltimateLocker_clicked():
	QtBind.clear(gui,lstInfo)
	QtBind.append(gui,lstInfo,'UltimateLockeR:\n    # BU PLUGIN AKADEMI VE PARTI LISTELERINDEN OTOMATIK GIRIS YAPARKEN\nISTENMEYEN KISILERIN GIRMESINI ENGELLEMEK ICIN TASARLANMISTIR.\n    # BIR NEVI SIFRELEME SISTEMI OLUP, MASTER CHARIN BELIRLENEN SORUYU\nSORMASININ ARDINDAN GIRIS YAPAN CHARIN DOGRU CEVABI VERMESIYLE CALISIR.\n    # KURULUM :\n - PARTI MASTER: PARTY MASTERI OLACAK CHARIN ADI.\n - AKADEMI MASTER: AKADEMI MASTERI OLACAK CHARIN ADI.\n - SORU: CHAT EKRANINDA SORDURMAK ISTEDIGIN SORU.\n - CEVAP: SORULAN SORUYA VERILMESINI ISTEDIGIN YANIT.\n(SIFRE NITELIGINDE OLUP BASKA BIR KISI ILE PAYLASMAYIN.)')
def btnUltimatePacketTool_clicked():
	QtBind.clear(gui,lstInfo)
	QtBind.append(gui,lstInfo,'UltimatePacketTooL:\n    # BU PLUGIN CLIENTTEN SERVERA GONDERILEN OPCODE PAKETLERINI VEYA\nSERVERDAN CLIENTE GELEN OPCODE PAKETLERINI GOSTERMEKTEDIR.\n    # EK OLARAK CLIENTTEN SERVERA OPCODE ENEJEKTE EDEBILIR VE CEVRENIZDEKI\nNPCLERIN DATALARINA ULASABILIRSINIZ.')
def btnUltimateUpdater_clicked():
	QtBind.clear(gui,lstInfo)
	QtBind.append(gui,lstInfo,'UltimateUpdater:\n    # BU PLUGIN BILGSAYARINIZDA GITHUB.COM UZERINDEN YAYINLANAN\nHERHANGI BIR YAZILIMCININ PLUGININI BULDUGU TAKTIRDE GUNCELLER..\n KULLANIMI:\n"GUNCELLEMELERI KONTROL ET" BUTONUNA BASTIKTAN SONRA;\n LISTEDE "GUNCELLEME BULUNDU" YAZAN PLUGINLERIN UZERINE TIKLAYIP,\n"SECILEN PLUGINI GUNCELLE" BUTONUNA BASINIZ.\n    # ISLEM BITIMINDE BOTUNUZU YENIDEN BASLATIRSANIZ VEYA "PLUGIN"\nSEKMESINDE "YENIDEN YUKLE" BUTONUNA TIKLARSANIZ PLUGININ SON\nVERSIYONUNU KULLANMAYA BASLAYABILIRSINIZ..')
def btnUltimateTombala_clicked():
	QtBind.clear(gui,lstInfo)
	QtBind.append(gui,lstInfo,'UltimateTombala:\n    # BU PLUGIN ILE MEVCUT MANAGER UZERINDEN GIRILEN BUTUN CHARLAR\nOTOMATIK TOMBALAYA KAYIT YAPARLAR.')
def btnUltimateArena_clicked():
	QtBind.clear(gui,lstInfo)
	QtBind.append(gui,lstInfo,'UltimateArena:\n    # BU PLUGIN ILE MEVCUT MANAGER UZERINDEN GIRILEN BUTUN CHARLAR\n OTO ARENAYA KAYIT YAPARLAR.\n\n - RANDOM ARENA\n - PT ARENA\n - JOB ARENA\n - GUILD ARENA')
def btnUltimateAcademy_clicked():
	QtBind.clear(gui,lstInfo)
	QtBind.append(gui,lstInfo,'UltimateAcademy:\n    # BU PLUGIN ILE;\n - CHAR OLUSTURMA (ISTEDIGINIZ IRKTA, NICKLE VE SIRAYLA),\n - CHAR SILME (40-100 LVL ARASI),\n - AKADEMIDE OLAN CHARLARI SILMEDEN TEKRAR OYUNA GIRME (40-50 LVL ARASI)\nISLEVLERINI YAPTIRABILIRSINIZ.\n    # ID ICERISINDE CHAR ALANI KALMADIGINDA;\n - BOTU KAPATMA,\n - PHBOT BILDIRIMLERINDE GOSTERME,\n - DOSYA YOLUNU BELIRTTIGINIZ SESI CALMA (.waw UZANTILI),\n - LOG DOSYASI OLUSTURMA\nOZELLIKLERI BULUNMAKTADIR. ')
def btnIletisim_clicked():
	QtBind.clear(gui,lstInfo)
	QtBind.append(gui,lstInfo,'- ILETISIM:\n   # DISCORD: "GAUCHE#8710"\n   # E-MAIL: "can.berk.cetin@hotmail.com.tr"\n\n- SOSYAL MEDYA:\n    # INSTAGRAM: "can.berk.cetin"\n    # YOUTUBE: "JoySro Hazar GAUCHE" ')
def btnUltimateChanger_clicked():
	QtBind.clear(gui,lstInfo)
	QtBind.append(gui,lstInfo, 'UltimateChanger:\n    # BU PLUGIN ILE GUVENILIR KISI LISTESINE EKLENMIS;\nPT - GUILD - UNION UYELERINDEN GELEN EXCHANGELERI OTOMATIK KABUL EDER,\nVERILEN ITEM VEYA GOLDU OTOMATIK KABUL EDER VE OTOMATIK ONAYLAMA\nYAPARAK TAKASI SONLANDIRIR.')
def btnUltimateItemManager_clicked():
	QtBind.clear(gui,lstInfo)
	QtBind.append(gui,lstInfo,'UltimateItemManager:\n    # BU PLUGININ CIFT ISLEVI VARDIR.\n1. ISLEV:\n # PLUGIN UZERINDEN CHARINIZDA MEVCUT OLAN STONE, ELIXIR VE COINLERI\nGOREBILIRSINIZ.(ENVANTER - STORAGE - GUILD STORAGE)\n2.ISLEV:\n # PLUGINDE BELIRLEDIGINIZ MAIN CHAR,SIFRE VE DEGREE NUMARASI ILE DIGER\nCHARLARINIZDAKI STONE,ELIXIR VE COIN MIKTARLARINI PM OLARAK ALABILIRSINIZ.\n YAPMANIZ GEREKEN TEK SEY YAN CHARINIZI GORMEK ISTEDIGINIZ YERIN VE\nITEMIN KODUNU YAZMAK..\n # YER KODLARI:\n i = ENVANTER | s = STORAGE | g = GUILD SORAGE\n # ITEM KODLARI:\n Stone | Elixir | Coin\n # ORNEK: STORAGEDEKI COIN MIKTARINI PM OLARAK ALMAK ICIN "sCoin" YAZILIR. ')
def btnUltimateTranslator_clicked():
	QtBind.clear(gui,lstInfo)
	QtBind.append(gui,lstInfo,'UltimateTranslator:\n    # BU PLUGIN ILE OYUN CHATINDAN GELEN HERHANGI BIR DILDEDKI YAZIYI\nISTEDIGINIZ BASKA BIR DILE CEVIREBILIR, TURKCE GONDERDIGINIZ YAZIYI KARSI\nTARAFA OTOMATIK SECTIGINIZ DILE CEVIREREK GONDERIR.')
def btnUltimateDungeon_clicked():
	QtBind.clear(gui,lstInfo)
	QtBind.append(gui,lstInfo,'UltimateDungeon:\n    # BU PLUGIN ILE FORGOTTEN WORLD - HOLW WATER TEMPLE GIBI DUNGEONLARI\nSCRIPTE EKLENEN 2 KOMUT SAYESINDE OTO YAPTIRABILIRSINIZ.\n1. KOMUT:\n "AtackArea,x,y"\n # x = RANGE (YAZILMAZSA VARSAYILAN = 75)\n # y = YENIDEN CANAVAR TANIMLAMA SURESI (SANIYE)\n2. KOMUT:\n "GoDimensional"\n      VEYA\n "GoDimensional,Dimension Hole (Flame Mountain-3 stars)" \n            = DIMENSION ACIP FGW GIRMESI ICIN.')
log('Plugin: '+pName+' v'+pVersion+' BASARIYLA YUKLENDI')
