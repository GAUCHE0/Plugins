from phBot import *
import QtBind
import urllib.request
import re
import os
import shutil

pName = 'UltimateUpdater'
pVersion = '0.0.2'
pUrl = "https://raw.githubusercontent.com/GAUCHE0/Plugins/main/UltimateUpdater.py"

# ______________________________ YUKLME ______________________________ #
# KULLANICI ARAYUZU
gui = QtBind.init(__name__,pName)
lblPlugins = QtBind.createLabel(gui,"BILGISAYARDA BULUNAN PLUGINLER :",21,11)
lvwPlugins = QtBind.createList(gui,21,30,700,200)
lstPluginsData = []
btnCheck = QtBind.createButton(gui,'btnCheck_clicked',"  GUNCELLEMELERI KONTROL ET  ",300,8)
btnUpdate = QtBind.createButton(gui,'btnUpdate_clicked',"  SECILEN PLUGINI GUNCELLE  ",480,8)
lblPlugins2 = QtBind.createLabel(gui,"UltimateUpdater:\n * GAUCHE TARAFINDAN DUZENLENMISTIR. \n * FEEDBACK SISTEMLI BIR YAZILIMDIR. \n * HATA VE ONERI BILDIRIMLERINIZI BANA ULASTIRABILIRSINIZ.",21,230)
# ______________________________ METHODLAR ______________________________ #
# PLUGIN KLASORUNU KONTROL ETME
def GetPluginsFolder():
	return str(os.path.dirname(os.path.realpath(__file__)))
# AYNI KLASORDEKI TUM PLUGINLERI KONTROL ET VE LISTELE
def btnCheck_clicked():
	QtBind.clear(gui,lvwPlugins)
	# PLUGIN KLASORUNDEKI PLUGINLERI LISTELEME
	pyFolder = GetPluginsFolder()
	files = os.listdir(pyFolder)
	# PLUGIN DATASINI YUKLEME
	global lstPluginsData
	for filename in files:
		# PY DOSYALARINI KONTROL ETME
		if filename.endswith(".py"):
			pyFile = pyFolder+"\\"+filename
			with open(pyFile,"r") as f:
				pyCode = str(f.read())
				# DOSYAYI OKU VE VERSIYON KONTROLU YAP
				if re.search("\npVersion = [0-9a-zA-Z.'\"]*",pyCode):
					# VERSIYON AYIKLA
					pyVersion = re.search("\npVersion = ([0-9a-zA-Z.'\"]*)",pyCode).group(0)[13:-1]
					# ISIM VARSA AYIKLA
					pyName = filename[:-3]
					if re.search("\npName = ([0-9a-zA-Z'\"]*)",pyCode):
						pyName = re.search("\npName = ([0-9a-zA-Z'\"]*)",pyCode).group(0)[10:-1]
					# URL VARSA KONTROL ET
					pyUrl = pyCode.find("\npUrl = ")
					# PLUGIN BILGILERINI GOSTER
					pyInfo = filename+" ("+pyName+" v"+pyVersion+") - "

					# PLUGINI GUNCELLEMEK ICIN GEREKEN HERSEYI AL
					pData = {}
					pData['canUpdate'] = False
					# EGER URL VARSA TUM DATAYI KAYDET
					if pyUrl != -1:
						# URL DEKI KODLARI CEKMEK
						pyUrl = pyCode[pyUrl+9:].split('\n')[0][:-1]
						pyNewVersion = getVersion(pyUrl)
						# VERSIYON VE DATA GUNCELLEMESI
						if pyNewVersion and compareVersion(pyVersion,pyNewVersion):
							# GUNCELLEMEDEN SONRA DATA KAYDETMEK
							pData['canUpdate'] = True
							pData['url'] = pyUrl
							pData['filename'] = filename
							pData['pName'] = pyName
							# GUNCELLEME LOGLARI
							pyInfo += "GUNCELLEME BULUNDU (v"+pyNewVersion+")"
						else:
							pyInfo += "GUNCELLENDI.."
					else:
						pyInfo += "GUNCELLENEMEDI.URL BULUNAMADI."
					# GUI ICINE YERLESTIRME
					QtBind.append(gui,lvwPlugins,pyInfo)
					lstPluginsData.append(pData)
# URL ILE AYNI VERSIYONA SAHIPSE DEVAM ET
def getVersion(url):
	try:
		req = urllib.request.Request(url, headers={'User-Agent' : "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0"})
		with urllib.request.urlopen(req) as w:
			pyCode = str(w.read().decode("utf-8"))
			if re.search("\npVersion = [0-9.'\"]*",pyCode):
				return re.search("\npVersion = ([0-9a-zA-Z.'\"]*)",pyCode).group(0)[13:-1]
	except:
		pass
	return None
# PCDEKI VERSIYON URLDEN DUSUKSE DEVAM ET
def compareVersion(a, b):
	# YALNIZCA NUMARALARA IZIN VERMEK
	a = tuple(map(int, (a.split("."))))
	b = tuple(map(int, (b.split("."))))
	return a < b
# SECILEN GUNCELLEMEYI YAPMAK
def btnUpdate_clicked():
	# SECILEN PLUGINI GETIR
	indexSelected = QtBind.currentIndex(gui,lvwPlugins)
	if indexSelected >= 0:
		pyData = lstPluginsData[indexSelected]
		# EGER YAPABILIYORSA PLUGINI GUNCELLE
		if "canUpdate" in pyData and pyData['canUpdate']:
			# URL DEN AL
			pyUrl = pyData['url']
			try:
				req = urllib.request.Request(pyUrl, headers={'User-Agent' : "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0"})
				with urllib.request.urlopen(req) as w:
					pyCode = str(w.read().decode("utf-8"))
					pyVersion = re.search("\npVersion = ([0-9a-zA-Z.'\"]*)",pyCode).group(0)[13:-1]
					# YEDEK KOPYA OLUSTURMA
					pyFolder = GetPluginsFolder()+'\\'
					shutil.copyfile(pyFolder+pyData['filename'],pyFolder+pyData['pName']+".py.bkp")
					os.remove(pyFolder+pyData['filename'])
					# USTUNE YAZMA DOSYASI OLUSTURMA
					with open(pyFolder+pyData['pName']+".py","w+") as f:
						f.write(pyCode)
					# GUI DATASINI UPDATE ET
					QtBind.removeAt(gui,lvwPlugins,indexSelected)
					QtBind.append(gui,lvwPlugins,pyData['pName']+".py ("+pyData['pName']+" v"+pyVersion+") - GUNCELLEME TAMAMLANDI.")
					log('Plugin: "'+pyData['pName']+'" PLUGIN BASARI ILE GUNCELLENDI')
			except:
				log("Plugin: GUNCELLENIRKEN BIR HATA ILE KARSILASILDI, LUTFEN DAHA SONRA TEKRAR DENEYINIZ.")
# PLUGIN YUKLENDI
log('Plugin: '+pName+' v'+pVersion+' BASARIYLA YUKLENDI.')
