from pathlib import Path
from typing import List, Optional, Dict
import random
import logging
from dataclasses import dataclass

import discord
from discord.ext import commands

# Configure logging
logger = logging.getLogger('AnimeCogs')

CHARACTER_MAPPINGS = {
    "one_piece": {
        "luffy": ["monkey d luffy", "monkey_d_luffy", "luffy", "strawhat"],
        "zoro": ["roronoa zoro", "roronoa_zoro", "zoro"],
        "nami": ["nami", "nami_(one_piece)"],
        "sanji": ["vinsmoke sanji", "vinsmoke_sanji", "sanji", "black leg"],
        "robin": ["nico robin", "nico_robin", "robin", "robin_(alabasta)", "robin_(cosplay)"],
        "uta": ["uta", "uta_(one_piece)"],
        "rebecca": ["rebecca", "rebecca_(one_piece)"],
        "carrot": ["carrot", "carrot_(one_piece)"],
        "bonney": ["jewelry bonney", "jewelry_bonney", "bonney"],
        "baby_5": ["baby 5", "baby_5", "baby five", "baby_five"],
        "boa_hancock": ["boa hancock", "boa_hancock", "hancock"],
        "vivi": ["nefertari vivi", "nefertari_vivi", "vivi"],
        "vinsmoke_reiju": ["vinsmoke reiju", "vinsmoke_reiju", "reiju"],
        "charlotte_linlin": ["big mom", "big_mom", "charlotte_linlin", "charlotte linlin", "linlin"],
        "kuina": ["shimotsuki kuina", "shimotsuki_kuina", "kuina"],
        "charlotte_smoothie": ["charlotte_smoothie", "charlotte smoothie", "smoothie"],
        "shirahoshi": ["shirahoshi", "princess shirahoshi", "princess_shirahoshi"],
        "kouzuki_hiyori": ["hiyori", "kouzuki hiyori", "kouzuki_hiyori"],
        "catarina_devon": ["devon", "catarina devon", "catarina_devon"],
        "perona": ["perona", "'ghost princess' perona", "ghost princess perona", "'ghost_princess'_perona",
                   "ghost_princess_perona"],
        "charlotte_flampe": ["charlotte_flampe", "charlotte flampe", "flampe"],
        "kouzuki_toki": ["kouzuki toki", "kouzuki_toki", "toki"],
        "alvida": ["alvida", "alvida_(one_piece)"],
        "kikunojo": ["kikunojo", "kikunojo_(one_piece)", "kiku"],
        "vegapunk_lilith": ["vegapunk lilith", "vegapunk_lilith", "lilith"],
        "kaya": ["kaya", "kaya_(one_piece)"],
        "monet": ["monet", "monet_(one_piece)"],
        "wanda": ["wanda", "wanda_(one_piece)"],
        "nico_olvia": ["nico olvia", "nico_olvia", "olvia"],
        "nojiko": ["nojiko"],
        "charlotte_pudding": ["charlotte pudding", "charlotte_pudding", "pudding"],
        "vegapunk_atlas": ["vegapunk atlas", "vegapunk_atlas", "atlas"],
        "vegapunk_york": ["vegapunk york", "vegapunk_york", "york"],
        "stussy": ["stussy", "stussy_(one_piece)"],
        "tashigi": ["tashigi"],
        "hina": ["hina", "hina_(one_piece)"],
        "isuka": ["isuka", "isuka_(one_piece)"]
    },

    "dota2": {
        "lina": ["lina", "lina inverse"],
        "crystal_maiden": ["crystal maiden", "crystal_maiden", "rylai"],
        "invoker": ["invoker", "kael"],
        "windrunner": ["windranger", "windrunner", "lyralei", "windranger_(dota)"],
        "marci": ["marci", "marci_(dota)"],
        "dark_willow": ["dark willow", "dark_willow"],
        "mirana": ["mirana", "mirana_(dota)"],
        "broodmother": ["broodmother", "broodmother_(dota)"],
        "dawnbreaker": ["dawnbreaker", "dawnbreaker_(dota)", "dawnbreaker_(dota_2)"],
        "death_prophet": ["death prophet", "death_prophet_(dota)"],
        "enchantress": ["enchantress", "enchantress_(dota)", "enchantress_(dota_2)"],
        "legion_commander": ["legion commander", "legion_commander_(dota)"],
        "luna": ["luna", "luna_(dota)"],
        "naga_siren": ["naga siren", "naga_siren_(dota)"],
        "phantom_assassin": ["phantom assassin", "phantom_assassin_(dota)"],
        "queen_of_pain": ["queen of pain", "queen_of_pain_(dota)"],
        "snapfire": ["snapfire"],
        "spectre": ["spectre", "spectre_(dota)"],
        "templar_assassin": ["templar assassin", "templar_assassin_(dota)"],
        "vengeful_spirit": ["vengeful spirit", "vengeful_spirit_(dota_2)"]
    },

    "naruto": {
        "tsunade": ["tsunade", "lady tsunade", "princess tsunade"],
        "sakura": ["sakura haruno", "sakura_haruno"],
        "hinata": ["hinata hyuga", "hinata_hyuga"],
        "tenten": ["tenten"],
        "temari": ["temari"],
        "kushina": ["kushina uzumaki", "kushina_uzumaki"],
        "sarada": ["sarada uchiha", "sarada_uchiha"],
        "himawari": ["himawari uzumaki", "himawari_uzumaki"],
        "ino": ["ino yamanaka", "ino_yamanaka"],
        "kurenai": ["kurenai yuhi", "kurenai_yuhi"],
        "anko": ["anko mitarashi", "anko_mitarashi"],
        "shizune": ["shizune"],
        "karin": ["karin uzumaki", "karin_uzumaki"],
        "konan": ["konan"],
        "mei": ["mei terumi", "mei_terumi"],
        "samui": ["samui"],
        "karui": ["karui"],
        "mabui": ["mabui"],
        "yugao": ["yugao uzuki", "yugao_uzuki"],
        "tsume": ["tsume inuzuka", "tsume_inuzuka"],
        "hana": ["hana inuzuka", "hana_inuzuka"],
        "natsu": ["natsu hyuga", "natsu_hyuga"],
        "yakumo": ["yakumo kurama", "yakumo_kurama"],
        "tsunami": ["tsunami"],
        "ayame": ["ayame"],
        "yugito": ["yugito nii", "yugito_nii"],
        "fuu": ["fuu"],
        "hokuto": ["hokuto"],
        "hanabi": ["hanabi hyuga", "hanabi_hyuga"],
        "moegi": ["moegi"],
        "sumire": ["sumire kakei", "sumire_kakei"],
        "chocho": ["chocho akimichi", "chocho_akimichi"],
        "mirai": ["mirai sarutobi", "mirai_sarutobi"],
        "wasabi": ["wasabi izuno", "wasabi_izuno"],
        "namida": ["namida suzumeno", "namida_suzumeno"]
    },

    "fairy_tail": {
        "lucy": ["lucy heartfilia", "lucy_heartfilia"],
        "erza": ["erza scarlet", "erza_scarlet", "titania"],
        "wendy": ["wendy marvell", "wendy_marvell"],
        "juvia": ["juvia lockser", "juvia_lockser"],
        "levy": ["levy mcgarden", "levy_mcgarden"],
        "mirajane": ["mirajane strauss", "mirajane_strauss"],
        "lisanna": ["lisanna strauss", "lisanna_strauss"],
        "cana": ["cana alberona", "cana_alberona"],
        "evergreen": ["evergreen"],
        "bisca": ["bisca connell", "bisca_connell"],
        "laki": ["laki olietta", "laki_olietta"],
        "kinana": ["kinana"],
        "mavis": ["mavis vermillion", "mavis_vermillion"],
        "meredy": ["meredy"],
        "ultear": ["ultear milkovich", "ultear_milkovich"],
        "yukino": ["yukino agria", "yukino_agria"],
        "minerva": ["minerva orlando", "minerva_orlando"],
        "kagura": ["kagura mikazuchi", "kagura_mikazuchi"],
        "milliana": ["milliana"],
        "flare": ["flare corona", "flare_corona"],
        "jenny": ["jenny realight", "jenny_realight"],
        "sherry": ["sherry blendy", "sherry_blendy"],
        "chelia": ["chelia blendy", "chelia_blendy"],
        "sorano": ["sorano agria", "sorano_agria", "angel"],
        "brandish": ["brandish μ", "brandish mu"],
        "dimaria": ["dimaria yesta", "dimaria_yesta"],
        "irene": ["irene belserion", "irene_belserion"],
        "hisui": ["hisui e fiore", "hisui_e_fiore"]
    },

    "dragon_ball": {
        "bulma": ["bulma briefs", "bulma_briefs"],
        "chi_chi": ["chi chi", "chi_chi"],
        "videl": ["videl"],
        "pan": ["pan"],
        "android_18": ["android 18", "c-18", "lazuli"],
        "bulla": ["bulla", "bra"],
        "launch": ["launch", "lunch"],
        "marron": ["marron"],
        "mai": ["mai"],
        "ranfan": ["ranfan"],
        "vados": ["vados"],
        "caulifla": ["caulifla"],
        "kale": ["kale"],
        "ribrianne": ["ribrianne", "brianne de chateau"],
        "oceanus": ["oceanus shenron", "princess oto"],
        "gine": ["gine"],
        "fasha": ["fasha", "selypa"],
        "zangya": ["zangya"],
        "towa": ["towa"],
        "supreme_kai_of_time": ["supreme kai of time", "chronoa"],
        "arale": ["arale norimaki", "arale_norimaki"]
    },

    "attack_on_titan": {
        "mikasa": ["mikasa ackerman", "mikasa_ackerman"],
        "annie": ["annie leonhart", "annie_leonhart"],
        "historia": ["historia reiss", "historia_reiss", "christa"],
        "sasha": ["sasha braus", "sasha_braus"],
        "hange": ["hange zoe", "hanji"],
        "ymir": ["ymir", "freckled ymir"],
        "pieck": ["pieck finger", "pieck_finger"],
        "gabi": ["gabi braun", "gabi_braun"],
        "frieda": ["frieda reiss", "frieda_reiss"],
        "carla": ["carla yeager", "carla_yeager"],
        "dina": ["dina fritz", "dina_fritz"],
        "petra": ["petra ral", "petra_ral"],
        "rico": ["rico brzenska", "rico_brzenska"],
        "yelena": ["yelena"],
        "kiyomi": ["kiyomi azumabito", "kiyomi_azumabito"],
        "louise": ["louise"],
        "nifa": ["nifa"],
        "lynne": ["lynne"],
        "ilse": ["ilse langnar", "ilse_langnar"],
        "nanaba": ["nanaba"]
    },

    "demon_slayer": {
        "nezuko": ["nezuko kamado", "nezuko_kamado"],
        "kanao": ["kanao tsuyuri", "kanao_tsuyuri"],
        "shinobu": ["shinobu kocho", "shinobu_kocho"],
        "kanae": ["kanae kocho", "kanae_kocho"],
        "mitsuri": ["mitsuri kanroji", "mitsuri_kanroji"],
        "daki": ["daki", "ume"],
        "tamayo": ["tamayo"],
        "makio": ["makio"],
        "suma": ["suma"],
        "hinatsuru": ["hinatsuru"],
        "aoi": ["aoi kanzaki", "aoi_kanzaki"],
        "kiyo": ["kiyo terauchi", "kiyo_terauchi"],
        "sumi": ["sumi nakahara", "sumi_nakahara"],
        "naho": ["naho takada", "naho_takada"],
        "goto": ["goto", "goto_san"],
        "amane": ["amane"],
        "mukago": ["mukago"],
        "ruka": ["ruka"],
        "hinaki": ["hinaki ubuyashiki", "hinaki_ubuyashiki"],
        "nichika": ["nichika ubuyashiki", "nichika_ubuyashiki"],
        "kuina": ["kuina ubuyashiki", "kuina_ubuyashiki"]
    },

    "jujutsu_kaisen": {
        "nobara": ["nobara kugisaki", "nobara_kugisaki"],
        "maki": ["maki zenin", "maki_zenin"],
        "mei_mei": ["mei mei", "mei_mei"],
        "miwa": ["kasumi miwa", "kasumi_miwa"],
        "momo": ["momo nishimiya", "momo_nishimiya"],
        "mai": ["mai zenin", "mai_zenin"],
        "yuki": ["yuki tsukumo", "yuki_tsukumo"],
        "rika": ["rika orimoto", "rika_orimoto"],
        "utahime": ["utahime iori", "utahime_iori"],
        "tsumiki": ["tsumiki fushiguro", "tsumiki_fushiguro"],
        "manami": ["manami suda", "manami_suda"],
        "saori": ["saori rokujo", "saori_rokujo"],
        "shoko": ["shoko ieiri", "shoko_ieiri"],
        "mimiko": ["mimiko hasaba", "mimiko_hasaba"],
        "nanako": ["nanako hasaba", "nanako_hasaba"]
    },

    "cowboy_bebop": {
        "faye": ["faye valentine", "faye_valentine"],
        "ed": ["edward wong", "radical ed", "edward"],
        "julia": ["julia"],
        "meifa": ["meifa puzi", "meifa_puzi"],
        "judy": ["judy"],
        "annie": ["anastasia"],
        "alisa": ["alisa"],
        "vip": ["v.t.", "victoria terraforming"],
        "stella": ["stella bonnaro", "stella_bonnaro"],
        "coffee": ["coffee"],
        "katrina": ["katrina solensan", "katrina_solensan"]
    },

    "spy_x_family": {
        "yor": ["yor forger", "yor_forger", "thorn princess"],
        "anya": ["anya forger", "anya_forger"],
        "sylvia": ["sylvia sherwood", "sylvia_sherwood"],
        "fiona": ["fiona frost", "fiona_frost"],
        "becky": ["becky blackbell", "becky_blackbell"],
        "sharon": ["sharon", "shop_keeper"],
        "melinda": ["melinda desmond", "melinda_desmond"],
        "camilla": ["camilla", "shopkeeper_sister"],
        "karen": ["karen gloomy", "karen_gloomy"],
        "dominic": ["dominic", "handler"],
        "martha": ["martha", "landlady"]
    },

    "one_punch_man": {
        "fubuki": ["fubuki", "blizzard", "hellish blizzard"],
        "tatsumaki": ["tatsumaki", "tornado", "tornado of terror"],
        "psykos": ["psykos"],
        "suiko": ["suiko"],
        "lin_lin": ["lin lin"],
        "lily": ["lily of the three section staff", "lily"],
        "do_s": ["do-s", "monster princess"],
        "mosquito_girl": ["mosquito girl"],
        "mizuki": ["captain mizuki", "mizuki"],
        "shadow_ring": ["shadow ring"],
        "zenko": ["zenko", "metal bat's sister"],
        "madame_shibabawa": ["madame shibabawa"],
        "goddess_glasses": ["goddess glasses"],
        "swim": ["swim"],
        "pai": ["pai"]
    },

    "league_of_legends": {
        "ahri": ["ahri"],
        "lux": ["lux", "luxanna crownguard"],
        "jinx": ["jinx"],
        "vi": ["vi"],
        "caitlyn": ["caitlyn"],
        "leona": ["leona"],
        "diana": ["diana"],
        "ashe": ["ashe"],
        "katarina": ["katarina"],
        "miss_fortune": ["miss fortune", "sarah fortune"],
        "akali": ["akali"],
        "anivia": ["anivia"],
        "annie": ["annie"],
        "bel_veth": ["bel'veth", "belveth"],
        "briar": ["briar"],
        "cassiopeia": ["cassiopeia"],
        "elise": ["elise"],
        "evelynn": ["evelynn"],
        "fiora": ["fiora"],
        "gwen": ["gwen"],
        "illaoi": ["illaoi"],
        "irelia": ["irelia"],
        "janna": ["janna"],
        "kai_sa": ["kai'sa", "kaisa"],
        "kalista": ["kalista"],
        "karma": ["karma"],
        "kindred": ["kindred"],
        "leblanc": ["leblanc"],
        "lillia": ["lillia"],
        "lissandra": ["lissandra"],
        "morgana": ["morgana"],
        "nami": ["nami"],
        "neeko": ["neeko"],
        "nidalee": ["nidalee"],
        "nilah": ["nilah"],
        "orianna": ["orianna"],
        "poppy": ["poppy"],
        "qiyana": ["qiyana"],
        "rell": ["rell"],
        "riven": ["riven"],
        "samira": ["samira"],
        "senna": ["senna"],
        "seraphine": ["seraphine"],
        "sejuani": ["sejuani"],
        "senna": ["senna"],
        "shyvana": ["shyvana"],
        "sivir": ["sivir"],
        "sona": ["sona"],
        "soraka": ["soraka"],
        "syndra": ["syndra"],
        "taliyah": ["taliyah"],
        "tristana": ["tristana"],
        "vayne": ["vayne"],
        "vex": ["vex"],
        "xayah": ["xayah"],
        "yuumi": ["yuumi"],
        "zeri": ["zeri"],
        "zoe": ["zoe"],
        "zyra": ["zyra"]
    },

    "hunter_x_hunter": {
        "biscuit": ["biscuit krueger", "bisky"],
        "palm": ["palm siberia"],
        "machi": ["machi"],
        "shizuku": ["shizuku"],
        "canary": ["canary"],
        "neferpitou": ["neferpitou", "pitou"],
        "komugi": ["komugi"],
        "pakunoda": ["pakunoda"],
        "melody": ["melody", "senritsu"],
        "zazan": ["zazan"],
        "eliza": ["eliza"],
        "amane": ["amane"],
        "tsubone": ["tsubone"],
        "kalluto": ["kalluto zoldyck", "kalluto_zoldyck"],
        "kikyo": ["kikyo zoldyck", "kikyo_zoldyck"],
        "alluka": ["alluka zoldyck", "alluka_zoldyck"],
        "cheadle": ["cheadle yorkshire", "cheadle_yorkshire"],
        "menchi": ["menchi"],
        "ponzu": ["ponzu"]
    },

    "fullmetal_alchemist": {
        "winry": ["winry rockbell", "winry_rockbell"],
        "riza": ["riza hawkeye", "riza_hawkeye"],
        "olivier": ["olivier armstrong", "olivier_armstrong"],
        "izumi": ["izumi curtis", "izumi_curtis"],
        "mei": ["mei chang", "mei_chang"],
        "maria": ["maria ross", "maria_ross"],
        "gracia": ["gracia hughes", "gracia_hughes"],
        "elicia": ["elicia hughes", "elicia_hughes"],
        "lan_fan": ["lan fan", "lan_fan"],
        "paninya": ["paninya"],
        "sheska": ["sheska", "sciezka"],
        "rose": ["rose thomas", "rose_thomas"],
        "catherine": ["catherine elle armstrong", "catherine_armstrong"],
        "martel": ["martel"],
        "trisha": ["trisha elric", "trisha_elric"],
        "pinako": ["pinako rockbell", "pinako_rockbell"],
        "lust": ["lust"],
        "dante": ["dante"],
        "clara": ["clara", "psiren"]
    },

    "my_hero_academia": {
        "uraraka": ["ochaco uraraka", "ochaco_uraraka"],
        "asui": ["tsuyu asui", "tsuyu_asui", "froppy"],
        "yaoyorozu": ["momo yaoyorozu", "momo_yaoyorozu"],
        "jirou": ["kyoka jirou", "kyoka_jirou"],
        "hagakure": ["toru hagakure", "toru_hagakure"],
        "ashido": ["mina ashido", "mina_ashido", "pinky"],
        "mount_lady": ["mount lady", "yu takeyama"],
        "midnight": ["midnight", "nemuri kayama"],
        "mirko": ["mirko", "rumi usagiyama"],
        "ryuku": ["ryuku", "ryuko tatsuma"],
        "nejire": ["nejire hado", "nejire_hado"],
        "mandalay": ["mandalay", "shino sosaki"],
        "pixie_bob": ["pixie-bob", "ryuko tsuchikawa"],
        "ragdoll": ["ragdoll", "tomoko shiretoko"],
        "kendo": ["itsuka kendo", "itsuka_kendo"],
        "tsunotori": ["pony tsunotori", "pony_tsunotori"],
        "komori": ["kinoko komori", "kinoko_komori"],
        "kodai": ["yui kodai", "yui_kodai"],
        "yanagi": ["reiko yanagi", "reiko_yanagi"],
        "tokage": ["setsuna tokage", "setsuna_tokage"],
        "melissa": ["melissa shield", "melissa_shield"],
        "inko": ["inko midoriya", "inko_midoriya"],
        "fuyumi": ["fuyumi todoroki", "fuyumi_todoroki"],
        "eri": ["eri"],
        "nana": ["nana shimura", "nana_shimura"],
        "toga": ["himiko toga", "himiko_toga"]
    },

    "jojos_bizarre_adventure": {
        "jolyne": ["jolyne cujoh", "jolyne_cujoh"],
        "lisa_lisa": ["lisa lisa", "lisa_lisa"],
        "erina": ["erina pendleton", "erina_pendleton"],
        "trish": ["trish una", "trish_una"],
        "suzi_q": ["suzi q", "suzi_q"],
        "holly": ["holly kujo", "holly_kujo", "seiko"],
        "yukako": ["yukako yamagishi", "yukako_yamagishi"],
        "reimi": ["reimi sugimoto", "reimi_sugimoto"],
        "hot_pants": ["hot pants", "hot_pants"],
        "lucy": ["lucy steel", "lucy_steel"],
        "yasuho": ["yasuho hirose", "yasuho_hirose"],
        "hermes": ["hermes costello", "hermes_costello"],
        "foo_fighters": ["foo fighters", "f.f.", "ff"],
        "ermes": ["ermes costello", "ermes_costello"],
        "gwess": ["gwess"],
        "mariah": ["mariah"],
        "midler": ["midler", "rose"],
        "anne": ["anne"],
        "tomoko": ["tomoko higashikata", "tomoko_higashikata"]
    },

    "pokemon": {
        "misty": ["misty", "kasumi"],
        "may": ["may", "haruka"],
        "dawn": ["dawn", "hikari"],
        "serena": ["serena"],
        "iris": ["iris"],
        "lillie": ["lillie"],
        "cynthia": ["cynthia", "shirona"],
        "diantha": ["diantha"],
        "lusamine": ["lusamine"],
        "sabrina": ["sabrina"],
        "erika": ["erika"],
        "whitney": ["whitney"],
        "jasmine": ["jasmine"],
        "clair": ["clair"],
        "flannery": ["flannery"],
        "winona": ["winona"],
        "roxanne": ["roxanne"],
        "gardenia": ["gardenia"],
        "candice": ["candice"],
        "fantina": ["fantina"],
        "elesa": ["elesa"],
        "skyla": ["skyla"],
        "korrina": ["korrina"],
        "valerie": ["valerie"],
        "olympia": ["olympia"],
        "mallow": ["mallow"],
        "lana": ["lana"],
        "nessa": ["nessa"],
        "marnie": ["marnie"],
        "sonia": ["sonia"],
        "professor_juniper": ["professor juniper", "professor_juniper"],
        "nurse_joy": ["nurse joy", "joy"],
        "officer_jenny": ["officer jenny", "jenny"],
        "jessie": ["jessie", "musashi"],
        "bonnie": ["bonnie", "eureka"],
        "rosa": ["rosa"]
    },

    "hatsune_miku": {
        "miku": ["hatsune miku", "hatsune_miku", "miku", "initial miku", "initial_miku", "miku_(vocaloid)", "miku_(project_diva)"],
        "meiko": ["meiko", "meiko_(vocaloid)", "meiko_(project_diva)"],
        "rin": ["kagamine rin", "kagamine_rin", "rin", "rin_(vocaloid)", "rin_(project_diva)"],
        "luka": ["megurine luka", "megurine_luka", "luka", "luka_(vocaloid)", "luka_(project_diva)"],
        "gumi": ["gumi", "megpoid", "gumi_(vocaloid)", "gumi_(project_diva)"],
        "teto": ["kasane teto", "kasane_teto", "teto", "teto_(utau)"],
        "neru": ["akita neru", "akita_neru", "neru", "neru_(derivative)"],
        "haku": ["yowane haku", "yowane_haku", "haku", "haku_(derivative)"],
        "una": ["otomachi una", "otomachi_una", "una", "una_(vocaloid)"],
        "ia": ["ia", "ia_(vocaloid)", "aria on the planetes"],
        "cul": ["cul", "cul_(vocaloid)"],
        "lily": ["lily", "lily_(vocaloid)"],
        "miki": ["sf-a2 miki", "sf_a2_miki", "miki", "miki_(vocaloid)"],
        "yukari": ["yuzuki yukari", "yuzuki_yukari", "yukari", "yukari_(vocaloid)"]
    },
}

CHARACTER_DESCRIPTIONS = {
    "one_piece": {
        "nami": ("Nami", "The Cat Burglar and Navigator of the Straw Hat Pirates"),
        "robin": ("Nico Robin", "The Devil Child and Archaeologist of the Straw Hat Pirates"),
        "boa_hancock": ("Boa Hancock", "The Pirate Empress and Captain of the Kuja Pirates"),
        "vivi": ("Nefertari Vivi", "Princess of Alabasta and Former Straw Hat Companion"),
        "vinsmoke_reiju": ("Vinsmoke Reiju", "The Poison Pink Princess of the Germa 66"),
        "charlotte_linlin": ("Charlotte Linlin", "Big Mom, Captain of the Big Mom Pirates"),
        "shirahoshi": ("Shirahoshi", "The Ancient Weapon Poseidon and Mermaid Princess"),
        "kouzuki_hiyori": ("Kozuki Hiyori", "Daughter of the Daimyo and Heir to Wano"),
        "perona": ("Perona", "The Ghost Princess and Former Member of Thriller Bark"),
        "monet": ("Monet", "The Snow Woman and Caesar's Secretary"),
        "wanda": ("Wanda", "Warrior of the Mink Tribe"),
        "nico_olvia": ("Nico Olvia", "The Revolutionary Scholar and Robin's Mother"),
        "nojiko": ("Nojiko", "Nami's Adoptive Sister and Bell-mère's Daughter"),
        "charlotte_pudding": ("Charlotte Pudding", "The 35th Daughter of the Charlotte Family"),
        "stussy": ("Stussy", "The Queen of the Pleasure District and CP0 Agent"),
        "tashigi": ("Tashigi", "Marine Captain and Swordswoman"),
        "hina": ("Hina", "The Black Cage Marine Officer"),
        "rebecca": ("Rebecca", "The Undefeated Gladiator and Princess of Dressrosa"),
        "carrot": ("Carrot", "The Moon Lion Warrior of the Mink Tribe"),
        "bonney": ("Jewelry Bonney", "The Big Eater and Captain of the Bonney Pirates"),
        "baby_5": ("Baby 5", "The Living Weapon and Former Donquixote Pirate"),
        "kuina": ("Kuina", "The Legendary Swordswoman and Zoro's Childhood Friend"),
        "charlotte_smoothie": ("Charlotte Smoothie", "Sweet Commander of the Big Mom Pirates"),
        "catarina_devon": ("Catarina Devon", "The Crescent Moon Hunter of the Blackbeard Pirates"),
        "charlotte_flampe": ("Charlotte Flampe", "Leader of the Special Forces and Charlotte Family Member"),
        "kouzuki_toki": ("Kozuki Toki", "The Time Traveler and Wife of Oden"),
        "alvida": ("Alvida", "Iron Mace Alvida and Former Captain"),
        "kikunojo": ("Kikunojo", "The Lingering Snow of the Nine Red Scabbards"),
        "vegapunk_lilith": ("Vegapunk Lilith", "Evil Satellite of Dr. Vegapunk"),
        "kaya": ("Kaya", "The Kind-Hearted Heiress of Syrup Village"),
        "isuka": ("Isuka", "The Nailing Marine and Former Instructor"),
        "vegapunk_atlas": ("Vegapunk Atlas", "Combat Satellite of Dr. Vegapunk"),
        "vegapunk_york": ("Vegapunk York", "Analysis Satellite of Dr. Vegapunk"),
    },

    "naruto": {
        "tsunade": ("Tsunade Senju", "The Fifth Hokage and Legendary Sannin"),
        "sakura": ("Sakura Haruno", "The Strongest Medical Ninja and Student of Tsunade"),
        "hinata": ("Hinata Hyuga", "The Byakugan Princess and Wife of Naruto"),
        "tenten": ("Tenten", "The Weapons Mistress of Team Guy"),
        "temari": ("Temari", "The Wind Mistress and Ambassador of Sunagakure"),
        "kushina": ("Kushina Uzumaki", "The Red Hot-Blooded Habanero and Naruto's Mother"),
        "sarada": ("Sarada Uchiha", "Daughter of Sasuke and Future Hokage Aspirant"),
        "himawari": ("Himawari Uzumaki", "Daughter of Naruto with the Byakugan"),
        "ino": ("Ino Yamanaka", "Leader of the Sensory Division and Medical Ninja"),
        "kurenai": ("Kurenai Yuhi", "The Genjutsu Mistress and Team 8 Leader"),
        "anko": ("Anko Mitarashi", "The Snake Mistress and Former Student of Orochimaru"),
        "shizune": ("Shizune", "First Apprentice of Tsunade and Chief Medical Ninja"),
        "karin": ("Karin Uzumaki", "The Sensory Ninja and Former Member of Taka"),
        "konan": ("Konan", "The Angel of Amegakure and Member of the Akatsuki"),
        "mei": ("Mei Terumi", "The Fifth Mizukage with Dual Kekkei Genkai"),
        "samui": ("Samui", "The Cool-Headed Kunoichi of Kumogakure"),
        "karui": ("Karui", "The Fierce Warrior of Kumogakure"),
        "mabui": ("Mabui", "The Raikage's Assistant and Transport Specialist"),
        "yugao": ("Yugao Uzuki", "ANBU Captain and Master Swordswoman"),
        "tsume": ("Tsume Inuzuka", "Matriarch of the Inuzuka Clan"),
        "hana": ("Hana Inuzuka", "The Veterinary Ninja and Sister of Kiba"),
        "natsu": ("Natsu Hyuga", "Caretaker of the Hyuga Clan"),
        "yakumo": ("Yakumo Kurama", "Heiress of the Kurama Clan"),
        "tsunami": ("Tsunami", "Kind-Hearted Civilian of the Land of Waves"),
        "ayame": ("Ayame", "Daughter of Teuchi and Ramen Chef"),
        "yugito": ("Yugito Nii", "The Two-Tails Jinchūriki of Kumogakure"),
        "fuu": ("Fuu", "The Seven-Tails Jinchūriki of Takigakure"),
        "hokuto": ("Hokuto", "Star Village Kunoichi"),
        "hanabi": ("Hanabi Hyuga", "Leader of the Hyuga Clan"),
        "moegi": ("Moegi", "Member of Team Ebisu and Wood Release User"),
        "sumire": ("Sumire Kakei", "Class Rep and Former Root Member"),
        "chocho": ("Chocho Akimichi", "The Butterfly Ninja of the New Generation"),
        "mirai": ("Mirai Sarutobi", "Daughter of Asuma and Kurenai"),
        "wasabi": ("Wasabi Izuno", "Cat-Like Ninja of the New Generation"),
        "namida": ("Namida Suzumeno", "Sound-Based Ninja of the New Generation")
    },

    "fairy_tail": {
        "lucy": ("Lucy Heartfilia", "Celestial Spirit Mage and Novel Writer"),
        "erza": ("Erza Scarlet", "Titania, Queen of the Fairies and S-Class Requip Mage"),
        "wendy": ("Wendy Marvell", "The Sky Dragon Slayer and Healing Specialist"),
        "juvia": ("Juvia Lockser", "The Rain Woman and Water Magic Master"),
        "levy": ("Levy McGarden", "Solid Script Mage and Leader of Shadow Gear"),
        "mirajane": ("Mirajane Strauss", "The Demon Take-Over Mage and Former S-Class"),
        "lisanna": ("Lisanna Strauss", "Animal Soul Take-Over Mage and Mirajane's Sister"),
        "cana": ("Cana Alberona", "Card Magic Expert and Gildarts' Daughter"),
        "evergreen": ("Evergreen", "The Fairy Queen of the Thunder Legion"),
        "bisca": ("Bisca Connell", "The Gunslinger Mage and Alzack's Wife"),
        "laki": ("Laki Olietta", "Wood-Make Magic User"),
        "kinana": ("Kinana", "Former Snake Cubellios and Guild Barmaid"),
        "mavis": ("Mavis Vermillion", "First Guild Master and Fairy Tactician"),
        "meredy": ("Meredy", "Sensory Link Mage of Crime Sorcière"),
        "ultear": ("Ultear Milkovich", "Arc of Time Master and Founder of Crime Sorcière"),
        "yukino": ("Yukino Agria", "Celestial Spirit Mage of Sabertooth"),
        "minerva": ("Minerva Orlando", "Territory Magic User and Lady of Sabertooth"),
        "kagura": ("Kagura Mikazuchi", "Gravity Magic Swordswoman of Mermaid Heel"),
        "milliana": ("Milliana", "Cat-Like Binding Magic User of Mermaid Heel"),
        "flare": ("Flare Corona", "Crimson Hair Mage of Raven Tail"),
        "jenny": ("Jenny Realight", "Take-Over Mage and Blue Pegasus Model"),
        "sherry": ("Sherry Blendy", "Doll Attack Mage and Ren's Wife"),
        "chelia": ("Chelia Blendy", "Former Sky God Slayer and Wendy's Friend"),
        "sorano": ("Sorano", "Angel of the Oracion Seis and Yukino's Sister"),
        "brandish": ("Brandish μ", "Mass Manipulation Mage of the Spriggan 12"),
        "dimaria": ("Dimaria Yesta", "Time God of the Spriggan 12"),
        "irene": ("Irene Belserion", "Scarlet Despair and Mother of Dragon Slaying Magic"),
        "hisui": ("Hisui E. Fiore", "Princess of Fiore and Jade Dragon")
    },

    "dragon_ball": {
        "bulma": ("Bulma Briefs", "Scientific Genius and Founder of Capsule Corporation"),
        "chi_chi": ("Chi-Chi", "The Ox Princess and Wife of Goku"),
        "videl": ("Videl Satan", "Crime Fighter and Wife of Gohan"),
        "pan": ("Pan", "Quarter-Saiyan Daughter of Gohan and Videl"),
        "android_18": ("Android 18", "Former Enemy turned Z-Fighter and Krillin's Wife"),
        "bulla": ("Bulla", "Half-Saiyan Daughter of Vegeta and Bulma"),
        "launch": ("Launch", "Jekyll and Hyde Personality Fighter"),
        "marron": ("Marron", "Daughter of Krillin and Android 18"),
        "mai": ("Mai", "Former Enemy turned Time Patrol Member"),
        "ranfan": ("Ranfan", "World Tournament Fighter"),
        "vados": ("Vados", "Angel Attendant of Universe 6"),
        "caulifla": ("Caulifla", "Universe 6 Saiyan Prodigy"),
        "kale": ("Kale", "Legendary Super Saiyan of Universe 6"),
        "ribrianne": ("Ribrianne", "Love Warrior of Universe 2"),
        "oceanus": ("Oceanus Shenron", "Shadow Dragon of Water and Wind"),
        "gine": ("Gine", "Mother of Goku and Former Saiyan Warrior"),
        "fasha": ("Fasha", "Member of Bardock's Elite Squad"),
        "zangya": ("Zangya", "Warrior of the Galaxy Soldiers"),
        "towa": ("Towa", "Dark Scientist of the Demon Realm"),
        "supreme_kai_of_time": ("Supreme Kai of Time", "Guardian of the Time Nest"),
        "arale": ("Arale Norimaki", "Android Girl with Superhuman Strength")
    },

    "attack_on_titan": {
        "mikasa": ("Mikasa Ackerman", "The Last Asian and Elite Survey Corps Soldier"),
        "annie": ("Annie Leonhart", "The Female Titan and Former Military Police"),
        "historia": ("Historia Reiss", "The True Queen of the Walls"),
        "sasha": ("Sasha Braus", "The Potato Girl and Expert Marksman"),
        "hange": ("Hange Zoë", "14th Commander of the Survey Corps and Titan Researcher"),
        "ymir": ("Ymir", "The Jaw Titan and Historia's Protector"),
        "pieck": ("Pieck Finger", "The Cart Titan and Marley's Strategist"),
        "gabi": ("Gabi Braun", "Warrior Candidate and Reiner's Cousin"),
        "frieda": ("Frieda Reiss", "Former Holder of the Founding Titan"),
        "carla": ("Carla Yeager", "Eren's Mother and Victim of the Fall"),
        "dina": ("Dina Fritz", "The Smiling Titan and Grisha's First Wife"),
        "petra": ("Petra Ral", "Elite Member of the Levi Squad"),
        "rico": ("Rico Brzenska", "Elite Garrison Squad Leader"),
        "yelena": ("Yelena", "Zeke's Devoted Follower and Anti-Marleyan"),
        "kiyomi": ("Kiyomi Azumabito", "Ambassador of Hizuru"),
        "louise": ("Louise", "Young Soldier Inspired by Mikasa"),
        "nifa": ("Nifa", "Member of Squad Hange"),
        "lynne": ("Lynne", "Veteran Survey Corps Member"),
        "ilse": ("Ilse Langnar", "Survey Corps Researcher"),
        "nanaba": ("Nanaba", "Veteran Survey Corps Member and Squad Leader")
    },

    "demon_slayer": {
        "nezuko": ("Nezuko Kamado", "Demon Sister of Tanjiro with Unique Blood Art"),
        "kanao": ("Kanao Tsuyuri", "Flower Breathing User and Shinobu's Protégé"),
        "shinobu": ("Shinobu Kocho", "Insect Hashira and Master of Poison"),
        "kanae": ("Kanae Kocho", "Former Flower Hashira and Shinobu's Sister"),
        "mitsuri": ("Mitsuri Kanroji", "Love Hashira with Unique Muscle Composition"),
        "daki": ("Daki", "Upper Rank Six Demon and Oiran"),
        "tamayo": ("Tamayo", "Doctor Demon Who Defied Muzan"),
        "makio": ("Makio", "Uzui's Wife and Kunoichi"),
        "suma": ("Suma", "Uzui's Wife and Shinobi"),
        "hinatsuru": ("Hinatsuru", "Uzui's Wife and Ninja"),
        "aoi": ("Aoi Kanzaki", "Medical Support at the Butterfly Estate"),
        "kiyo": ("Kiyo Terauchi", "Butterfly Estate Medical Staff"),
        "sumi": ("Sumi Nakahara", "Butterfly Estate Medical Staff"),
        "naho": ("Naho Takada", "Butterfly Estate Medical Staff"),
        "goto": ("Goto", "Kakushi Corps Leader"),
        "amane": ("Amane", "Ubuyashiki Household Staff"),
        "mukago": ("Mukago", "Spider Demon of Mt. Natagumo"),
        "ruka": ("Ruka", "Spider Demon Family Member"),
        "hinaki": ("Hinaki Ubuyashiki", "Daughter of Kagaya Ubuyashiki"),
        "nichika": ("Nichika Ubuyashiki", "Daughter of the Demon Slayer Leader"),
        "kuina": ("Kuina Ubuyashiki", "Youngest Daughter of Master Ubuyashiki")
    },

    "jujutsu_kaisen": {
        "nobara": ("Nobara Kugisaki", "First-Year Sorcerer and Master of Straw Doll Technique"),
        "maki": ("Maki Zenin", "Cursed Tools Expert and Former Zenin Clan Member"),
        "mei_mei": ("Mei Mei", "Grade 1 Sorcerer and Money-Motivated Bird Strike User"),
        "miwa": ("Kasumi Miwa", "Kyoto Student and New Shadow Style Swordsman"),
        "momo": ("Momo Nishimiya", "Broom-Flying Kyoto Second-Year"),
        "mai": ("Mai Zenin", "Maki's Twin with Construction Technique"),
        "yuki": ("Yuki Tsukumo", "Special Grade Sorcerer and Researcher"),
        "rika": ("Rika Orimoto", "Yuta's Cursed Spirit Companion"),
        "utahime": ("Utahime Iori", "Kyoto Teacher and Barrier Technique User"),
        "tsumiki": ("Tsumiki Fushiguro", "Megumi's Cursed Sister"),
        "manami": ("Manami Suda", "Curse Victim and Mahito's Target"),
        "saori": ("Saori Rokujo", "Nobara's Middle School Friend"),
        "shoko": ("Shoko Ieiri", "Jujutsu Tech's Doctor and Reverse Cursed Technique User"),
        "mimiko": ("Mimiko Hasaba", "Twin Curse User"),
        "nanako": ("Nanako Hasaba", "Twin Curse User")
    },

    "cowboy_bebop": {
        "faye": ("Faye Valentine", "Amnesiac Bounty Hunter with a Massive Debt"),
        "ed": ("Edward Wong", "Eccentric Hacker Prodigy"),
        "julia": ("Julia", "Mysterious Woman from Spike's Past"),
        "meifa": ("Meifa Puzi", "Feng Shui Master's Daughter"),
        "judy": ("Judy", "Television Show Host"),
        "annie": ("Anastasia", "Bar Owner and Spike's Friend"),
        "alisa": ("Alisa", "Jet's Former Love Interest"),
        "vip": ("V.T.", "Space Trucker and Racing Queen"),
        "stella": ("Stella Bonnaro", "Saxophone Player's Daughter"),
        "coffee": ("Coffee", "Owner of the Mexican Restaurant"),
        "katrina": ("Katrina Solensan", "Assassin turned Environmental Activist")
    },

    "spy_x_family": {
        "yor": ("Yor Forger", "The Thorn Princess and Secret Assassin"),
        "anya": ("Anya Forger", "Telepathic Child Spy-in-Training"),
        "sylvia": ("Sylvia Sherwood", "Handler of WISE and Operation Strix Manager"),
        "fiona": ("Fiona Frost", "Elite WISE Agent and Twilight's Former Partner"),
        "becky": ("Becky Blackbell", "Anya's Best Friend and Rich Heiress"),
        "sharon": ("Sharon", "Kind Shop Owner and Information Broker"),
        "melinda": ("Melinda Desmond", "Donovan Desmond's Reserved Wife"),
        "camilla": ("Camilla", "Sharon's Sister and Shop Assistant"),
        "karen": ("Karen Gloomy", "Photography Club Member"),
        "dominic": ("Dominic", "Garden's Handler"),
        "martha": ("Martha", "The Forger Family's Landlady")
    },

    "one_punch_man": {
        "fubuki": ("Fubuki", "The Hellish Blizzard and B-Class Hero"),
        "tatsumaki": ("Tatsumaki", "The Terrible Tornado and S-Class Hero"),
        "psykos": ("Psykos", "Leader of the Monster Association"),
        "suiko": ("Suiko", "Suiryu's Sister and Martial Artist"),
        "lin_lin": ("Lin Lin", "A-Class Hero and Super Fight Participant"),
        "lily": ("Lily", "The Three-Section Staff and Fubuki Group Member"),
        "do_s": ("Do-S", "The Monster Princess and Dominatrix"),
        "mosquito_girl": ("Mosquito Girl", "Blood-Drinking Monster"),
        "mizuki": ("Captain Mizuki", "Track and Field Hero"),
        "shadow_ring": ("Shadow Ring", "A-Class Ninja Hero"),
        "zenko": ("Zenko", "Metal Bat's Little Sister"),
        "madame_shibabawa": ("Madame Shibabawa", "The Great Fortune Teller"),
        "goddess_glasses": ("Goddess Glasses", "Support Hero"),
        "swim": ("Swim", "Tank Top Hero Group Member"),
        "pai": ("Pai", "Tank Top Hero Group Member")
    },

    "league_of_legends": {
        "ahri": ("Ahri", "The Nine-Tailed Fox and Vastayan Charmer"),
        "lux": ("Luxanna Crownguard", "The Lady of Luminosity"),
        "jinx": ("Jinx", "The Loose Cannon of Zaun"),
        "vi": ("Vi", "The Piltover Enforcer"),
        "caitlyn": ("Caitlyn", "The Sheriff of Piltover"),
        "leona": ("Leona", "The Radiant Dawn of Mount Targon"),
        "diana": ("Diana", "The Scorn of the Moon"),
        "ashe": ("Ashe", "The Frost Archer and Queen of Freljord"),
        "katarina": ("Katarina", "The Sinister Blade of Noxus"),
        "miss_fortune": ("Sarah Fortune", "The Bounty Hunter of Bilgewater"),
        "akali": ("Akali", "The Rogue Assassin"),
        "anivia": ("Anivia", "The Cryophoenix"),
        "annie": ("Annie", "The Dark Child"),
        "bel_veth": ("Bel'Veth", "The Empress of the Void"),
        "briar": ("Briar", "The Hungry Hydra"),
        "cassiopeia": ("Cassiopeia", "The Serpent's Embrace"),
        "elise": ("Elise", "The Spider Queen"),
        "evelynn": ("Evelynn", "Agony's Embrace"),
        "fiora": ("Fiora", "The Grand Duelist"),
        "gwen": ("Gwen", "The Hallowed Seamstress"),
        "illaoi": ("Illaoi", "The Kraken Priestess"),
        "irelia": ("Irelia", "The Blade Dancer"),
        "janna": ("Janna", "The Storm's Fury"),
        "kai_sa": ("Kai'Sa", "Daughter of the Void"),
        "kalista": ("Kalista", "The Spear of Vengeance"),
        "karma": ("Karma", "The Enlightened One"),
        "kindred": ("Kindred", "The Eternal Hunters"),
        "leblanc": ("LeBlanc", "The Deceiver"),
        "lillia": ("Lillia", "The Bashful Bloom"),
        "lissandra": ("Lissandra", "The Ice Witch"),
        "morgana": ("Morgana", "The Fallen"),
        "nami": ("Nami", "The Tidecaller"),
        "neeko": ("Neeko", "The Curious Chameleon"),
        "nidalee": ("Nidalee", "The Bestial Huntress"),
        "nilah": ("Nilah", "The Joy Unbound"),
        "orianna": ("Orianna", "The Lady of Clockwork"),
        "poppy": ("Poppy", "Keeper of the Hammer"),
        "qiyana": ("Qiyana", "Empress of the Elements"),
        "rell": ("Rell", "The Iron Maiden"),
        "riven": ("Riven", "The Exile"),
        "samira": ("Samira", "The Desert Rose"),
        "senna": ("Senna", "The Redeemer"),
        "seraphine": ("Seraphine", "The Starry-Eyed Songstress"),
        "sejuani": ("Sejuani", "Fury of the North"),
        "shyvana": ("Shyvana", "The Half-Dragon"),
        "sivir": ("Sivir", "The Battle Mistress"),
        "sona": ("Sona", "Maven of the Strings"),
        "soraka": ("Soraka", "The Starchild"),
        "syndra": ("Syndra", "The Dark Sovereign"),
        "taliyah": ("Taliyah", "The Stoneweaver"),
        "tristana": ("Tristana", "The Yordle Gunner"),
        "vayne": ("Vayne", "The Night Hunter"),
        "vex": ("Vex", "The Gloomist"),
        "xayah": ("Xayah", "The Rebel"),
        "yuumi": ("Yuumi", "The Magical Cat"),
        "zeri": ("Zeri", "The Spark of Zaun"),
        "zoe": ("Zoe", "The Aspect of Twilight"),
        "zyra": ("Zyra", "Rise of the Thorns")
    },

    "hunter_x_hunter": {
        "biscuit": ("Biscuit Krueger", "Master Nen Teacher and Precious Stone Hunter"),
        "palm": ("Palm Siberia", "Chimera Ant Soldier and Clairvoyant"),
        "machi": ("Machi", "Spider #3 and Phantom Troupe's Medic"),
        "shizuku": ("Shizuku", "Spider #8 and Vacuum User"),
        "canary": ("Canary", "Zoldyck Family Butler and Killua's Ally"),
        "neferpitou": ("Neferpitou", "Royal Guard and Doctor Blythe User"),
        "komugi": ("Komugi", "Gungi Champion and Meruem's Teacher"),
        "pakunoda": ("Pakunoda", "Spider #9 and Memory Reader"),
        "melody": ("Melody", "Music Hunter with Enhanced Hearing"),
        "zazan": ("Zazan", "Chimera Ant Queen of Meteor City"),
        "eliza": ("Eliza", "Squala's Girlfriend and Victim"),
        "amane": ("Amane", "Zoldyck Butler and Canary's Senior"),
        "tsubone": ("Tsubone", "Zoldyck Head Butler"),
        "kalluto": ("Kalluto Zoldyck", "Youngest Zoldyck and Spider #4"),
        "kikyo": ("Kikyo Zoldyck", "Matriarch of the Zoldyck Family"),
        "alluka": ("Alluka Zoldyck", "Killua's Sister and Wish Granter"),
        "cheadle": ("Cheadle Yorkshire", "Zodiac Dog and Medical Hunter"),
        "menchi": ("Menchi", "Gourmet Hunter and Examiner"),
        "ponzu": ("Ponzu", "Bee User and Hunter Examinee")
    },

    "fullmetal_alchemist": {
        "winry": ("Winry Rockbell", "Automail Engineer and Edward's Wife"),
        "riza": ("Riza Hawkeye", "The Hawk's Eye and Mustang's Lieutenant"),
        "olivier": ("Olivier Armstrong", "The Northern Wall of Briggs"),
        "izumi": ("Izumi Curtis", "The Alchemist Teacher"),
        "mei": ("Mei Chang", "Alkahestry Princess of Xing"),
        "maria": ("Maria Ross", "Framed Lieutenant and Loyal Soldier"),
        "gracia": ("Gracia Hughes", "Maes Hughes' Widow"),
        "elicia": ("Elicia Hughes", "Maes Hughes' Daughter"),
        "lan_fan": ("Lan Fan", "Ling's Personal Guard and Assassin"),
        "paninya": ("Paninya", "Rush Valley's Automail Thief"),
        "sheska": ("Sheska", "Photographic Memory Librarian"),
        "rose": ("Rose Thomas", "Reole's Religious Follower"),
        "catherine": ("Catherine Armstrong", "Strong Arm's Sister"),
        "martel": ("Martel", "Chimera Soldier of Devil's Nest"),
        "trisha": ("Trisha Elric", "Loving Mother of Edward and Alphonse"),
        "pinako": ("Pinako Rockbell", "Legendary Automail Engineer"),
        "lust": ("Lust", "The Ultimate Lance Homunculus"),
        "dante": ("Dante", "Ancient Alchemist and Main Antagonist"),
        "clara": ("Clara", "The Phantom Thief Psiren")
    },

    "my_hero_academia": {
        "uraraka": ("Ochaco Uraraka", "Zero Gravity Hero: Uravity"),
        "asui": ("Tsuyu Asui", "Rainy Season Hero: Froppy"),
        "yaoyorozu": ("Momo Yaoyorozu", "Everything Hero: Creati"),
        "jirou": ("Kyoka Jirou", "Hearing Hero: Earphone Jack"),
        "hagakure": ("Toru Hagakure", "Stealth Hero: Invisible Girl"),
        "ashido": ("Mina Ashido", "Pinky: The Acid Hero"),
        "mount_lady": ("Yu Takeyama", "Giant Hero: Mount Lady"),
        "midnight": ("Nemuri Kayama", "R-Rated Hero: Midnight"),
        "mirko": ("Rumi Usagiyama", "Rabbit Hero: Mirko"),
        "ryuku": ("Ryuko Tatsuma", "Dragon Hero: Ryukyu"),
        "nejire": ("Nejire Hado", "Wave Motion Hero: Nejire-chan"),
        "mandalay": ("Shino Sosaki", "Wild Wild Pussycats: Mandalay"),
        "pixie_bob": ("Ryuko Tsuchikawa", "Wild Wild Pussycats: Pixie-Bob"),
        "ragdoll": ("Tomoko Shiretoko", "Wild Wild Pussycats: Ragdoll"),
        "kendo": ("Itsuka Kendo", "Battle Fist of Class 1-B"),
        "tsunotori": ("Pony Tsunotori", "Class 1-B's Exchange Student"),
        "komori": ("Kinoko Komori", "Mushroom Girl of Class 1-B"),
        "kodai": ("Yui Kodai", "Size Master of Class 1-B"),
        "yanagi": ("Reiko Yanagi", "Poltergeist of Class 1-B"),
        "tokage": ("Setsuna Tokage", "Lizard Hero: Lizardy"),
        "melissa": ("Melissa Shield", "Support Item Developer"),
        "inko": ("Inko Midoriya", "Deku's Caring Mother"),
        "fuyumi": ("Fuyumi Todoroki", "Shoto's Supportive Sister"),
        "eri": ("Eri", "The Girl with Rewind Powers"),
        "nana": ("Nana Shimura", "All Might's Mentor"),
        "toga": ("Himiko Toga", "League of Villains' Transform Expert")
    },

"jojos_bizarre_adventure": {
        "jolyne": ("Jolyne Cujoh", "Stone Free Stand User and Jotaro's Daughter"),
        "lisa_lisa": ("Lisa Lisa", "Hamon Master and Joseph's Mother"),
        "erina": ("Erina Pendleton", "Jonathan's Wife and Hamon Healer"),
        "trish": ("Trish Una", "Spice Girl Stand User and Diavolo's Daughter"),
        "suzi_q": ("Suzi Q", "Joseph's Wife and Holy's Mother"),
        "holly": ("Holly Kujo", "Stand-Afflicted Mother of Jotaro"),
        "yukako": ("Yukako Yamagishi", "Love Deluxe Stand User and Koichi's Girlfriend"),
        "reimi": ("Reimi Sugimoto", "Ghost Girl and Kira's First Victim"),
        "hot_pants": ("Hot Pants", "Cream Starter Stand User and Nun"),
        "lucy": ("Lucy Steel", "Key Ally in Steel Ball Run"),
        "yasuho": ("Yasuho Hirose", "Paisley Park Stand User and Josuke's Aid"),
        "hermes": ("Hermes Costello", "Kiss Stand User and Jolyne's Friend"),
        "foo_fighters": ("Foo Fighters", "Plankton Stand User Known as F.F."),
        "ermes": ("Ermes Costello", "Vengeful Sister with Kiss Stand"),
        "gwess": ("Gwess", "Goo Goo Dolls Stand User"),
        "mariah": ("Mariah", "Bastet Stand User and DIO's Minion"),
        "midler": ("Midler", "High Priestess Stand User"),
        "anne": ("Anne", "Stowaway Girl from Part 3"),
        "tomoko": ("Tomoko Higashikata", "Josuke's Mother and Joseph's Former Lover")
    },

    "pokemon": {
        "misty": ("Misty", "Cerulean City Gym Leader and Water Pokemon Master"),
        "may": ("May", "Hoenn Coordinator and Daughter of Norman"),
        "dawn": ("Dawn", "Sinnoh Coordinator and Piplup's Trainer"),
        "serena": ("Serena", "Kalos Performer and Ash's Childhood Friend"),
        "iris": ("Iris", "Dragon Master and Unova Champion"),
        "lillie": ("Lillie", "Ultra Beast Researcher and Aether Foundation Heir"),
        "cynthia": ("Cynthia", "Sinnoh Champion and Archaeological Expert"),
        "diantha": ("Diantha", "Kalos Champion and Movie Star"),
        "lusamine": ("Lusamine", "Aether Foundation President"),
        "sabrina": ("Sabrina", "Saffron City Gym Leader and Psychic Master"),
        "erika": ("Erika", "Celadon City Gym Leader and Grass Expert"),
        "whitney": ("Whitney", "Goldenrod City Gym Leader with Miltank"),
        "jasmine": ("Jasmine", "Olivine City Gym Leader and Steel Specialist"),
        "clair": ("Clair", "Blackthorn City Gym Leader and Dragon Tamer"),
        "flannery": ("Flannery", "Lavaridge Town Gym Leader and Fire Expert"),
        "winona": ("Winona", "Fortree City Gym Leader and Flying Specialist"),
        "roxanne": ("Roxanne", "Rustboro City Gym Leader and Rock Expert"),
        "gardenia": ("Gardenia", "Eterna City Gym Leader and Grass Master"),
        "candice": ("Candice", "Snowpoint City Gym Leader and Ice Expert"),
        "fantina": ("Fantina", "Hearthome City Gym Leader and Ghost Specialist"),
        "elesa": ("Elesa", "Nimbasa City Gym Leader and Model"),
        "skyla": ("Skyla", "Mistralton City Gym Leader and Pilot"),
        "korrina": ("Korrina", "Shalour City Gym Leader and Mega Evolution User"),
        "valerie": ("Valerie", "Laverre City Gym Leader and Fairy Expert"),
        "olympia": ("Olympia", "Anistar City Gym Leader and Psychic Master"),
        "mallow": ("Mallow", "Alola Trial Captain and Chef"),
        "lana": ("Lana", "Alola Trial Captain and Fisher"),
        "nessa": ("Nessa", "Hulbury Gym Leader and Model"),
        "marnie": ("Marnie", "Spikemuth Gym Leader and Rival"),
        "sonia": ("Sonia", "Pokemon Professor and Researcher"),
        "professor_juniper": ("Professor Juniper", "Unova's Regional Professor"),
        "nurse_joy": ("Nurse Joy", "Pokemon Center Healer"),
        "officer_jenny": ("Officer Jenny", "Pokemon Police Officer"),
        "jessie": ("Jessie", "Team Rocket Member and Former Coordinator"),
        "bonnie": ("Bonnie", "Clemont's Sister and Future Trainer"),
        "rosa": ("Rosa", "Unova Pokemon Trainer")
    },

    "hatsune_miku": {
        "miku": ("Hatsune Miku", "The World's Virtual Idol and First Crypton Vocaloid"),
        "meiko": ("MEIKO", "The First Japanese Commercial Vocaloid"),
        "rin": ("Kagamine Rin", "The Energetic Half of the Kagamine Mirror Images"),
        "luka": ("Megurine Luka", "The Bilingual Diva of the Vocaloid World"),
        "gumi": ("GUMI", "The Green-Haired Voice of Internet Co.'s Megpoid"),
        "teto": ("Kasane Teto", "The Popular UTAU Voice Bank and Unofficial Vocaloid"),
        "neru": ("Akita Neru", "The Tsundere Derivative Character with a Cell Phone"),
        "haku": ("Yowane Haku", "The Failed Singing Voice Derivative Character"),
        "una": ("Otomachi Una", "The Sugar Voice Internet Co. Vocaloid"),
        "ia": ("IA", "The Spiritual Voiced 1st ARIA Vocaloid"),
        "cul": ("CUL", "The Red-Haired Rock-Style Vocaloid"),
        "lily": ("Lily", "The Internet Co. Ltd. Rock-inspired Vocaloid"),
        "miki": ("SF-A2 Miki", "The AH-Software Cherry-Voiced Vocaloid"),
        "yukari": ("Yuzuki Yukari", "The Purple-Haired Voiceroid and Vocaloid")
    },
}

# Configure logging
logger = logging.getLogger('AnimeCogs')

@dataclass
class CharacterInfo:
    """Store character information"""
    name: str
    title: str
    description: str
    folder: str
    aliases: List[str] = field(default_factory=list)
    source: str = ""


class ImageHandler:
    """Handle image file operations"""

    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)

    def get_random_image(self, subfolder: str) -> tuple[str, Path]:
        """Get a random image from specified subfolder"""
        dir_path = self.root_dir / subfolder

        try:
            files = [p for p in dir_path.iterdir() if p.is_file()]
            if not files:
                raise ValueError(f"No files found in {dir_path}")

            random_file = random.choice(files)
            return random_file.name, random_file

        except Exception as e:
            logger.error(f"Error accessing {dir_path}: {e}")
            raise


class BaseAnimeCog(commands.Cog):
    """Base cog for anime image commands"""

    def __init__(self, bot: commands.Bot, root_dir: str):
        self.bot = bot
        self.image_handler = ImageHandler(root_dir)
        self.characters: Dict[str, CharacterInfo] = {}

    async def cog_check(self, ctx: commands.Context) -> bool:
        """Prevent DM usage"""
        if isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("These commands are not available in DMs.")
            return False
        return True

    async def send_character_image(
            self,
            ctx: commands.Context,
            character: CharacterInfo
    ) -> None:
        """Send an embed with random character image"""
        try:
            filename, file_path = self.image_handler.get_random_image(character.folder)

            embed = discord.Embed(
                title=f"{character.title} ({character.source})",
                description=character.description
            )

            file = discord.File(
                file_path,
                filename=filename
            )

            embed.set_image(url=f"attachment://{filename}")
            await ctx.send(file=file, embed=embed)

        except Exception as e:
            logger.error(f"Error sending image for {character.name}: {e}")
            await ctx.send(f"Error retrieving image for {character.name}")

    def register_character_commands(self):
        """Register commands for all characters"""
        for char_info in self.characters.values():
            @commands.command(
                name=char_info.name.lower(),
                aliases=char_info.aliases
            )
            async def character_command(
                    self,
                    ctx: commands.Context,
                    char_info=char_info
            ):
                await self.send_character_image(ctx, char_info)

            self.__cog_commands__ = self.__cog_commands__ + (character_command,)


def create_character_info(name: str, source: str, desc_data: tuple, mapping_data: dict) -> CharacterInfo:
    """Helper function to create CharacterInfo objects from mapping data"""
    title, description = desc_data
    aliases = mapping_data.get(name, [])

    return CharacterInfo(
        name=name,
        title=title,
        description=description,
        folder=f"{source}/{name}",
        aliases=aliases,
        source=source.replace('_', ' ').title()
    )


class AnimeCog(BaseAnimeCog):
    """Combined cog for all anime/game characters"""

    def __init__(self, bot: commands.Bot):
        super().__init__(bot, "./images/")
        self.load_all_characters()
        self.register_character_commands()

    def load_all_characters(self):
        """Load all character mappings with their unique descriptions"""
        for source, characters in CHARACTER_DESCRIPTIONS.items():
            for char_name, desc_data in characters.items():
                mapping_data = CHARACTER_MAPPINGS[source]
                char_info = create_character_info(char_name, source, desc_data, mapping_data)
                self.characters[char_name] = char_info


class GifCog(BaseAnimeCog):
    """Cog for animated GIF images"""

    def __init__(self, bot: commands.Bot):
        super().__init__(bot, "./images/gifs/")
        self.load_gif_characters()
        self.register_character_commands()

    def load_gif_characters(self):
        """Load GIF versions of characters"""
        for source, characters in CHARACTER_DESCRIPTIONS.items():
            for char_name, (title, description) in characters.items():
                gif_name = f"{char_name}_gif"
                self.characters[gif_name] = CharacterInfo(
                    name=gif_name,
                    title=f"{title} Gif",
                    description=f"Animated GIF - {description}",
                    folder=f"{source}/gifs/{char_name}",
                    aliases=[f"gif_{char_name}", f"{char_name}-gif"],
                    source=source.replace('_', ' ').title()
                )


async def setup(bot: commands.Bot):
    """Setup function to add cogs to bot"""
    try:
        await bot.add_cog(AnimeCog(bot))
        await bot.add_cog(GifCog(bot))
        logger.info("Successfully loaded anime cogs")
    except Exception as e:
        logger.error(f"Error loading anime cogs: {e}")
        raise