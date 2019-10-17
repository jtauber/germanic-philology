#!/usr/bin/env python3

from itertools import chain, zip_longest
import re


def merge(h, v, split="_", join="", redup="~"):
    if "-" in v:
        prefix, rest = v.split("-")
        prefix += "-"
    else:
        prefix = ""
        rest = v
    first = v.split("-")[~0].split(split)[0][:1]
    return prefix + join.join(
        chain.from_iterable(
            zip_longest(h.split(split), rest.split(split), fillvalue="")
        )
    ).replace(redup, first)

def gen_parts(h_pattern, v, post=lambda arg: arg):
    return [post(merge(h, v)) for h in h_pattern]

def phon(s):
    s = re.sub(r"(?<=')(.?)f", r"\1b", s)  # f → b / '(X)__
    s = re.sub(r"(?<=')(.?)þ", r"\1d", s)  # þ → d / '(X)__
    # s = re.sub(r"(?<=')hʷ", r"gʷ", s)  # hʷ → gʷ / '__
    # s = re.sub(r"(?<=')h", r"g", s)  # h → g / '__
    # s = re.sub(r"(?<=')s", r"z", s)  # s → z / '__
    s = re.sub(r"'", r"", s)
    #
    # s = re.sub(r"(?<=[ae])u(?=w)", r"w", s)  # u → w / V__w
    # s = re.sub(r"(?<=.)w(?=u)", r"(w)", s)  # w → (w) / X__u
    # s = re.sub(r"kʷ(?=u)", r"k", s)  # kʷ → k / __u
    # s = re.sub(r"gʷ(?=u)", r"g", s)  # gʷ → g / __u

    s = re.sub(r"(?<=[iē])u(?=[au])", r"w", s)  # u → w / V__V
    s = re.sub(r"a(?=u$)", r"á", s)  # a → á / __u#

    return s

templates = {}
with open("gothic-strong-verb-templates.txt") as f:
    for line in f:
        verb_class, inf, past_sg, past_pl, past_ptc = line.strip().split("|")
        templates[verb_class] = [inf, past_sg, past_pl, past_ptc]

roots = {
    "beitan": "b_t",
    "weihan": "w_h",
    "driusan": "dr_s",
    "tiuhan": "t_h",
    "ga-lūkan": "ga-l_k",
    "bindan": "b_nd",
    "waírþan": "w_rþ",
    "niman": "n_m",
    "baíran": "b_r",
    "trudan": "tr_þ",
    "qiþan": "q_þ",
    "giban": "g_f",
    "sniwan": "sn_u",
    "bidjan": "b_þ",
    "itan": "_t",
    "saíƕan": "s_ƕ",
    "fraíhnan": "fr_h",
    "faran": "f_r",
    "graban": "gr_f",
    "fraþjan": "fr_þ",
    "standan": "st_þ",
    "falþan": "f_lþ",
    "fāhan": "f_h",
    "háitan": "h_t",
    "slēpan": "sl_p",
    "ƕōpan": "ƕ_p",
    "*lauan": "l_",
    "áukan": "_k",
    "grētan": "gr_t",
    "ga-rēdan": "ga-r_þ",
    "saian": "s_",
}

with open("gothic-strong-verb-classes.txt") as f:
    for line in f:
        verb_class, gloss, inf, past_sg, past_pl, past_ptc = line.strip().split("|")
        if inf in roots:
            for c, a, b in zip([1, 2, 3, 4], [inf, past_sg, past_pl, past_ptc], gen_parts(templates[verb_class], roots[inf], phon)):
                if a.lstrip("*") != b:
                    print(inf, verb_class, f"expected {a} for {c}, got {b}")
