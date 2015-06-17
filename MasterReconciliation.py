import DP
import Greedy
import newickToVis
import ReconConversion

def Reconcile(fileName, D, T, L, k):
	newickToVis.convert(fileName)
	host, paras, phi = DP.newickFormatReader.getInput(fileName)
	DTL = DP.DP(host, paras, phi, D, T, L)
	rec = Greedy.Greedy(DTL, paras, k)
	ReconConversion.convert(rec[0], fileName[:-7])
	return DTL, rec