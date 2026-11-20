import re
R3={'Fin Funnels':'Aletas satélite','Los Funnels':'Los cañones satélite','Funnels':'Cañones satélite','Funnel':'Cañón satélite','Full Frontal':'Frontal Total','Tri Bomber':'Triple Bombardero','Battle Bomber':'Bombardero de Combate','Great Mightgaine':'Gran Mightgaine','Lambda Driver':'Motor Lambda'}
P3=re.compile(r'(?<![\wáéíóúñ])('+'|'.join(sorted(map(re.escape,R3),key=len,reverse=True))+r')(?![\wáéíóúñ])')
def sub(s): return P3.sub(lambda m:R3[m.group(1)],s)
