#  CamdInfo - Converter
from enigma import iServiceInformation
from Components.Converter.Converter import Converter
from Components.Element import cached
from Tools.Directories import fileExists
import os


class CamdInfo3(Converter, object):
	def __init__(self, type):
		Converter.__init__(self, type)

	@cached
	def getText(self):
		service = self.source.service
		info = service and service.info()
		camd = ""
		serlist = None
		if not info:
			return ""
		# TS-Panel
		if fileExists("/etc/startcam.sh"):
			try:
				for line in open("/etc/startcam.sh"):
					if line.find("script") > -1:
						return "%s" % line.split("/")[-1].split()[0][:-3]
			except:
				camdlist = None
		# VTI 	
		if fileExists("/tmp/.emu.info"):
			try:
				camdlist = open("/tmp/.emu.info", "r")
			except:
				return None
		# BlackHole	
		elif fileExists("/etc/CurrentBhCamName"):
			try:
				camdlist = open("/etc/CurrentBhCamName", "r")
			except:
				return None
		# Domica	
		elif fileExists("/etc/active_emu.list"):
			try:
				camdlist = open("/etc/active_emu.list", "r")
			except:
				return None
		# Egami	
		elif fileExists("/tmp/egami.inf","r"):
			lines = open("/tmp/egami.inf", "r").readlines()
			for line in lines:
				item = line.split(":",1)
				if item[0] == "Current emulator":
					return item[1].strip()
		#Pli
		elif fileExists("/etc/init.d/softcam") or fileExists("/etc/init.d/cardserver"):
			try:
				camdlist = os.popen("/etc/init.d/softcam info")
			except:
				pass
			try:
				serlist = os.popen("/etc/init.d/cardserver info")
			except:
				pass
			
		# OoZooN
		elif fileExists("/tmp/cam.info"):
			try:
				camdlist = open("/tmp/cam.info", "r")
			except:
				return None
		# Merlin2	
		elif fileExists("/etc/clist.list"):
			try:
		   		camdlist = open("/etc/clist.list", "r")
		   	except:
				return None
		# GP3
		elif fileExists("/usr/lib/enigma2/python/Plugins/Bp/geminimain/lib/libgeminimain.so"):
			try:
				from Plugins.Bp.geminimain.plugin import GETCAMDLIST
				from Plugins.Bp.geminimain.lib import libgeminimain
				camdl = libgeminimain.getPyList(GETCAMDLIST)
				cam = None
				for x in camdl:
					if x[1] == 1:
						cam = x[2] 
				return cam
		   	except:
				return None
		# Unknown emu
		else:
			return None
			
		if serlist is not None:
			try:
				cardserver = ""
				for current in serlist.readlines():
					cardserver = current
				serlist.close()
			except:
				pass
		else:
			cardserver = "NA"

		if camdlist is not None:
			try:
				emu = ""
				for current in camdlist.readlines():
					emu = current
				camdlist.close()
			except:
				pass
		else:
			emu = "NA"
			
		return "%s %s" % (cardserver.split('\n')[0], emu.split('\n')[0])
		
	text = property(getText)

	def changed(self, what):
		Converter.changed(self, what)
