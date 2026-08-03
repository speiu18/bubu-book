#!/usr/bin/env python3
"""Build Consemnările mele — corrected chapters + HTML book + print styles."""

from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path("/workspace")
CARTE = ROOT / "carte"
CONTENT = CARTE / "content"
ILLUST = CARTE / "assets" / "illustrations"
SRC = ROOT / "source_joined.txt"

REPLACEMENTS = [
    ("naăstrușnic", "năstrușnic"),
    ("caselele", "casele"),
    ("aceestor", "acestor"),
    ("adoua", "a doua"),
    ("alegem de fiecare", "alegeam de fiecare"),
    ("coto-lac", "cotolac"),
    ("cât –l", "cât îl"),
    ("cât-l", "cât îl"),
    ("stand asa", "stând așa"),
    ("proecție", "proiecție"),
    ("regioanale", "regionale"),
    ("Buna ideie", "Bună idee"),
    ("părău pană", "pârâu până"),
    ("pană la", "până la"),
    ("pană acasă", "până acasă"),
    ("confectionam", "confecționam"),
    ("innobilam", "înnobilam"),
    ("intampla", "întâmpla"),
    ("experientă", "experiență"),
    ("înaintaşi", "înaintași"),
    ("stiea", "știa"),
    ("Culesa", "Culeșa"),
    ("Cuelsa", "Culeșa"),
    ("imbietor", "îmbietor"),
    ("Raspunea", "Răspundea"),
    ("indrăgea", "îndrăgea"),
    ("masuta", "măsuța"),
    ("cateva", "câteva"),
    ("zambet", "zâmbet"),
    ("imbraca", "îmbrăca"),
    ("înfierbană", "înfierbânta"),
    ("sangele", "sângele"),
    ("sa i înmoaie", "să i se înmoaie"),
    ("Cand s-a", "Când s-a"),
    ("acasă ranit", "acasă rănit"),
    ("solda militara", "solda militară"),
    ("romani d-ai", "români d-ai"),
    ("Targu Neamt", "Târgu Neamț"),
    ("cumparaturi", "cumpărături"),
    ("cumpa raturi", "cumpărături"),
    ("campului", "câmpului"),
    ("atinci când", "atunci când"),
    ("chiama", "chema"),
    ("zaboveam", "zăboveam"),
    ("mancare", "mâncare"),
    ("adresandu-se", "adresându-se"),
    ("smantana", "smântână"),
    ("grasa -", "grasă —"),
    ("cumîi", "cum îi"),
    ("intampla sa", "întâmpla să"),
    ("neobisnuite", "neobișnuite"),
    ("prăjeasca", "prăjească"),
    ("pranzului", "prânzului"),
    ("bors dres", "borș dres"),
    ("de de a mea", "de a mea"),
    ("In politică", "În politică"),
    ("lasă sapă", "lasă sapa"),
    ("gradină", "grădină"),
    ("crastoanelele", "căstronașele"),
    ("confeționând", "confecționând"),
    ("întîi", "întâi"),
    ("vietuiau", "viețuiau"),
    ("stră moașele", "strămoașele"),
    ("Humulesti", "Humulești"),
    ("jumatate", "jumătate"),
    ("ceasta se", "aceasta se"),
    ("îanite de", "înainte de"),
    ("bogati", "bogați"),
    ("vântrura", "vânturau"),
    ("Semintele", "Semințele"),
    ("plcintă", "plăcintă"),
    ("aștepatei", "așteptatei"),
    ("atrificial", "artificial"),
    ("depășeste", "depășește"),
    ("învârstă", "în vârstă"),
    ("dinstinctive", "distinctive"),
    ("aceiași", "aceeași"),
    ("teriminare", "terminare"),
    ("ragelei", "ragilei"),
    ("gosodărie", "gospodărie"),
    ("îceput", "început"),
    ("desfașurau", "desfășurau"),
    ("Mai tărziu", "Mai târziu"),
    ("fcea de către", "făcea de către"),
    ("aceast ă", "această"),
    ("mecanizrea", "mecanizarea"),
    ("halucicogene", "halucinogene"),
    ("Muți s-au", "Mulți s-au"),
    ("declaratii", "declarații"),
    ("desăvâșită", "desăvârșită"),
    ("știea", "știa"),
    ("Intre timp", "Între timp"),
    ("oamintire", "o amintire"),
    ("lăcomiia strică omeniia", "lăcomia strică omenia"),
    ("inecau", "înecau"),
    ("simțem burta", "simțeam burta"),
    ("hăndrălăiii", "hăndrălăii"),
    ("nivideau", "împărțeau"),
    ("vacantă", "vacanță"),
    ("transparent ;", "transparente;"),
    ("dr păr", "de păr"),
    ("Ș acum", "Și acum"),
    ("cunoscândui-se", "cunoscându-i-se"),
    ("albinile", "albinele"),
    ("Iazulie", "Iazurile"),
    ("trimeteau", "trimiteau"),
    ("punem în cosul", "puneam în coșul"),
    ("sau înrădăcinat", "s-au înrădăcinat"),
    ("in hârtia", "în hârtia"),
    ("cprioară", "căprioară"),
    ("pănă la", "până la"),
    ("vanatul", "vânatul"),
    ("agațat", "agățat"),
    ("pustii", "puștii"),
    ("î-l prezenta", "îl prezenta"),
    ("vânatoare", "vânătoare"),
    ("vânatorii", "vânătorii"),
    ("ramase", "rămase"),
    ("părintecă", "părintească"),
    ("pamânt", "pământ"),
    ("asteptând", "așteptând"),
    ("întrbam", "întrebam"),
    ("binicăi", "bunicii"),
    ("Dute și", "Du-te și"),
    ("vre-un", "vreun"),
    ("încetisor", "încetișor"),
    ("In momentul", "În momentul"),
    ("facută", "făcută"),
    ("trăisuță", "trăistuță"),
    ("tigară", "țigară"),
    ("in gură", "în gură"),
    ("înegrită", "înnegrită"),
    ("înfăsurare", "înfășurare"),
    ("In timp", "În timp"),
    ("Di piatra", "Din piatra"),
    ("mscă", "mișca"),
    ("intrebări", "întrebări"),
    ("ma i face", "mai face"),
    ("acsă", "acasă"),
    ("aproppia", "apropia"),
    ("s-a facut", "s-a făcut"),
    ("iși iubesc", "își iubesc"),
    ("barbați", "bărbați"),
    ("pveștile", "poveștile"),
    ("a căror maluri", "ale căror maluri"),
    ("Letopisețiul", "Letopisețul"),
    ("stim că", "știm că"),
    ("pârae", "pâraie"),
    ("pmenită", "pomenită"),
    ("hiară", "fiară"),
    ("arata \\lunca", "arăta lunca"),
    ("arata lunca", "arăta lunca"),
    ("săgeti", "săgeți"),
    ("jerfă", "jertfă"),
    ("Dragos", "Dragoș"),
    ("fiecae", "fiecare"),
    ("srăbunicul", "străbunicul"),
    ("tufisuri", "tufișuri"),
    ("pentu păsări", "pentru păsări"),
    ("decsindă", "descindă"),
    ("de cât să", "decât să"),
    ("intindea", "întindea"),
    ("îndeleniciri", "îndeletniciri"),
    ("ocupatiile", "ocupațiile"),
    ("preocuparile", "preocupările"),
    ("specealizau", "specializau"),
    ("tesător", "țesător"),
    ("tesutul", "țesutul"),
    ("usurință", "ușurință"),
    ("energiea", "energia"),
    ("Fiind -că", "Fiindcă"),
    ("am șă", "am să"),
    ("îtreabă", "întreabă"),
    ("știeam", "știam"),
    ("plimare", "plimbare"),
    ("îmidaivoie", "îmi dai voie"),
    ("impreună", "împreună"),
    ("buncii", "bunicii"),
    ("înșiret", "înșirat"),
    ("tractiune", "tracțiune"),
    ("in plus", "în plus"),
    ("vitei si", "viței și"),
    ("vre-o", "vreo"),
    ("îmreună", "împreună"),
    ("s- a", "s-a"),
    ("incumetat", "încumetat"),
    ("Ceilalti", "Ceilalți"),
    ("căstorit", "căsătorit"),
    ("fostilor", "foștilor"),
    ("tehnologig", "tehnologic"),
    ("cădura", "căldura"),
    ("ultimile", "ultimele"),
    ("Desleg", "Dezleg"),
    ("traducator", "traducător"),
    ("respectoși", "respectuoși"),
    ("Ci-că", "Cicǎ"),
    ("Stefan", "Ștefan"),
    ("omenii aceștea", "oamenii aceștia"),
    ("on hohot", "un hohot"),
    ("Moldvei", "Moldovei"),
    ("placute", "plăcute"),
    ("părăului", "pârâului"),
    ("mai de parte", "mai departe"),
    ("proursoare", "propulsoare"),
    ("sau oprit", "s-au oprit"),
    ("trebuiea", "trebuia"),
    ("moaară", "moară"),
    ("înteaga", "întreaga"),
    ("fluient", "fluent"),
    ("șoșotului", "șopotului"),
    ("a al apei", "al apei"),
    ("bineîțeles", "bineînțeles"),
    ("greutate ei", "greutatea ei"),
    ("întradevăr", "într-adevăr"),
    ("zdroobea", "zdrobea"),
    ("amonizându-se", "armonizându-se"),
    ("continuîdu", "continuându"),
    ("pînă la", "până la"),
    ("tebuia", "trebuia"),
    ("însetete", "însetate"),
    ("calu ,", "calul,"),
    ("mîngâiat", "mângâiat"),
    ("Costsche", "Costache"),
    ("dupa ce", "după ce"),
    ("atelieru", "atelierul"),
    ("pregatire", "pregătire"),
    ("Între-timp", "Între timp"),
    ("știubee", "știubeie"),
    ("modifiat", "modificat"),
    ("fata bucătăriei", "fața bucătăriei"),
    ("unnde", "unde"),
    ("așteapă", "așteaptă"),
    ("căte-un", "câte-un"),
    ("mergrgeam", "mergeam"),
    ("învățăm unii", "învățam unii"),
    ("mijlacele", "mijloacele"),
    ("peștel ", "peștele "),
    ("împarțire", "împărțire"),
    ("ditrugeu", "distrugeau"),
    ("dânt iar", "dând iar"),
    ("pșnice", "pașnice"),
    ("povestile", "poveștile"),
    ("sară !", "seară!"),
    ("piciarle", "picioarele"),
    ("zvârgoleau", "zvârcoleau"),
    ("matușei", "mătușei"),
    ("Ți- so", "Ți s-o"),
    ("ptins", "prins"),
    ("fceau", "făceau"),
    ("amăndouă", "amândouă"),
    ("undelemn", "untdelemn"),
    ("musa-i", "musai"),
    ("* 89", "’89"),
    ("in fiecare", "în fiecare"),
    ("si la amintiri", "și la amintiri"),
    ("vremurilor si", "vremurilor și"),
    ("ca să", "ca să"),
    ("bineînțeles ca", "bineînțeles că"),
    ("senile", "șenile"),
    ("foița de", "foiță de"),
    ("Naționale", "Naționale"),
    ("gipiesul", "GPS-ul"),
    ("7o de ani", "70 de ani"),
    ("întrbări", "întrebări"),
    ("căăă", "că"),
    ("Canabis", "cânepă"),
    ("CANABIS ;;", "CANNABIS."),
    ("CANABIS", "cannabis"),
]


def apply_word_fixes(text: str) -> str:
    text = re.sub(r"(?<=[.!?…])\s+\d{1,2}\s+(?=[A-ZĂÂÎȘȚ])", " ", text)
    text = re.sub(r"\s+\d{1,2}\s+(?=Și |Deci |Dar |Pe |Eu |Ne |Mai |Când |Totuși |Ei |În |Din |După |La |Cu |Noi |Mama |Tata |Bunica |Bunicu |Așa |Și |O |Se |Ca )", " ", text)
    text = re.sub(r"(?<![./\d])\s+\d{1,2}\s+(?=[A-ZĂÂÎȘȚa-zăâîșț„])", " ", text)
    text = text.replace(",,", "„")
    text = text.replace("''", "”")
    text = re.sub(r"(?<!\w)'(?!\w)", "”", text)

    reps = sorted(REPLACEMENTS, key=lambda x: -len(x[0]))
    for a, b in reps:
        text = text.replace(a, b)

    text = re.sub(r"\bsi\b", "și", text)
    text = re.sub(r"\bSi\b", "Și", text)
    text = re.sub(r"\bin\b", "în", text)
    text = re.sub(r"\bIn\b", "În", text)
    text = re.sub(r"\bcand\b", "când", text)
    text = re.sub(r"\bCand\b", "Când", text)
    text = re.sub(r"\bpana\b", "până", text)
    text = re.sub(r"\bPana\b", "Până", text)
    text = re.sub(r"\bintr-\b", "într-", text)
    text = re.sub(r"\bIntr-\b", "Într-", text)
    text = re.sub(r"\basa\b", "așa", text)
    text = re.sub(r"\bAsa\b", "Așa", text)
    text = re.sub(r"\bdecat\b", "decât", text)
    text = re.sub(r"\bcat\b", "cât", text)
    text = re.sub(r"\bCat\b", "Cât", text)
    text = re.sub(r"\bmai tarziu\b", "mai târziu", text)

    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r" +\n", "\n", text)
    # Polish quotes spacing
    text = re.sub(r"„\s+", "„", text)
    text = re.sub(r"\s+”", "”", text)
    text = re.sub(r"\.{4,}", "…", text)
    text = re.sub(r"…{2,}", "…", text)
    text = text.replace("Cicǎ", "Cică")
    text = text.replace("Aaceasta", "Aceasta")
    text = text.replace("cruța", "căruța")
    text = text.replace("proursoare", "propulsoare")
    text = text.replace("atelierull", "atelierul")
    text = text.replace("di-ta-mai", "dat-amai")
    text = text.replace("doanda-doanda", "doamda-doamda")
    text = text.replace("bunatatea", "bunătatea")
    text = text.replace("pentru ca acum", "pentru că acum")
    text = text.replace("Pâna la urmă", "Până la urmă")
    text = text.replace("lânga maidanul", "lângă maidanul")
    text = text.replace("mai tine minte", "mai ține minte")
    text = text.replace("din natura.", "din natură.")
    text = text.replace("Ne luăm rolul", "Ne luam rolul")
    text = text.replace("şi-l jucăm", "și-l jucam")
    text = text.replace("fantana", "fântâna")
    text = text.replace("contrare pe atunci", "contrarietate pe atunci")
    text = text.replace("numita Deleni", "numită Deleni")
    text = text.replace("numita Cot", "numită Cot")
    text = text.replace("Soimărești", "Șoimărești")
    text = text.replace("toata ziua", "toată ziua")
    text = text.replace("Mânâncă", "Mănâncă")
    text = text.replace("de-o viaţa", "de-o viață")
    text = text.replace("Sarut-mana", "Sărut-mâna")
    text = text.replace("Sarut mana", "Sărut mâna")
    text = text.replace("indrăgea", "îndrăgea")
    text = text.replace("camasa alba", "cămașa albă")
    text = text.replace("sociabila", "sociabilă")
    text = text.replace("buna gospodina", "bună gospodină")
    text = text.replace("placintele", "plăcintele")
    text = text.replace("raspundeam", "răspundeam")
    text = text.replace("mananc", "mănânc")
    text = text.replace("Cateodata", "Câteodată")
    text = text.replace("cateodata", "câteodată")
    text = text.replace("țara cu", "țară cu")
    text = text.replace("plecăm acasă", "plecam acasă")
    text = text.replace("Plecăm totuși", "Plecam totuși")
    text = text.replace("de razboi", "de război")
    text = text.replace("ajunse acasa ranit", "ajunse acasă rănit")
    text = text.replace("pârăului", "pârâului")
    text = text.replace("ereu și ele", "erau și ele")
    text = text.replace("înafara", "în afara")
    text = text.replace("incepand", "începând")
    text = text.replace("incepand", "începând")
    text = text.replace("incepând", "începând")
    text = text.replace("cere se folosește", "care se folosește")
    text = text.replace("sase -șapte", "șase-șapte")
    text = text.replace("creia și", "crea și")
    text = text.replace("Răucesti", "Răucești")
    text = text.replace("Pe vremea ceia", "Pe vremea aceea")
    text = text.replace("transparent;", "transparente;")
    text = text.replace("de-și mi-am", "deși mi-am")
    text = text.replace("trimetea:", "trimitea:")
    text = text.replace("muștireule", "muștiroule")
    text = text.replace("alghinele", "albinele")
    text = text.replace("discutind", "discutând")
    text = text.replace("îmbatrănit", "îmbătrânit")
    text = text.replace("adevarate", "adevărate")
    text = text.replace("adaposti", "adăposti")
    text = text.replace("cân s-a", "când s-a")
    text = text.replace("colectivzare", "colectivizare")
    text = text.replace("stătem cu", "stăteam cu")
    text = text.replace("mai msca", "mai mișca")
    text = text.replace("tereierat", "treierat")
    text = text.replace("întâpla", "întâmpla")
    text = text.replace("întâplat", "întâmplat")
    text = text.replace("devotati", "devotați")
    text = text.replace("ramificatii", "ramificații")
    text = text.replace("pietris", "pietriș")
    text = text.replace("vremea aceia", "vremea aceea")
    text = text.replace("frământîndu", "frământându")
    text = text.replace("cân am", "când am")
    text = text.replace("pănă termina", "până termina")
    text = text.replace("inaintea", "înaintea")
    text = text.replace("bucatăria", "bucătăria")
    text = text.replace("să între în", "să intre în")
    text = text.replace("s-au dat inapoi", "s-au dat înapoi")
    text = text.replace("Măria Să", "Măria Sa")
    text = text.replace("garda să mergea", "garda sa mergea")
    text = text.replace("constructie", "construcție")
    text = text.replace("diferentă", "diferență")
    text = text.replace("incetau", "încetau")
    text = text.replace("pe lân ei", "pe lângă ei")
    text = text.replace("adăncă", "adâncă")
    text = text.replace("Bratul râului", "Brațul râului")
    text = text.replace("amuși se face sară", "amuși se face seară")
    text = text.replace("un peste)", "un pește)")
    text = text.replace("puii mic ", "puii mici ")
    text = text.replace("Ți s-o fi facut", "Ți s-o fi făcut")
    text = text.replace("frip pe plita", "fript pe plită")
    return text.strip()


def clean_text(text: str) -> str:
    return apply_word_fixes(text)


def paragraphize(body: str) -> list[str]:
    # Keep dialogue lines separate when possible
    sentences = re.split(r"(?<=[.!?…])\s+", body)
    paras: list[str] = []
    buf: list[str] = []
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        # Dialogue starts
        if s.startswith("-") or s.startswith("—") or s.startswith("„-"):
            if buf:
                paras.append(" ".join(buf))
                buf = []
            paras.append(s)
            continue
        buf.append(s)
        if len(buf) >= 3 or (len(buf) >= 2 and len(" ".join(buf)) > 480):
            paras.append(" ".join(buf))
            buf = []
    if buf:
        paras.append(" ".join(buf))
    return paras


CHAPTER_META = [
    {
        "id": "consemnari",
        "title": "Unde ești, copilărie?",
        "source_title": "CONSEMNARI",
        "image": "cover-culesa.jpg",
        "caption": "Pârâul Culeșa, izvorât din Culmea Stânișoarei",
    },
    {
        "id": "maidan",
        "title": "Din maidan",
        "source_title": "Din maidan",
        "image": "cap-maidan.jpg",
        "caption": "Jocurile de pe maidan și haiducii de pe malul Culeșei",
        "extra_images": [
            ("cap-haiduci.jpg", "De-a haiducii și potera, printre răchițe"),
        ],
    },
    {
        "id": "scaldat",
        "title": "Scăldatul pe Culeșa",
        "source_title": "Scăldatul pe Culeşa",
        "image": "cap-scaldat.jpg",
        "caption": "Bulboana de la cotitura pârâului",
        "extra_images": [
            ("cap-bunica-bors.jpg", "Borșul de pește al bunicii Sultana"),
        ],
    },
    {
        "id": "canepa",
        "title": "Cânepa",
        "source_title": "CANNABIS",
        "image": "cap-canepa.jpg",
        "caption": "Drumul la topit cânepa, pe apele Râșcăi",
    },
    {
        "id": "claca",
        "title": "La clacă",
        "source_title": "LA CLACĂ",
        "image": "cap-claca.jpg",
        "caption": "Serile de clacă, cu tors, cântec și chiroști",
    },
    {
        "id": "rauesti",
        "title": "Drumeții la bunicii din Răucești",
        "source_title": "DRUMEȚII LA BUNICII",
        "image": "cap-rauesti.jpg",
        "caption": "Pe drumul de tractoare, până la bunicii din Răucești",
        "extra_images": [
            ("cap-bunicu-iaz.jpg", "Bunicul Cosău, la iazul lui"),
        ],
    },
    {
        "id": "lunca",
        "title": "Prin lunca Moldovei",
        "source_title": "PRIN LUNCA MOLDOVEI",
        "image": "cap-lunca.jpg",
        "caption": "Lunca Moldovei, morile de apă și gârlele copilăriei",
        "extra_images": [
            ("cap-drum-moara.jpg", "Cu mamuca, pe drumul spre moară"),
        ],
    },
]


def split_chapters(text: str) -> dict[str, str]:
    # Markers may sit on own lines or be inline after cleaning collapsed newlines.
    pattern = re.compile(
        r"(?:^|\n)\s*###\s*(CONSEMNARI|Din maidan|Scăldatul pe Culeşa|Scăldatul pe Culeșa|CANNABIS|LA CLACĂ|DRUMEȚII LA BUNICII(?:\s+DIN RĂUCEȘTI)?|PRIN LUNCA MOLDOVEI)\s*",
        re.M,
    )
    matches = list(pattern.finditer(text))
    if not matches:
        # Fallback: titles without ###
        pattern2 = re.compile(
            r"(CONSEMNARI|Din maidan|Scăldatul pe Culeşa|CANNABIS|LA CLACĂ|DRUMEȚII LA BUNICII(?:\s+DIN RĂUCEȘTI)?|PRIN LUNCA MOLDOVEI)\b"
        )
        matches = list(pattern2.finditer(text))
        out: dict[str, str] = {}
        for i, m in enumerate(matches):
            title = m.group(1).strip()
            start = m.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            body = text[start:end].strip()
            body = re.sub(r"\s*Fila\s+\d+.*$", "", body, flags=re.I | re.S)
            # Normalize titles
            if title.startswith("DRUMEȚII"):
                title = "DRUMEȚII LA BUNICII"
            if title.startswith("Scăldatul"):
                title = "Scăldatul pe Culeşa"
            out[title] = body
        return out

    out = {}
    for i, m in enumerate(matches):
        title = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        body = re.sub(r"\s*Fila\s+\d+.*$", "", body, flags=re.I | re.S)
        if title.startswith("DRUMEȚII"):
            title = "DRUMEȚII LA BUNICII"
        if title.startswith("Scăldatul"):
            title = "Scăldatul pe Culeşa"
        out[title] = body
    return out


def paras_to_html(paras: list[str]) -> str:
    chunks = []
    for p in paras:
        cls = ' class="dialogue"' if p.startswith(("-", "—")) else ""
        chunks.append(f"<p{cls}>{html.escape(p)}</p>")
    return "\n".join(chunks)


def build_html(chapters_html: list[tuple[dict, str]]) -> str:
    nav_items = "\n".join(
        f'<li><a href="#{meta["id"]}">{html.escape(meta["title"])}</a></li>'
        for meta, _ in chapters_html
    )
    sections = []
    for meta, body_html in chapters_html:
        extras = ""
        for img, cap in meta.get("extra_images", []):
            extras += f"""
      <figure class="illust illust-inline">
        <img src="assets/illustrations/{img}" alt="{html.escape(cap)}" loading="lazy" />
        <figcaption>{html.escape(cap)}</figcaption>
      </figure>
"""
        # Insert extras roughly after first third of paragraphs
        parts = body_html.split("</p>")
        if extras and len(parts) > 8:
            mid = max(4, len(parts) // 3)
            body_with_extra = (
                "</p>".join(parts[:mid]) + "</p>\n" + extras + "</p>".join(parts[mid:])
            )
        else:
            body_with_extra = body_html + extras

        sections.append(
            f"""
    <section class="chapter" id="{meta["id"]}">
      <header class="chapter-head">
        <p class="chapter-kicker">Capitol</p>
        <h2>{html.escape(meta["title"])}</h2>
      </header>
      <figure class="illust illust-hero">
        <img src="assets/illustrations/{meta["image"]}" alt="{html.escape(meta["caption"])}" />
        <figcaption>{html.escape(meta["caption"])}</figcaption>
      </figure>
      <div class="chapter-body">
        {body_with_extra}
      </div>
    </section>
"""
        )

    return f"""<!DOCTYPE html>
<html lang="ro">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Consemnările mele — Vasia Peiu</title>
  <meta name="author" content="Vasia Peiu" />
  <meta name="description" content="Consemnările mele — amintiri din copilăria de pe meleagurile Neamțului, de Vasia Peiu." />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,600;1,7..72,400&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="css/book.css" />
</head>
<body>
  <a class="skip" href="#cuprins">Sari la cuprins</a>

  <header class="cover" id="coperta">
    <div class="cover-media" aria-hidden="true">
      <img src="assets/illustrations/cover-culesa.jpg" alt="" />
    </div>
    <div class="cover-veil"></div>
    <div class="cover-content">
      <p class="cover-gift">Un cadou pentru tata</p>
      <h1>Consemnările mele</h1>
      <p class="cover-author">Vasia Peiu</p>
      <p class="cover-lead">Amintiri de pe malul Culeșei, din lunca Moldovei și din anii copilăriei.</p>
      <a class="cover-cta" href="#dedicatie">Deschide cartea</a>
    </div>
  </header>

  <main>
    <section class="dedication" id="dedicatie">
      <div class="dedication-inner">
        <p class="ornament" aria-hidden="true">❧</p>
        <h2>Dedicație</h2>
        <p>
          Pentru tatăl meu, <strong>Vasia Peiu</strong> — autorul acestor consemnări —
          cu dragoste, recunoștință și mândrie.
        </p>
        <p class="dedication-note">
          Am păstrat glasul poveștilor tale, am îngrijit textul și i-am alăturat ilustrații
          inspirate din lumile pe care le-ai scris: pârâul, maidanul, claca, cânepa,
          bunicii și lunca Moldovei.
        </p>
      </div>
    </section>

    <nav class="toc" id="cuprins" aria-label="Cuprins">
      <h2>Cuprins</h2>
      <ol>
        {nav_items}
      </ol>
    </nav>

    {"".join(sections)}

    <section class="colophon" id="colofon">
      <h2>Colofon</h2>
      <p>
        Text original: <strong>Vasia Peiu</strong>. Titlul: <em>Consemnările mele</em>.
        Ediție îngrijită ca dar de familie, cu corectură de limbă și ilustrații
        generate în stil acuarelă, inspirate din poveștile cărții.
      </p>
      <p class="colophon-place">Ținutul Neamțului · Culeșa · Râșca · Lunca Moldovei</p>
    </section>
  </main>

  <footer class="site-footer">
    <p><a href="#coperta">Înapoi la copertă</a></p>
  </footer>
  <script src="js/book.js"></script>
</body>
</html>
"""


def main() -> None:
    raw = SRC.read_text(encoding="utf-8")
    cleaned = clean_text(raw)
    (ROOT / "source_corrected.txt").write_text(cleaned, encoding="utf-8")

    by_title = split_chapters(cleaned)
    CONTENT.mkdir(parents=True, exist_ok=True)

    chapters_html: list[tuple[dict, str]] = []
    for meta in CHAPTER_META:
        body = by_title.get(meta["source_title"], "")
        if not body:
            # fuzzy match
            for k, v in by_title.items():
                if meta["source_title"].lower() in k.lower() or k.lower() in meta["source_title"].lower():
                    body = v
                    break
        if not body:
            raise SystemExit(f"Missing chapter body for {meta['source_title']}; have {list(by_title)}")

        # Special: first chapter also absorbed maidan start before "Din maidan" marker —
        # Din maidan is separate. For "Din maidan", body may start mid-thought; OK.

        paras = paragraphize(body)
        (CONTENT / f"{meta['id']}.txt").write_text(
            meta["title"] + "\n\n" + "\n\n".join(paras), encoding="utf-8"
        )
        chapters_html.append((meta, paras_to_html(paras)))

    html_out = build_html(chapters_html)
    (CARTE / "index.html").write_text(html_out, encoding="utf-8")
    print("Built", CARTE / "index.html")
    print("Chapters:", ", ".join(m["title"] for m, _ in chapters_html))
    for m, _ in chapters_html:
        print(f"  {m['id']}: {(CONTENT / (m['id'] + '.txt')).stat().st_size} bytes")


if __name__ == "__main__":
    main()
