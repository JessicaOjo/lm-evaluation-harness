import re
from sklearn.metrics import f1_score, accuracy_score
from lm_eval.utils import weighted_f1_score

LANGUAGE_VARIATIONS = {
    "Acehnese": {"acehnese"},
    "Ta’izzi-Adeni Arabic": {"ta’izzi-adeni arabic", "taizzi adeni arabic"},
    "Tunisian Arabic": {"tunisian arabic"},
    "Afrikaans": {"afrikaans"},
    "Amharic": {"amharic"},
    "Moroccan Arabic": {"moroccan arabic"},
    "Egyptian Arabic": {"egyptian arabic"},
    "Bambara": {"bambara", "bamanankan"},
    "Bemba": {"bemba"},
    "Chokwe": {"chokwe"},
    "Dinka": {"dinka"},
    "Dyula": {"dyula"},
    "Ewe": {"ewe"},
    "Fon": {"fon"},
    "French": {"french"},
    "Nigerian Fulfulde": {"nigerian fulfulde", "fulfulde", "fula"},
    "Hausa": {"hausa"},
    "Igbo": {"igbo"},
    "Kabyle": {"kabyle"},
    "Kamba": {"kamba"},
    "Kanuri": {"kanuri", "central kanuri", "yerwa kanuri"},
    "Kabiyè": {"kabiyè", "kabiye"},
    "Kabuverdianu": {"kabuverdianu", "cape verdean creole"},
    "Kikuyu": {"kikuyu", "gikuyu"},
    "Kinyarwanda": {"kinyarwanda", "ikinyarwanda"},
    "Kimbundu": {"kimbundu"},
    "Kikongo": {"kikongo", "kongo"},
    "Lingala": {"lingala"},
    "Luba-Kasai": {"luba-kasai", "tshiluba", "luba", "ciluba"},
    "Luganda": {"luganda"},
    "Luo": {"luo", "dholuo"},
    "Plateau Malagasy": {"plateau malagasy", "malagasy"},
    "Mossi": {"mossi"},
    "Northern Sotho": {"northern sotho", "sepedi", "pedi", "sesotho sa leboa"},
    "Nuer": {"nuer", "nueric"},
    "Nyanja": {"nyanja", "chichewa", "chewa"},
    "Oromo": {"oromo"},
    "Rundi": {"rundi", "kirundi"},
    "Sango": {"sango"},
    "Shona": {"shona", "chishona"},
    "Somali": {"somali"},
    "Sesotho": {"sesotho", "southern sotho"},
    "Swati": {"swati", "siswati"},
    "Sundanese": {"sundanese"},
    "Swahili": {"swahili", "kiswahili"},
    "Tigrinya": {"tigrinya"},
    "Tamasheq": {"tamasheq", "tamashek"},
    "Setswana": {"setswana", "tswana"},
    "Tsonga": {"tsonga"},
    "Tumbuka": {"tumbuka"},
    "Twi": {"twi", "akan"},
    "Umbundu": {"umbundu"},
    "Wolof": {"wolof"},
    "Xhosa": {"xhosa"},
    "Yoruba": {"yoruba"},
    "Standard Moroccan Tamazight": {
        "standard moroccan tamazight",
        "tamazight"
    },
    "Zulu": {"zulu", "isizulu"},
}

def normalize_text(strings):
    def get_blank_spaces_pattern():
        return re.compile(r"\s{3,}|\t")

    def remove_blank_spaces(text):
        text = re.sub(pattern=get_blank_spaces_pattern(), repl="", string=text)
        text = re.sub(r"\s+", " ", text)
        return text

    def remove_punctuation(text):
        my_punctuation = '!"$%&\'()*+,-./:;<=>?[\\]^_`{|}~•@.""-,`'
        text = re.sub(
            "[" + my_punctuation + "]+", " ", str(text)
        )  # strip punctuation
        return text

    def remove_articles(text):
        regex = re.compile(r"\b(a|an|the|isi|izi|ki|)\b", re.UNICODE)
        return re.sub(regex, " ", text)

    def lowercase(text):
        text = text.strip().lower()
        return text

    strings = remove_punctuation(strings)
    strings = remove_articles(strings)
    strings = remove_blank_spaces(strings)
    strings = lowercase(strings)

    return strings


def normalize_prediction(gold, text):
    pred = normalize_text(text).lower().strip()
    gold_norm = normalize_text(gold).lower().strip()

    # Empty / null output
    if pred == "":
        return "unknown"

    # Exact or substring match on canonical name
    if gold_norm in pred:
        return gold_norm

    # Match against language-specific variants
    aliases = LANGUAGE_VARIATIONS.get(gold, set())

    for alias in aliases:
        if alias in pred:
            return gold_norm

    return "unknown"


def calculate_f1(items):
    """
    Computes macro F1 for single-label LID.
    items: List[Tuple[target, prediction]]
    """
    targets, predictions = zip(*items)

    norm_preds = [
        normalize_prediction(g, p)
        for g, p in zip(targets, predictions)
    ]

    norm_gold = [normalize_text(g).lower().strip() for g in targets]

    print(f"Normalized Gold: {norm_gold}")  # Debugging line
    print(f"Normalized Predictions: {norm_preds}")  # Debugging line

    return f1_score(
        norm_gold,
        norm_preds,
        pos_label=norm_gold[0],
        average="binary"
    )


def calculate_acc(items):
    """
    Computes accuracy for single-label LID.
    items: List[Tuple[target, prediction]]
    """
    targets, predictions = zip(*items)

    norm_preds = [
        normalize_prediction(g, p)
        for g, p in zip(targets, predictions)
    ]

    norm_gold = [
        normalize_text(g).lower().strip()
        for g in targets
    ]

    return accuracy_score(norm_gold, norm_preds)
