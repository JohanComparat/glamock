import os
from os.path import join

# define params
def runPMP(LBOX = "650.000", NROW = "1612", NGRID = "1612", DTHR = "120.000", NORM = "0.0001", nrm= "N1em4", SLOPE= "-1.000", slp = "am100", DMAX = "240.000", RR=1, start=0):
	# create outdir
	
	os.chdir(os.environ['GLAMOCK_DIR'])
	os.remove("Init.dat")

	f=open("Init.dat", 'w')
	f.write("""Box      = """ + LBOX  + "\n")
	f.write("""Nrow     = """ + NROW  + "\n")
	f.write("""Ngrid    = """ + NGRID  + "\n")
	f.write("""sig8     = 0.828"""  + "\n")
	f.write("""z_init   = 100.000"""  + "\n")
	f.write("""step da  = 2.0000E-04"""  + "\n")
	f.write("""z_final  = 0.000"""  + "\n")
	f.write("""#outputs = 23"""  + "\n")
	f.write("""3.2 2.61 2.19 1.87 1.62 1.41 1.24 1.09 0.97 0.86 0.76 0.67 0.59 0.51 0.45 0.39 0.33 0.28 0.23 0.18 0.14 0.10 0.00"""  + "\n")
	f.write("""dens_thr = """ + DTHR + "\n")
	f.write("""Vrms     = 0.000"""  + "\n")
	f.write("""#Params  = 10"""  + "\n")
	f.write("""Parametr = """ + DTHR  + "\n")
	f.write("""Parametr = """ +NORM + "\n")
	f.write("""Parametr = """ + SLOPE + "\n")
	f.write("""Parametr = """ +DMAX + "\n")
	f.write("""Parametr =      0.000"""  + "\n")
	f.write("""Parametr =      0.000"""  + "\n")
	f.write("""Parametr =      0.000"""  + "\n")
	f.write("""Parametr =      0.000"""  + "\n")
	f.write("""Parametr =      0.000"""  + "\n")
	f.write("""Parametr =      0.000"""  )
	f.close()

	os.system("make clean")
	os.system("make PMP2main")
	os.system("make PMP2start ")
	os.system("make PMP2init ")
	os.system("make PMPanalysis")
	os.system("./PMP2init.exe")
	
	dirName = "PM_Nr"+NROW+"_L"+LBOX+"_g"+NGRID+"_Dgt"+DTHR[:4]+"_"+slp+"_Dlt"+DMAX[:4] +"_"+nrm
	outdir = join(os.environ['GLAMOCK_DIR'], dirName)
	os.mkdir(outdir)
	os.chdir(outdir)
	
	for ii in range(start, start+RR, 1):
		os.system("touch begin"+str(ii) )
		os.system("echo " + str(ii) + " | " + join( os.environ['GLAMOCK_DIR'], "PMP2start.exe") )
		os.system("echo 1000000 | " + join( os.environ['GLAMOCK_DIR'], "PMP2main.exe") )
		os.system("rm -rf PMcr*.DAT" )
	
	return dirName

dirName = runPMP(LBOX="1000.000", NROW="2000", NGRID="2000", DTHR="10.000", NORM="0.0003", nrm= "N3em4", SLOPE= "0.110", slp="ap011", DMAX="400.000", RR = 10, start=0)

#os.rename(join(os.environ['GLAMOCK_DIR'], dirName), join(os.environ['PM_DIR'], dirName))