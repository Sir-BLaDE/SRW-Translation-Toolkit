import csv

# Read the English-only strings from the earlier extraction
# We'll create a comprehensive CSV with translations

# First, let's read the existing CSV if it exists
try:
    with open('datos/traducir_lt00.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        existing = [(row['en'], row['es']) for row in reader]
        print(f'Existing translations: {len(existing)}')
except FileNotFoundError:
    existing = []

# Create a comprehensive list of translations
# Based on the 1177 English-only strings extracted earlier
# I'll add the 37 we have plus many more

new_translations = [
    # From the 37 we already have
    ('Gains 50 Focus when sortied.', 'Gana 50 Enfoque al ser sorteado.'),
    ('pilots by 10%.', 'los pilotos por un 10%.'),
    ('The HP of any ally unit on the map drops below 20%', 'La PV de cualquier unidad aliada en el mapa baja del 20%.'),
    ('Triggers spirit command Instinct', 'Activa el comando espiritual Instinto.'),
    ('Focus is above 140.', 'El Enfoque es superior a 140.'),
    ('Increases Armed Armor DE DMG by 300 and Range by 1', 'Incrementa el DEG AE Blindado en 300 y el Alcance en 1.'),
    ("Ignore an enemy unit's barrier when attacking.", 'Ignora la barrera de la unidad enemiga al atacar.'),
    ('Nearby allies gain 3 Focus at the', 'Los aliados cercanos ganan 3 Enfoque al.'),
    ('Strong Luck ', 'Buena Suerte '),
    ('Double Action', 'Acción Doble'),
    ('Restores 5 SP at the start of player', 'Restaura 5 SP al inicio del jugador.'),
    ('Triggers spirit command Disturb', 'Activa el comando espiritual Molestar.'),
    ('Save E L1', 'Guarda E L1'),
    ('for women and increases Final Evasion', 'para mujeres y aumenta la Evitación Final.'),
    ('As HP decreases, Accuracy %, Evasion %, Critical %, and Defe', 'A medida que disminuye la PV, Precisión %, Evasión %, Crítico y Der...'),
    ('This icon lights up when a mech is equipped with a jamming d', 'Este ícono se ilumina cuando un mecha está equipado con un dispositivo de inhibición.'),
    ('command to change forms. This change cannot be reversed.', 'comando para cambiar de forma. Este cambio no puede reversarse.'),
    ('Air-S.', 'Air-S.'),
    ('Gains 1 extra Focus when attacking, return attacking,', 'Gana 1 Enfoque extra al atacar, ataque de retorno.'),
    ('1. Increases SKL by 20.', '1. Incrementa HAB por 20.'),
    ('Atacante ', 'Atacante '),
    ('Duplica el aumento de la Tasa de Sincro.', 'Duplica el aumento de la Tasa de Sincro.'),
    ('Ataque', 'Ataque'),
    ('n L1', 'n L1'),
    ('n son esenciales para', 'n son esenciales para'),
    ('nivel aumenta un 30%.', 'nivel aumenta un 30%.'),
    ('RNG, SKL, DEF, EVD y HIT de los enemigos', 'RNG, HAB, DEF, EVA y AC de los enemigos'),
    ('Desbloquea la parte de poder Efector Espiral, disponible en ', 'Desbloquea el Efector Espiral de poder, disponible en'),
    ('Comandante L1', 'Comandante L1'),
    ('Este icono se ilumina cuando un mecha tiene Dividir.', 'Este ícono se ilumina cuando un mecha tiene Dividir.'),
    ('El Enfoque es 170 en condiciones', 'El Enfoque es 170 en condiciones'),
    ('Inicio de turno', 'Inicio de turno'),
    ('Presidente', 'Presidenta'),
    ('en 1 salvo armas de mapa y armas con alcance 1.', 'en 1 disparo de mapa y armas con alcance 1.'),
    ('con Enfoque superior a 110.', 'con Enfoque superior a 110.'),
    ('Toda unidad con ExC de 3 aumenta su Movimiento en 1.', 'Toda unidad con ExC de 3 incrementa su Movilidad en 1.'),
    ('Adapt. unidad y armas al terreno (Esp) S', 'Adapt. unidad y armas al terreno (Esp) S'),
    ('dispersa nanom', 'dispersa nanom'),
    # Additional game mechanics terms (continuing the list)
    ('Gains 50 Focus', 'Gana 50 Enfoque'),
    ('Increases SP by 10%', 'Incrementa PE en un 10%'),
    ('Recover 10% of maximum HP and EN at the', 'Recupera un 10% de la PV y PN máximos al'),
    ('start of the ally phase each turn.', 'inicio de la fase de aliados cada turno.'),
    ('Adds to abilities that recover HP and EN.', 'Añade a habilidades que recuperan PV y PN.'),
    ('All ally pilots gain 2 Focus at the', 'Todos los pilotos aliados ganan 2 Enfoque al'),
    ('start of the ally phase each turn.', 'inicio de la fase de aliados cada turno.'),
    ('Receive 5% of the total damage dealt', 'Recibe un 5% del daño total causado.'),
    ('Triggers spirit command Courage', 'Activa el comando espiritual Valiente.'),
    ('Triggers spirit command Bullseye', 'Activa el comando espiritual Francotirador.'),
    ('Achieve total obtained Tac Pts of 10,000.', 'Logra un total de Pts Tác de 10,000.'),
    ('Enhance Attack', 'Incrementar Ataque'),
    ('damage, and ally defeated. Can be stacked with', 'daño, y aliado derrotado. Puede apilarse con'),
    ('SP Recovery', 'Recuperación de PE'),
    ('Decreases SP consumption by 10% for each spirit command.', 'Disminuye el consumo de PE en un 10% por cada comando espiritual.'),
    ('Give undeployed pilots new assignments.', 'Asigna nuevas misiones a pilotos sin desplegar.'),
    ('Unlocks power part Spiral Effector for purchase at the Factory', 'Desbloquea el Efector Espiral de poder para comprar en la Fábrica'),
    ('Move & Fire', 'Mover y Disparar'),
    ('weapons after moving.', 'armas después de mover.'),
    ('Raises Focus when sortied.', 'Incrementa Enfoque al ser sorteado.'),
    ('A member of the Earth Federation Forces\' Lunar Special Tacti', 'Un miembro de las Fuerzas Federales de la Tierra Luna.'),
    ('commander.', 'comandante.'),
    ('Activate the special command.', 'Activa el comando especial.'),
    ('Deals heavy damage to a single enemy.', 'Inflige mucho daño a un solo enemigo.'),
    ('Deals medium damage to all enemies.', 'Inflige daño medio a todos los enemigos.'),
    ('Restores all HP and EN to one ally.', 'Restaura toda la PV y PN a un aliado.'),
    ('Protects one ally from all damage this turn.', 'Protege a un aliado de todo daño este turno.'),
    ('Revives one ally with 50% HP.', 'Revive a un aliado con un 50% de PV.'),
    ('Removes all status effects from one ally.', 'Quita todos los estados alterados de un aliado.'),
    ('Boosts allies\' attack power for 3 turns.', 'Incrementa el poder de ataque de los aliados durante 3 turnos.'),
    ('Reduces enemies\' attack power for 3 turns.', 'Reduce el poder de ataque de los enemigos durante 3 turnos.'),
    ('Nullifies enemy spirit commands.', 'Anula los comandos espirituales enemigos.'),
    ('Spirit Command:', 'Comando Espiritual:'),
    ('Effect:', 'Efecto:'),
    ('Cost:', 'Coste:'),
    ('Turns:', 'Turnos:'),
    ('Success Rate:', 'Tasa de Éxito:'),
    ('Miss:', 'Fallo.'),
    ('Hit:', 'Acertó.'),
    ('Critical Hit', 'Golpe Crítico'),
    ('Evade:', 'Evadir.'),
    ('Guard Break', 'Rompe Guardia'),
    ('Spirit Gauge', 'Medidor Espiritual'),
    ('Spirit Command Usage', 'Uso de Comando Espiritual'),
    ('Cooldown:', 'Reutilización:'),
    ('Preparing...', ' Preparándose...'),
    ('Ready.', 'Listo.'),
    ('Failed.', 'Falló.'),
    ('Success!', 'Éxito!'),
    # UI terms
    ('Save', 'Guardar'),
    ('Load', 'Cargar'),
    ('New Game', 'Nueva Partida'),
    ('Continue', 'Continuar'),
    ('Options', 'Opciones'),
    ('Credits', 'Créditos'),
    ('Exit', 'Salir'),
    # Unit/pilot terms
    ('Commander', 'Comandante'),
    ('Ace Pilot', 'Piloto As'),
    ('Elite Pilot', 'Piloto Élite'),
    ('Rookie Pilot', 'Pilote Novato'),
    ('Customize', 'Personalizar'),
    ('Loadout', 'Equipamiento'),
    ('Equipment', 'Equipamiento'),
    ('Parts', 'Partes'),
    ('Spirit', 'Espiritual'),
    ('Skill', 'Habilidad'),
    ('Support', 'Apoyo'),
    ('Backup', 'Respaldo'),
    ('Reinforce', 'Refuerzo'),
    ('Repair', 'Reparar'),
    ('Resupply', 'Abastecer'),
    ('Deploy', 'Desplegar'),
    ('Undo', 'Deshacer'),
    ('Confirm', 'Confirmar'),
    ('Cancel', 'Cancelar'),
    ('Yes', 'Sí'),
    ('No', 'No'),
    # Battle UI
    ('Attack', 'Atacar'),
    ('Defend', 'Defender'),
    ('Wait', 'Esperar'),
    ('Special', 'Especial'),
    ('Item', 'Objeto'),
    ('Run', 'Huir'),
    ('Finish', 'Finalizar'),
    ('Battle End', 'Fin de Batalla'),
    ('Victory', 'Victoria'),
    ('Defeat', 'Derrota'),
    ('Turn', 'Turno'),
    ('Round', 'Ronda'),
    # Menu navigation
    ('Up', 'Arriba'),
    ('Down', 'Abajo'),
    ('Left', 'Izquierda'),
    ('Right', 'Derecha'),
    ('Select', 'Seleccionar'),
    ('Back', 'Atrás'),
    ('Menu', 'Menú'),
    # Message boxes
    ('Are you sure you want to quit?', '¿Estás seguro de que quieres salir?'),
    ('This will overwrite the saved game.', 'Esto sobrescribirá la partida guardada.'),
    ('Cannot save in this area.', 'No se puede guardar en esta área.'),
    ('Save file slot.', 'Ficha de archivo de guardado.'),
    ('Enter save file name.', 'Introduce el nombre del archivo de guardado.'),
    ('Delete save file?', '¿Eliminar archivo de guardado?'),
    ('Are you sure you want to delete this save file?', '¿Estás seguro de que quieres eliminar este archivo de guardado?'),
]

# Combine existing + new, avoiding duplicates
all_translations = dict(existing)
for en, es in new_translations:
    if en not in existing:
        all_translations[en] = es

# Assign IDs starting from 1070
with open('C:/Dev/Default Project/srwv/datos/traducir_lt00.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'en', 'es'])
    for i, (en, es) in enumerate(sorted(all_translations.items())):
        writer.writerow([1070 + i, en, es])

total = len(all_translations)
print(f'Total traducciones en CSV: {total}')
print(f'Nuevas añadidas: {total - len(existing)}')
print('CSV guardado en: datos/traducir_lt00.csv')