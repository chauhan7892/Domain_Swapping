import FR_Prot_Data


def Count_AA(seq):
	Prot_letters = "ACDEFGHIKLMNPQRSTVWY"
	prot_dict = dict((k,0) for k in Prot_letters)

	for aa in prot_dict:
		prot_dict[aa] = seq.count(aa)

	return prot_dict

def Get_AA_percentage(seq):
	AA_count = Count_AA(seq)
	percentage = {}

	for aa in AA_count:
		percentage[aa] = AA_count[aa]/float(len(seq))

	return percentage

def MW(seq):
	water = 18.010565
	wt = sum(FR_Prot_Data.Wt_table[x] for x in seq) - (len(seq) - 1)*water

	return wt

def Aromaticity(seq):
	Aroma_AAs = 'YWF'

	AA_percent = get_AA_percentage(seq)
	aromaticity = sum(AA_percent[aa] for aa in Aroma_AAs)

	return aromaticity


# This function calculates the total charge of the protein at a given pH.
def Get_Prot_Charge(seq, pH):

	pos_pKs = {'Nterm': 7.5, 'K': 10.0, 'R': 12.0, 'H': 5.98}
	neg_pKs = {'Cterm': 3.55, 'D': 4.05, 'E': 4.45, 'C': 9.0, 'Y': 10.0}
	charged_AAs = 'KRHDECY'
	pKnterminal = {'A': 7.59, 'M': 7.0, 'S': 6.93, 'P': 8.36, 'T': 6.82, 'V': 7.44, 'E': 7.7}
	pKcterminal = {'D': 4.55, 'E': 4.75}
	nterm = seq[0]
	cterm = seq[-1]

	if nterm in pKnterminal:
		pos_pKs['Nterm'] = pKnterminal[nterm]
	if cterm in pKcterminal:
		pos_pKs['Cterm'] = pKcterminal[cterm]

	AA_count = Count_AA(seq)
	charged_AAs_content = {}

	for aa in charged_AAs:
		charged_AAs_content[aa] = AA_count[aa]

	charged_AAs_content['Nterm'] = 1.0
	charged_AAs_content['Cterm'] = 1.0

	Positive_Charge = 0.0
	for aa, pK in pos_pKs.items():
		CR = 10 ** (pK - pH)
		partial_charge = CR / (CR + 1.0)
		Positive_Charge += 	charged_AAs_content[aa] * partial_charge

	Negative_Charge = 0.0

	for aa, pK in neg_pKs.items():
		CR = 10 ** (pH - pK)
		partial_charge = CR / (CR + 1.0)
		Negative_Charge += 	charged_AAs_content[aa] * partial_charge

	Total_charge = Positive_Charge - Negative_Charge

	return Total_charge


# IsoelectricPoint
def pI(seqpI):

	pH = 7.4
	Charge = Get_Prot_Charge(seq, pH)
	if Charge > 0.0:
		pH1 = pH
		Charge1 = Charge
		while Charge1 > 0.0:
			pH = pH1 + 1.0
			Charge = Get_Prot_Charge(seq, pH)
			if Charge > 0.0:
				pH1 = pH
				Charge1 = Charge
			else:
				pH2 = pH
				Charge2 = Charge
				break
	else:
		pH2 = pH
		Charge2 = Charge
		while Charge2 < 0.0:
			pH = pH2 - 1.0
			Charge = Get_Prot_Charge(seq, pH)
			if Charge < 0.0:
				pH2 = pH
				Charge2 = Charge
			else:
				pH1 = pH
				Charge1 = Charge
				break
	# Bisection
	while pH2 - pH1 > 0.0001 and Charge != 0.0:
		pH = (pH1 + pH2) / 2.0
		Charge = Get_Prot_Charge(seq, pH)
		if Charge > 0.0:
			pH1 = pH
			Charge1 = Charge
		else:
			pH2 = pH
			Charge2 = Charge

	return pH

#Calculate the instability index according to Guruprasad et al 1990
def instability_index(seq):
	index =''
	score = 0.0
	length = len(seq)

	for i in range(length - 1):
		first, second = seq[i:i + 2]
		dipeptide_value = index[first][second]
		score += dipeptide_value

	inst = (10.0 / length ) * score

	return inst

# Calculate the flexibility according to Vihinen, 1994
def flexibility(seq):
	flexibilities = FR_Prot_Data.Flex
	window_size = 9
	weights = [0.25, 0.4375, 0.625, 0.8125, 1]
	length = len(seq)

	scores = []
	for i in range(length - window_size):
		subsequence = seq[i:i + window_size]
		score = 0.0

		for j in range(window_size // 2):
			front = subsequence[j]
			back = subsequence[window_size - j - 1]
			score += (flexibilities[front] + flexibilities[back]) * weights[j]

		middle = subsequence[window_size // 2 + 1]
		score += flexibilities[middle]
		scores.append(score / 5.25)

	return scores

def gravy(seq):
	total_gravy = sum( FR_Prot_Data.kd[aa] for aa in seq)
	length = len(seq)

	return(total_gravy/length)

def sec_struct_frac(seq):
	AA_percent = Get_AA_percentage(seq)
	helix = sum(AA_percent[i] for i in 'VIYFWL')
	turn = sum(AA_percent[i] for i in 'NPGS')
	sheet = sum(AA_percent[i] for i in 'EMAL')

	return(helix, turn, sheet)

text = "AETVSFNFNSFSEGNPAINFQGDVTVLSNGNIQLTNLNKVNSVGRVLYAMPVRIWSSATGNVASFLTSFSFEMKDIKDYDPADGIIFFIAPEDTQIPAGSIGGGTLGVSDTKGAGHFVGVEFDTYSNSEYNDPPTDHVGIDVNSVDSVKTVPWNSVSGAVVKVTVIYDSSTKTLSVAVTNDNGDITTIAQVVDLKAKLPERVKFGFSASGSLGGRQIHLIRSWSFTSTLITT"
s = Count_AA(text)
print s
