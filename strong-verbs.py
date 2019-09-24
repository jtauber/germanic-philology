from itertools import chain, zip_longest
import re


def merge(h, v, split="_", join=""):
    return join.join(
        chain.from_iterable(
            zip_longest(h.split(split), v.split(split), fillvalue="")
        )
    )

def gen_parts(h_pattern, v, post=lambda arg: arg):
    return [post(merge(h, v)) for h in h_pattern]

def phon(s):
    s = re.sub(r"(?<=')(.?)f", r"\1b", s)  # f → b / '(X)__
    s = re.sub(r"(?<=')(.?)þ", r"\1d", s)  # þ → d / '(X)__
    s = re.sub(r"(?<=')hʷ", r"gʷ", s)  # hʷ → gʷ / '__
    s = re.sub(r"(?<=')h", r"g", s)  # h → g / '__
    s = re.sub(r"(?<=')s", r"z", s)  # s → z / '__
    s = re.sub(r"'", r"", s)

    s = re.sub(r"(?<=[ae])u(?=w)", r"w", s)  # u → w / V__w
    s = re.sub(r"(?<=.)w(?=u)", r"(w)", s)  # w → (w) / X__u
    s = re.sub(r"kʷ(?=u)", r"k", s)  # kʷ → k / __u
    s = re.sub(r"gʷ(?=u)", r"g", s)  # gʷ → g / __u


    return s

def test(h_pattern, v_pattern, table):
    for v, row in zip(v_pattern, table):
        result = gen_parts(h_pattern, v, phon)
        for a, b in zip(result, row):
            if b and a != b:
                print(f"got {a} when expecting {b}")

v_pattern_1a = ["b_t", "b_d", "sn_þ"]
h_pattern_1a = ["_ī_aną", "_ai_", "_i'_un", "_i'_anaz"]

test(h_pattern_1a, v_pattern_1a, [
    ["bītaną",  "bait",  "bitun",  "bitanaz"],
    ["bīdaną",  "baid",  "bidun",  "bidanaz"],
    ["snīþaną", "snaiþ", "snidun", "snidanaz"],
])

v_pattern_1b = ["d_g", "st_k", "w_h"]
h_pattern_1b = ["_i'_aną", "_ai_", "_i'_un", "_i'_anaz"]

test(h_pattern_1b, v_pattern_1b, [
    ["diganą",  "daig",  "digun",  "diganaz"],
    ["stikaną", "staik", "stikun", "stikanaz"],
    ["wiganą",  "waih",  "wigun",  "wiganaz"],
])

test(h_pattern_1a, ["r_d"], [
    ["rīdaną", "raid", "ridun", "ridanaz"],
])

v_pattern_2a = ["g_t", "kl_b", "t_h"]
h_pattern_2a = ["_eu_aną", "_au_", "_u'_un", "_u'_anaz"]

test(h_pattern_2a, v_pattern_2a, [
    ["geutaną",  "gaut",  "gutun",  "gutanaz"],
    ["kleubaną", "klaub", "klubun", "klubanaz"],
    ["teuhaną",  "tauh",  "tugun",  "tuganaz"],
])

test(h_pattern_2a, ["k_w"], [
    ["kewwaną", "kaww", "ku(w)un", "kuwanaz"],
])

h_pattern_2c = ["_ū_aną", "_au_", "_u_un", "_u_anaz"]

test(h_pattern_2c, ["l_k"], [
    ["lūkaną", "lauk", "lukun", "lukanaz"],
])

v_pattern_3a = ["f_nþ", "dr_nk", "br_nn"]
h_pattern_3a = ["_i_aną", "_a_", "_u'_un", "_u'_anaz"]

test(h_pattern_3a, v_pattern_3a, [
    ["finþaną",  "fanþ",  "fundun",  "fundanaz"],
    ["drinkaną", "drank", "drunkun", "drunkanaz"],
    ["brinnaną", "brann", "brunnun", "brunnanaz"],
])

v_pattern_3b = ["w_rþ", "b_rg", "g_ld", "h_lp"]
h_pattern_3b = ["_e_aną", "_a_", "_u'_un", "_u'_anaz"]

test(h_pattern_3b, v_pattern_3b, [
    ["werþaną", "warþ", "wurdun", "wurdanaz"],
    ["berganą", "barg", "burgun", "burganaz"],
    ["geldaną", "gald", "guldun", "guldanaz"],
    ["helpaną", "halp", "hulpun", "hulpanaz"],
])

v_pattern_3c = ["þr_sk", "wr_skʷ", "fl_ht", "f_ht"]
h_pattern_3c = ["_e_aną", "_a_", "_u_un", "_u_anaz"]

test(h_pattern_3c, v_pattern_3c, [
    ["þreskaną",  "þrask",  "þruskun", "þruskanaz"],
    ["wreskʷaną", "wraskʷ", "wruskun", "wruskʷanaz"],
    ["flehtaną",  "flaht",  "fluhtun", "fluhtanaz"],
    ["fehtaną",   "faht",   "fuhtun",  "fuhtanaz"],
])

v_pattern_4a = [
    "b_r", "t_r", "sk_r", "st_l", "dw_l", "h_l", "kʷ_m", "n_m", "t_m", "st_n"
]
h_pattern_4a = ["_e_aną", "_a_", "_ē_un", "_u_anaz"]

test(h_pattern_4a, v_pattern_4a, [
    ["beraną", "bar", "bērun", "buranaz"],
    ["teraną", "tar", "tērun", "turanaz"],
    ["skeraną", "skar", "skērun", "skuranaz"],
    ["stelaną", "stal", "stēlun", "stulanaz"],
    ["dwelaną", "dwal", "dwēlun", "d(w)ulanaz"],
    ["helaną", "hal", "hēlun", "hulanaz"],
    ["kʷemaną", "kʷam", "kʷēmun", "kumanaz"],
    ["nemaną", "nam", "nēmun", "numanaz"],
    ["temaną", "tam", "tēmun", "tumanaz"],
    ["stenaną", "stan", "stēnun", "stunanaz"],
])

test(h_pattern_4a, ["br_k"], [
    ["brekaną", "brak", "brēkun", "brukanaz"],
]),

test(["_e_aną", "_a_", "_ē'_un", "_e'_anaz"], ["_t"], [
    ["etaną", "eeet", "ētun", "etanaz"],
]),

h_pattern_5a = ["_e_aną", "_a_", "_ē'_un", "_e'_anaz"]

test(h_pattern_5a, ["g_b", "kʷ_þ", "s_hʷ", "w_s"], [
    ["gebaną", "gab", "gēbun", "gebanaz"],
    ["kʷeþaną", "kʷaþ", "kʷēdun", "kʷedanaz"],
    ["sehʷaną", "sahʷ", "sēgun", "sewanaz"],
    ["wesaną", "was", "wēzun", None],
]),

h_pattern_5b = ["_i_janą", "_a_", "_ē_un", "_e_anaz"]

test(h_pattern_5b, ["b_d", "l_g", "s_t"], [
    ["bidjaną", "bad", "bēdun", "bedanaz"],
    ["ligjaną", "lag", "lēgun", "leganaz"],
    ["sitjaną", "sat", "sētun", "setanaz"],
]),

# 6

h_pattern_6a = ["_a_aną", "_ō_", "_ō'_un", "_a'_anaz"]

test(h_pattern_6a, ["f_r", "sl_h", "hl_þ", "w_d"], [
    ["faraną", "fōr", "fōrun", "faranaz"],
    ["slahaną", "slōh", "slōgun", "slaganaz"],
    ["hlaþaną", "hlōþ", "hlōdun", "hladanaz"],
    ["wadaną", "wōd", "wōdun", "wadanaz"],
])

h_pattern_6b = ["_a_janą", "_ō_", "_ō'_un", "_a'_anaz"]

test(h_pattern_6b, ["kʷ_b", "sk_p", "hl_h", "fr_þ"], [
    ["kʷabjaną", "kʷōb", "kʷōbun", "kʷabanaz"],
    ["skapjaną", "skōp", "skōpun", "skapanaz"],
    ["hlahjaną", "hlōh", "hlōgun", None],
    ["fraþjaną", "frōþ", "frōdun", "fradanaz"],
])

h_pattern_6c = ["_a'_janą", "_ō_", "_ō'_un", "_a'_anaz"]

test(h_pattern_6c, ["sw_r", "h_f", "-s_f"], [
    ["swarjaną", "swōr", "swōrun", "s(w)uranaz"],
    ["habjaną", "hōf", "hōbun", "habanaz"],
    ["-sabjaną", "-sōf", "-sōbun", "-sabanaz"],
])

h_pattern_6d = ["_a_ijaną", "_ō_", "_ō_un", "_a_anaz"]

test(h_pattern_6d, ["w_hs"], [
    ["wahsijaną", "wōhs", "wōhsun", "wahsanaz"],
])

h_pattern_6e = ["_a'n_aną", "_ō_", "_ō'_un", "_a'_anaz"]

test(h_pattern_6e, ["st_þ"], [
    ["standaną", "stōþ", "stōdun", "stadanaz"],
])
