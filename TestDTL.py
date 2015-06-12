P = {('p8', 'p3'): ('p8', 'p3', None, None), ('p6', 'p8'):

('p6', 'p8', ('p8', 'p2'), ('p8', 'p3')), 'pTop': 

('Top', 'p6', ('p6', 'p1'), ('p6', 'p8')), ('p6', 

'p1'): ('p6', 'p1', None, None), ('p8', 'p2'): ('p8', 

'p2', None, None)}



fDTL = {('p8', 'h2'): [['T', ('p3', 'h2'), ('p4', 'h4'), 1], 1], 
('p7', 'h1'): [['T', ('p1', 'h1'), ('p2', 'h3'), 1], 1], 
('p1', 'h1'): [['C', (None, None), (None, None), 1], 0], 
('p6', 'h7'): [['S', ('p7', 'h1'), ('p8', 'h2'), 1], 2], 
('p3', 'h2'): [['C', (None, None), (None, None), 1], 0], 
('p8', 'h4'): [['T', ('p4', 'h4'), ('p3', 'h2'), 1], 1], 
('p2', 'h3'): [['C', (None, None), (None, None), 1], 0], 
('p6', 'h8'): [['S', ('p7', 'h3'), ('p8', 'h4'), 1], 2], 
('p7', 'h3'): [['T', ('p2', 'h3'), ('p1', 'h1'), 1], 1], 
('p4', 'h4'): [['C', (None, None), (None, None), 1], 0]}



newDTL = {('p8', 'h2'): [['T', ('p3', 'h2'), ('p4', 'h4'), 0], 1], 
('p6', 'h7'): [['S', ('p7', 'h1'), ('p8', 'h2'), 0], 2], 
('p3', 'h2'): [['C', (None, None), (None, None), 0], 0], 
('p8', 'h4'): [['T', ('p4', 'h4'), ('p3', 'h2'), 1], 1], 
('p2', 'h3'): [['C', (None, None), (None, None), 0], 0], 
('p7', 'h3'): [['T', ('p2', 'h3'), ('p1', 'h1'), 1], 1], 
('p7', 'h1'): [['T', ('p1', 'h1'), ('p2', 'h3'), 0], 1], 
('p1', 'h1'): [['C', (None, None), (None, None), 0], 0], 
('p6', 'h8'): [['S', ('p7', 'h3'), ('p8', 'h4'), 1], 2], 
('p4', 'h4'): [['C', (None, None), (None, None), 0], 0]}

booking: newDTL output
{('p8', 'h2'): [[('T', ('p3', 'h2'), ('p4', 'h4'), 0)], 0], 
('p7', 'h1'): [[('T', ('p1', 'h1'), ('p2', 'h3'), 0)], 0], 
('p1', 'h1'): [('C', (None, None), (None, None), 0), 0], 
('p6', 'h7'): [[('S', ('p7', 'h1'), ('p8', 'h2'), 0)], 0], 
('p3', 'h2'): [('C', (None, None), (None, None), 0), 0], 
('p8', 'h4'): [[('T', ('p4', 'h4'), ('p3', 'h2'), 1)], 0], 
('p2', 'h3'): [('C', (None, None), (None, None), 0), 0], 
('p6', 'h8'): [[('S', ('p7', 'h3'), ('p8', 'h4'), 1)], 0], 
('p7', 'h3'): [[('T', ('p2', 'h3'), ('p1', 'h1'), 1)], 0], 
('p4', 'h4'): [('C', (None, None), (None, None), 0), 0]}


DTL = {('p2', 'h2'): [['C', (None, None), (None, None), 1], 0], 
('p6', 'h6'): [['CO', ('p1', 'h1'), ('p8', 'h8'), 1], 0], 
('p3', 'h3'): [['C', (None, None), (None, None), 1], 0], 
('p1', 'h1'): [['C', (None, None), (None, None), 1], 0], 
('p8', 'h8'): [['CO', ('p2', 'h2'), ('p3', 'h3'), 1], 0]}

bookkeeping output
'BSFHMap:'
{('p8', 'h2'): [('T', ('p3', 'h2'), ('p4', 'h4'), 1), 2], 
('p7', 'h3'): [('T', ('p2', 'h3'), ('p1', 'h1'), 1), 2], 
('p7', 'h1'): [('T', ('p1', 'h1'), ('p2', 'h3'), 1), 2], 
('p1', 'h1'): [('C', (None, None), (None, None), 1), 1], 
('p6', 'h7'): [('S', ('p7', 'h1'), ('p8', 'h2'), 1), 4], 
('p3', 'h2'): [('C', (None, None), (None, None), 1), 1], 
('p8', 'h4'): [('T', ('p4', 'h4'), ('p3', 'h2'), 1), 2], 
('p2', 'h3'): [('C', (None, None), (None, None), 1), 1], 
('p6', 'h8'): [('S', ('p7', 'h3'), ('p8', 'h4'), 1), 4], 
('p4', 'h4'): [('C', (None, None), (None, None), 1), 1]}

{('p8', 'h2'): [('T', ('p3', 'h2'), ('p4', 'h4'), 1), 2], 
('p7', 'h3'): [('T', ('p2', 'h3'), ('p1', 'h1'), 1), 2], 
('p7', 'h1'): [('T', ('p1', 'h1'), ('p2', 'h3'), 1), 2], 
('p1', 'h1'): [('C', (None, None), (None, None), 1), 1], 
('p6', 'h7'): [('S', ('p7', 'h1'), ('p8', 'h2'), 1), 4], 
('p3', 'h2'): [('C', (None, None), (None, None), 1), 1], 
('p8', 'h4'): [('T', ('p4', 'h4'), ('p3', 'h2'), 1), 2], 
('p2', 'h3'): [('C', (None, None), (None, None), 1), 1],  
('p6', 'h8'): [('S', ('p7', 'h3'), ('p8', 'h4'), 1), 4], 
('p4', 'h4'): [('C', (None, None), (None, None), 1), 1]}



 'BSFHEvent:'
  {('T', ('p4', 'h4'), ('p3', 'h2'), 1): 2, 
  ('T', ('p3', 'h2'), ('p4', 'h4'), 1): 2, 
  ('T', ('p2', 'h3'), ('p1', 'h1'), 1): 2, 
  ('S', ('p7', 'h3'), ('p8', 'h4'), 1): 4, 
  ('T', ('p1', 'h1'), ('p2', 'h3'), 1): 2, 
  'S', ('p7', 'h1'), ('p8', 'h2'), 1): 4})


({('p8', 'h2'): ('T', ('p3', 'h2'), ('p4', 'h4')), 
	('p7', 'h1'): ('T', ('p1', 'h1'), ('p2', 'h3')), 
	('p1', 'h1'): ['C', (None, None), (None, None)], 
	('p6', 'h7'): ('S', ('p7', 'h1'), ('p8', 'h2')), 
	('p3', 'h2'): ['C', (None, None), (None, None)], 
	('p2', 'h3'): ['C', (None, None), (None, None)], 
	('p4', 'h4'): ['C', (None, None), (None, None)]}, 


{('p8', 'h2'): [['T', ('p3', 'h2'), ('p4', 'h4'), 0], 1], 
('p6', 'h7'): [['S', ('p7', 'h1'), ('p8', 'h2'), 0], 2], 
('p3', 'h2'): [['C', (None, None), (None, None), 0], 0], 
('p8', 'h4'): [['T', ('p4', 'h4'), ('p3', 'h2'), 1], 1], 
('p2', 'h3'): [['C', (None, None), (None, None), 0], 0], 
('p7', 'h3'): [['T', ('p2', 'h3'), ('p1', 'h1'), 1], 1], 
('p7', 'h1'): [['T', ('p1', 'h1'), ('p2', 'h3'), 0], 1], 
('p1', 'h1'): [['C', (None, None), (None, None), 0], 0], 
('p6', 'h8'): [['S', ('p7', 'h3'), ('p8', 'h4'), 1], 2], 
('p4', 'h4'): [['C', (None, None), (None, None), 0], 0]}

Greedy output:

currentDTL:  {('p8', 'h2'): [['T', ('p3', 'h2'), ('p4', 'h4'), 0], 1], 
('p6', 'h7'): [['S', ('p7', 'h1'), ('p8', 'h2'), 0], 2], 
('p3', 'h2'): [['C', (None, None), (None, None), 0], 0], 
('p8', 'h4'): [['T', ('p4', 'h4'), ('p3', 'h2'), 1], 1], 
('p2', 'h3'): [['C', (None, None), (None, None), 0], 0], 
('p7', 'h3'): [['T', ('p2', 'h3'), ('p1', 'h1'), 1], 1], 
('p7', 'h1'): [['T', ('p1', 'h1'), ('p2', 'h3'), 0], 1], 
('p1', 'h1'): [['C', (None, None), (None, None), 0], 0], 
('p6', 'h8'): [['S', ('p7', 'h3'), ('p8', 'h4'), 1], 2], 
('p4', 'h4'): [['C', (None, None), (None, None), 0], 0]}


currentDTL:  {('p8', 'h2'): [['T', ('p3', 'h2'), ('p4', 'h4'), 0], 1], 
('p6', 'h7'): [['S', ('p7', 'h1'), ('p8', 'h2'), 0], 2], 
('p3', 'h2'): [['C', (None, None), (None, None), 0], 0], 
('p8', 'h4'): [['T', ('p4', 'h4'), ('p3', 'h2'), 1], 1], 
('p2', 'h3'): [['C', (None, None), (None, None), 0], 0], 
('p7', 'h3'): [['T', ('p2', 'h3'), ('p1', 'h1'), 1], 1], 
('p7', 'h1'): [['T', ('p1', 'h1'), ('p2', 'h3'), 0], 1], 
('p1', 'h1'): [['C', (None, None), (None, None), 0], 0], 
('p6', 'h8'): [['S', ('p7', 'h3'), ('p8', 'h4'), 1], 2], 
('p4', 'h4'): [['C', (None, None), (None, None), 0], 0]}

new BSFHMap:  {('p8', 'h2'): [('T', ('p3', 'h2'), ('p4', 'h4'), 1), 2], 
('p7', 'h3'): [('T', ('p2', 'h3'), ('p1', 'h1'), 1), 2], 
('p7', 'h1'): [('T', ('p1', 'h1'), ('p2', 'h3'), 1), 2], 
('p1', 'h1'): [('C', (None, None), (None, None), 1), 1], 
('p6', 'h7'): [('S', ('p7', 'h1'), ('p8', 'h2'), 1), 4], 
('p3', 'h2'): [('C', (None, None), (None, None), 1), 1], 
('p8', 'h4'): [('T', ('p4', 'h4'), ('p3', 'h2'), 1), 2], 
('p2', 'h3'): [('C', (None, None), (None, None), 1), 1], 
('p6', 'h8'): [('S', ('p7', 'h3'), ('p8', 'h4'), 1), 4], 
('p4', 'h4'): [('C', (None, None), (None, None), 1), 1]}
new BSFHMap:  {('p8', 'h2'): [('T', ('p3', 'h2'), ('p4', 'h4'), 0), 2], 
('p7', 'h1'): [('T', ('p1', 'h1'), ('p2', 'h3'), 0), 2], 
('p1', 'h1'): [('C', (None, None), (None, None), 0), 1], 
('p6', 'h7'): [('S', ('p7', 'h1'), ('p8', 'h2'), 0), 4], 
('p3', 'h2'): [('C', (None, None), (None, None), 0), 1], 
('p8', 'h4'): [('T', ('p4', 'h4'), ('p3', 'h2'), 1), 2], 
('p2', 'h3'): [('C', (None, None), (None, None), 0), 1], 
('p6', 'h8'): [('S', ('p7', 'h3'), ('p8', 'h4'), 1), 4], 
('p7', 'h3'): [('T', ('p2', 'h3'), ('p1', 'h1'), 1), 2], 
('p4', 'h4'): [('C', (None, None), (None, None), 0), 1]}







[{('p8', 'h2'): ('T', ('p3', 'h2'), ('p4', 'h4')), 
('p7', 'h1'): ('T', ('p1', 'h1'), ('p2', 'h3')), 
('p1', 'h1'): ('C', (None, None), (None, None)), 
('p6', 'h7'): ('S', ('p7', 'h1'), ('p8', 'h2')), 
('p3', 'h2'): ('C', (None, None), (None, None)), 
('p2', 'h3'): ('C', (None, None), (None, None)), 
('p4', 'h4'): ('C', (None, None), (None, None))}, 

{('p8', 'h2'): ('T', ('p3', 'h2'), ('p4', 'h4')), 
('p7', 'h1'): ('T', ('p1', 'h1'), ('p2', 'h3')), 
('p1', 'h1'): ('C', (None, None), (None, None)), 
('p6', 'h7'): ('S', ('p7', 'h1'), ('p8', 'h2')), 
('p3', 'h2'): ('C', (None, None), (None, None)), 
('p2', 'h3'): ('C', (None, None), (None, None)), 
('p4', 'h4'): ('C', (None, None), (None, None))}]




we did it!!!!!

[{('p8', 'h2'): ('T', ('p3', 'h2'), ('p4', 'h4')), 
('p7', 'h1'): ('T', ('p1', 'h1'), ('p2', 'h3')), 
('p1', 'h1'): ('C', (None, None), (None, None)), 
'p6', 'h7'): ('S', ('p7', 'h1'), ('p8', 'h2')), 
('p3', 'h2'): ('C', (None, None), (None, None)), 
('p2', 'h3'): ('C', (None, None), (None, None)), 
('p4', 'h4'): ('C', (None, None), (None, None))}, 

{('p7', 'h3'): ('T', ('p2', 'h3'), ('p1', 'h1')), 
('p1', 'h1'): ('C', (None, None), (None, None)), 
('p3', 'h2'): ('C', (None, None), (None, None)), 
('p8', 'h4'): ('T', ('p4', 'h4'), ('p3', 'h2')), 
('p2', 'h3'): ('C', (None, None), (None, None)), 
('p6', 'h8'): ('S', ('p7', 'h3'), ('p8', 'h4')), 
('p4', 'h4'): ('C', (None, None), (None, None))}]


 bookkeeping(newDTL, P):
 {('p8', 'h2'): [('T', ('p3', 'h2'), ('p4', 'h4'), 0), 0], 
 ('p7', 'h1'): [('T', ('p1', 'h1'), ('p2', 'h3'), 0), 0], 
 ('p1', 'h1'): [('C', (None, None), (None, None), 0), 0], 
 ('p6', 'h7'): [('S', ('p7', 'h1'), ('p8', 'h2'), 0), 0], 
 ('p3', 'h2'): [('C', (None, None), (None, None), 0), 0], 
 ('p8', 'h4'): [('T', ('p4', 'h4'), ('p3', 'h2'), 1), 1], 
 ('p2', 'h3'): [('C', (None, None), (None, None), 0), 0], 
 ('p6', 'h8'): [('S', ('p7', 'h3'), ('p8', 'h4'), 1), 3], 
 ('p7', 'h3'): [('T', ('p2', 'h3'), ('p1', 'h1'), 1), 1], 
 ('p4', 'h4'): [('C', (None, None), (None, None), 0), 0]}


testing from heliconius tree
 H = {('m5', 'ecuadoriensis_EastE'): ('m5', 'ecuadoriensis_EastE', None, None), 
 ('m9', 'm10'): ('m9', 'm10', ('m10', 'melpomene_WestPA'), ('m10', 'rosina_WestCR')), 
 ('m2', 'm3'): ('m2', 'm3', ('m3', 'm4'), ('m3', 'm5')), 
 ('m1', 'm8'): ('m1', 'm8', ('m8', 'm9'), ('m8', 'm11')), 
 ('m7', 'thelxiopeia_EastFG'): ('m7', 'thelxiopeia_EastFG', None, None), 
 ('m6', 'm7'): ('m6', 'm7', ('m7', 'thelxiopeia_EastFG'), ('m7', 'melpomene_EastFG')), 
 ('m3', 'm5'): ('m3', 'm5', ('m5', 'ecuadoriensis_EastE'), ('m5', 'malleti_EastE')), 
 'hTop': ('Top', 'm1', ('m1', 'm2'), ('m1', 'm8')), 
 ('m9', 'rosina_WestPA'): ('m9', 'rosina_WestPA', None, None), 
 ('m11', 'cythera_WestE'): ('m11', 'cythera_WestE', None, None), 
 ('m8', 'm9'): ('m8', 'm9', ('m9', 'm10'), ('m9', 'rosina_WestPA')), 
 ('m10', 'melpomene_WestPA'): ('m10', 'melpomene_WestPA', None, None), 
 ('m10', 'rosina_WestCR'): ('m10', 'rosina_WestCR', None, None), 
 ('m3', 'm4'): ('m3', 'm4', ('m4', 'aglaope_EastPE'), ('m4', 'amaryllis_EastPE')), 
 ('m5', 'malleti_EastE'): ('m5', 'malleti_EastE', None, None), 
 ('m4', 'aglaope_EastPE'): ('m4', 'aglaope_EastPE', None, None), 
 ('m11', 'melpomene_EastC'): ('m11', 'melpomene_EastC', None, None), 
 ('m7', 'melpomene_EastFG'): ('m7', 'melpomene_EastFG', None, None), 
 ('m2', 'm6'): ('m2', 'm6', ('m6', 'm7'), ('m6', 'melpomene_EastT')), 
 ('m1', 'm2'): ('m1', 'm2', ('m2', 'm3'), ('m2', 'm6')), 
 ('m4', 'amaryllis_EastPE'): ('m4', 'amaryllis_EastPE', None, None), 
 ('m6', 'melpomene_EastT'): ('m6', 'melpomene_EastT', None, None), 
 ('m8', 'm11'): ('m8', 'm11', ('m11', 'melpomene_EastC'), ('m11', 'cythera_WestE'))} 


 P = {('n10', 'hydara_WestPA'): ('n10', 'hydara_WestPA', None, None), 
 ('n6', 'erato_EastFG'): ('n6', 'erato_EastFG', None, None), 
 ('n5', 'etylus_EastE'): ('n5', 'etylus_EastE', None, None), 
 ('n9', 'n10'): ('n9', 'n10', ('n10', 'hydara_EastT'), ('n10', 'hydara_WestPA')), 
 ('n2', 'n6'): ('n2', 'n6', ('n6', 'erato_EastFG'), ('n6', 'hydara_EastFG')), 
 ('n6', 'hydara_EastFG'): ('n6', 'hydara_EastFG', None, None), 
 ('n9', 'petiverana_WestCR'): ('n9', 'petiverana_WestCR', None, None), 
 ('n1', 'n2'): ('n1', 'n2', ('n2', 'n3'), ('n2', 'n6')), 
 ('n2', 'n3'): ('n2', 'n3', ('n3', 'n4'), ('n3', 'lativitta_EastE')), 
 ('n7', 'n8'): ('n7', 'n8', ('n8', 'n9'), ('n8', 'petiverana_WestPA')), 
 'pTop': ('Top', 'n1', ('n1', 'n2'), ('n1', 'n7')), 
 ('n8', 'petiverana_WestPA'): ('n8', 'petiverana_WestPA', None, None), 
 ('n7', 'n11'): ('n7', 'n11', ('n11', 'hydara_EastC'), ('n11', 'cyrbia_WestE')), 
 ('n10', 'hydara_EastT'): ('n10', 'hydara_EastT', None, None), 
 ('n1', 'n7'): ('n1', 'n7', ('n7', 'n8'), ('n7', 'n11')), 
 ('n4', 'n5'): ('n4', 'n5', ('n5', 'favorinus_EastPE'), ('n5', 'etylus_EastE')), 
 ('n3', 'lativitta_EastE'): ('n3', 'lativitta_EastE', None, None), 
 ('n8', 'n9'): ('n8', 'n9', ('n9', 'n10'), ('n9', 'petiverana_WestCR')), 
 ('n4', 'emma_EastPE'): ('n4', 'emma_EastPE', None, None), 
 ('n11', 'hydara_EastC'): ('n11', 'hydara_EastC', None, None), 
 ('n11', 'cyrbia_WestE'): ('n11', 'cyrbia_WestE', None, None), 
 ('n5', 'favorinus_EastPE'): ('n5', 'favorinus_EastPE', None, None), 
 ('n3', 'n4'): ('n3', 'n4', ('n4', 'emma_EastPE'), ('n4', 'n5'))}


phi = {'cyrbia_WestE': 'cythera_WestE', 
'erato_EastFG': 'thelxiopeia_EastFG', 
'hydara_EastFG': 'melpomene_EastFG', 
'lativitta_EastE': 'malleti_EastE', 
'hydara_EastC': 'melpomene_EastC', 
'petiverana_WestPA': 'rosina_WestPA', 
'petiverana_WestCR': 'rosina_WestCR', 
'emma_EastPE': 'aglaope_EastPE', 
'etylus_EastE': 'ecuadoriensis_EastE', 
'favorinus_EastPE': 'amaryllis_EastPE', 
'hydara_EastT': 'melpomene_EastT', 
'hydara_WestPA': 'melpomene_WestPA'}

DTL output of DPjune12.py:
DTL = {('petiverana_WestCR', 'rosina_WestCR'): [['C', (None, None), (None, None), 1], 0], 
('n2', 'm2'): [['S', ('n3', 'm3'), ('n6', 'm6'), 1], 3], 
('n8', 'm9'): [['S', ('n9', 'm10'), ('petiverana_WestPA', 'rosina_WestPA'), 1], 1], 
('emma_EastPE', 'aglaope_EastPE'): [['C', (None, None), (None, None), 1], 0], 
('favorinus_EastPE', 'amaryllis_EastPE'): [['C', (None, None), (None, None), 1], 0], 
('etylus_EastE', 'ecuadoriensis_EastE'): [['C', (None, None), (None, None), 1], 0], 
('lativitta_EastE', 'malleti_EastE'): [['C', (None, None), (None, None), 1], 0], 
('n6', 'm7'): [['S', ('erato_EastFG', 'thelxiopeia_EastFG'), ('hydara_EastFG', 'melpomene_EastFG'), 1], 0], 
('n10', 'melpomene_WestPA'): [['T', ('hydara_WestPA', 'melpomene_WestPA'), ('hydara_EastT', 'melpomene_EastT'), 1], 1], 
('hydara_WestPA', 'melpomene_WestPA'): [['C', (None, None), (None, None), 1], 0], 
('n6', 'm6'): [['L', ('n6', 'm7'), (None, None), 1], 1], 
('petiverana_WestPA', 'rosina_WestPA'): [['C', (None, None), (None, None), 1], 0], 
('n7', 'm8'): [['S', ('n8', 'm9'), ('n11', 'm11'), 1], 1], 
('cyrbia_WestE', 'cythera_WestE'): [['C', (None, None), (None, None), 1], 0], 
('hydara_EastT', 'melpomene_EastT'): [['C', (None, None), (None, None), 1], 0], 
('erato_EastFG', 'thelxiopeia_EastFG'): [['C', (None, None), (None, None), 1], 0], 
('n5', 'amaryllis_EastPE'): [['T', ('favorinus_EastPE', 'amaryllis_EastPE'), ('etylus_EastE', 'ecuadoriensis_EastE'), 1], 1], 
('n11', 'm11'): [['S', ('hydara_EastC', 'melpomene_EastC'), ('cyrbia_WestE', 'cythera_WestE'), 1], 0], 
('n9', 'm10'): [['S', ('n10', 'melpomene_WestPA'), ('petiverana_WestCR', 'rosina_WestCR'), 1], 1], 
('n3', 'm3'): [['S', ('n4', 'm4'), ('lativitta_EastE', 'm5'), 1], 2], 
('n4', 'm4'): [['S', ('emma_EastPE', 'aglaope_EastPE'), ('n5', 'amaryllis_EastPE'), 1], 1], 
('hydara_EastC', 'melpomene_EastC'): [['C', (None, None), (None, None), 1], 0], 
('n1', 'm1'): [['S', ('n2', 'm2'), ('n7', 'm8'), 1], 4], 
('hydara_EastFG', 'melpomene_EastFG'): [['C', (None, None), (None, None), 1], 0], 
('lativitta_EastE', 'm5'): [['L', ('lativitta_EastE', 'malleti_EastE'), (None, None), 1], 1]}
















