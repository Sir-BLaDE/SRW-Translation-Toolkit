import sys
sys.path.insert(0, '.')
from srwv_cpk import Cpk
from crilayla import maybe_decompress
from srwv_crypto import decrypt_data

def extract_english_only(path1, path2):
    """Extract strings only in path1 (English) but not in path2 (Spanish)."""
    def get_strings(path):
        c = Cpk(path)
        raw = c.read_file(0)
        dec = maybe_decompress(raw)
        x = decrypt_data(dec)
        strings = []
        i = 0
        while i < len(x):
            if not (32 <= x[i] < 127):
                i += 1
                continue
            start = i
            while i < len(x) and 32 <= x[i] < 127:
                i += 1
            s = x[start:i].decode('ascii')
            if len(s) >= 3:
                strings.append(s)
        return set(strings)
    
    spanish_set = get_strings(path2)
    english_set = get_strings(path1)
    
    only_english = english_set - spanish_set
    return only_english

# Extract English-only strings
english_only = extract_english_only(
    'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/B_LT00_EN.cpk',
    'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk')

print(f'English-only strings: {len(english_only)}')

# Create Spanish translations
translations = {
    'Gains 50 Focus when sortied.': 'Gana 50 Enfoque al ser sorteado.',
    'pilots by 10%.': 'los pilotos por un 10%.',
    'The HP of any ally unit on the map drops below 20%': 'La PV de cualquier unidad aliada en el mapa baja del 20%.',
    'Triggers spirit command Instinct': 'Activa el comando espiritual Instinto.',
    'Focus is above 140.': 'El Enfoque es superior a 140.',
    'Increases Armed Armor DE DMG by 300 and Range by 1': 'Incrementa el DEG AE Blindado en 300 y el Alcance en 1.',
    "Ignore an enemy unit's barrier when attacking.": 'Ignora la barrera de la unidad enemiga al atacar.',
    'Nearby allies gain 3 Focus at the': 'Los aliados cercanos ganan 3 Enfoque al.',
    'Strong Luck ': 'Buena Suerte ',
    'Double Action': 'Acción Doble',
    'Restores 5 SP at the start of player': 'Restaura 5 SP al inicio del jugador.',
    'Triggers spirit command Disturb': 'Activa el comando espiritual Molestar.',
    'Save E L1': 'Guarda E L1',
    'for women and increases Final Evasion': 'para mujeres y aumenta la Evitación Final.',
    'As HP decreases, Accuracy %, Evasion %, Critical %, and Defe': 'A medida que disminuye la PV, Precisión %, Evasión %, Crítico y Der...',
    'This icon lights up when a mech is equipped with a jamming d': 'Este ícono se ilumina cuando un mecha está equipado con un dispositivo de inhibición.',
    'command to change forms. This change cannot be reversed.': 'comando para cambiar de forma. Este cambio no puede reversarse.',
    'Air-S.': 'Air-S.',
    'Gains 1 extra Focus when attacking, return attacking,': 'Gana 1 Enfoque extra al atacar, ataque de retorno.',
    '1. Increases SKL by 20.': '1. Incrementa HAB por 20.',
    'Atacante ': 'Atacante ',
    'Duplica el aumento de la Tasa de Sincro.': 'Duplica el aumento de la Tasa de Sincro.',
    'Ataque': 'Ataque',
    'n L1': 'n L1',
    'n son esenciales para': 'n son esenciales para',
    'nivel aumenta un 30%.': 'nivel aumenta un 30%.',
    'RNG, SKL, DEF, EVD y HIT de los enemigos': 'RNG, HAB, DEF, EVA y AC de los enemigos',
    'Desbloquea la parte de poder Efector Espiral, disponible en ': 'Desbloquea el Efector Espiral de poder, disponible en',
    'Comandante L1': 'Comandante L1',
    'Este icono se ilumina cuando un mecha tiene Dividir.': 'Este ícono se ilumina cuando un mecha tiene Dividir.',
    'El Enfoque es 170 en condiciones': 'El Enfoque es 170 en condiciones',
    'Inicio de turno': 'Inicio de turno',
    'Presidente': 'Presidenta',
    'en 1 salvo armas de mapa y armas con alcance 1.': 'en 1 disparo de mapa y armas con alcance 1.',
    'con Enfoque superior a 110.': 'con Enfoque superior a 110.',
    'Toda unidad con ExC de 3 aumenta su Movimiento en 1.': 'Toda unidad con ExC de 3 incrementa su Movilidad en 1.',
    'Adapt. unidad y armas al terreno (Esp) S': 'Adapt. unidad y armas al terreno (Esp) S',
}

# Filter to only translate strings that need it
translatable = {k: v for k, v in translations.items() if k in english_only}

print(f'Traducciones creadas: {len(translatable)}')
print(f'Total English-only: {len(english_only)}')

# Show some translations
print('\n=== Muestra de traducciones ===')
for i, (en, es) in enumerate(list(translatable.items())[:20]):
    print(f'  English: {en[:60]}')
    print(f'  Spanish: {es[:60]}')
    print()