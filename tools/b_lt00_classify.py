# -*- coding: utf-8 -*-
"""Clasificador de cadenas inglesas user-facing de B_LT00."""
import re

# Solo palabras distintivas: se excluyen ambiguas del espanol (en, a, al, el, de, un, o, etc.)
DISTINCT = re.compile(
    r"\b(the|you|your|this|that|these|those|and|with|for|from|attack|defend|power|"
    r"level|item|skill|move|range|damage|hit|miss|turn|phase|start|press|select|"
    r"confirm|cancel|name|point|points|ability|weapon|pilot|unit|enemy|allies|"
    r"action|end|next|continue|yes|are|was|will|not|can|what|when|where|who|how|"
    r"now|out|down|left|right|open|close|save|load|data|set|get|use|using|become|"
    r"increase|increases|decrease|decreases|effect|only|also|just|very|more|most|"
    r"less|than|then|there|here|their|them|his|her|its|our|they|she|one|two|three|"
    r"recover|receives?|gains?|amount|each|maximum|when|lands|critical|cleared|"
    r"during|battle|map|all|any|target|takes|until|after|before|first|time|added|"
    r"based|number|times|equivalent|adjacent|original|dealt|destroy|acquire|earn|"
    r"bronze|silver|gold|emblem|stacked|stackable|exp|raises?|ignores?|reduces?|"
    r"applies?|considered|calculated|accuracy|evasion|defense|focus|spirit|command|"
    r"ammo|squad|support|counter|repair|sortie|defeat|money|recovery|raises|lower|"
    r"lower|higher|opponent|weapons|attack|attacks|when|without|another|original)\b",
    re.I,
)
ES = set("áéíóúñÁÉÍÓÚ¿¡")


def is_en(s):
    """True si parece texto ingles user-facing (y no espanol)."""
    if not s or any(x in ES for x in s):
        return False
    hits = len(DISTINCT.findall(s))
    if hits >= 2:
        return True
    # una sola palabra distintiva basta si el resto es claramente ingles
    if hits == 1 and len(s) > 30:
        return True
    return False
