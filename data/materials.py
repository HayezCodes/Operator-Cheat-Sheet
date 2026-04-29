LATHE_MATERIALS = {
    "10 Series Steel": {
        "rough": {"sfm": 500, "ipr": 0.016, "doc": ".15 - .25 / side", "insert": "DNMG", "chipbreaker": "PF for softer steels, MR/MF/MRR for harder steels", "notes": "10 series steel roughing baseline. More aggressive than 40 series."},
        "finish": {"sfm": 700, "ipr": 0.0055, "doc": ".010 - .015 total remaining", "insert": "VNMG", "chipbreaker": "PF for softer steels, MR/MF/MRR for harder steels", "notes": "10 series steel finishing baseline. More aggressive than 40 series."},
    },
    "40 Series Steel": {
        "rough": {"sfm": 450, "ipr": 0.015, "doc": ".15 - .25 / side", "insert": "DNMG", "chipbreaker": "PF for softer steels, MR/MF/MRR for harder steels", "notes": "40 series steel roughing baseline. This is your previous plain steel baseline."},
        "finish": {"sfm": 600, "ipr": 0.005, "doc": ".010 - .015 total remaining", "insert": "VNMG", "chipbreaker": "PF for softer steels, MR/MF/MRR for harder steels", "notes": "40 series steel finishing baseline. This is your previous plain steel baseline."},
    },
    "17-4 / 300 Series": {
        "rough": {"sfm": 220, "ipr": 0.012, "doc": ".120 / side", "insert": "DNMG", "chipbreaker": "MR / MF / MRR", "notes": "Mazak OD roughing baseline."},
        "finish": {"sfm": 280, "ipr": 0.0045, "doc": ".010 - .015 total remaining", "insert": "VNMG", "chipbreaker": "MR / MF / MRR", "notes": "Light finish pass."},
    },
    "Duplex / Alloy 20": {
        "rough": {"sfm": 140, "ipr": 0.010, "doc": ".100 - .120 / side", "insert": "DNMG", "chipbreaker": "MR / MF / MRR", "notes": "Conservative roughing baseline."},
        "finish": {"sfm": 190, "ipr": 0.004, "doc": ".010 - .015 total remaining", "insert": "VNMG", "chipbreaker": "MR / MF / MRR", "notes": "Light finish pass."},
    },
    "Hastelloy": {
        "rough": {"sfm": 130, "ipr": 0.009, "doc": ".100 / side max", "insert": "DNMG", "chipbreaker": "SM", "notes": "Keep heat under control."},
        "finish": {"sfm": 180, "ipr": 0.004, "doc": ".010 total preferred", "insert": "VNMG", "chipbreaker": "SM", "notes": "Light, stable finish cut."},
    },
    "Titanium": {
        "rough": {"sfm": 180, "ipr": 0.008, "doc": ".080 - .120 / side", "insert": "DNMG", "chipbreaker": "SM", "notes": "Watch heat and maintain chipload."},
        "finish": {"sfm": 220, "ipr": 0.0035, "doc": ".005 - .010 total remaining", "insert": "VNMG", "chipbreaker": "SM", "notes": "Stable, light finish."},
    },
    "Monel": {
        "rough": {"sfm": 110, "ipr": 0.0085, "doc": ".080 - .100 / side", "insert": "DNMG", "chipbreaker": "SM / MF", "notes": "Conservative Monel roughing baseline. Keep pressure on the cut."},
        "finish": {"sfm": 150, "ipr": 0.0035, "doc": ".006 - .012 total remaining", "insert": "VNMG", "chipbreaker": "SM / MF", "notes": "Light Monel finish pass. Avoid rubbing."},
    },
    "Zirconium": {
        "rough": {"sfm": 90, "ipr": 0.0070, "doc": ".060 - .090 / side", "insert": "DNMG", "chipbreaker": "SM", "notes": "Very conservative zirconium roughing baseline. Keep heat controlled."},
        "finish": {"sfm": 120, "ipr": 0.0030, "doc": ".005 - .010 total remaining", "insert": "VNMG", "chipbreaker": "SM", "notes": "Stable zirconium finish pass with light stock to clean."},
    },
}

MILL_MATERIALS = {
    "10 Series Steel": {
        "Spot Drill": {"sfm": 90, "ipr": 0.0028, "notes": "10 series steel spot drill baseline."},
        "Drill": {"sfm": 80, "ipr": 0.0045, "notes": "10 series steel drilling baseline."},
        "Tap": {"sfm": 90, "notes": "10 series steel tapping baseline."},
        "Endmill": {"rough_sfm": 325, "rough_ipt": 0.0022, "rough_slot_doc_factor": 0.50, "rough_side_doc_factor": 1.00, "finish_sfm": 375, "finish_ipt": 0.0011, "finish_slot_doc_factor": 0.10, "finish_side_doc_factor": 0.25, "finish_radial": "0.010 - 0.020 radial", "notes": "10 series steel carbide endmill baseline. More aggressive than 40 series."},
    },
    "40 Series Steel": {
        "Spot Drill": {"sfm": 80, "ipr": 0.0025, "notes": "40 series steel spot drill baseline. This is your previous plain steel baseline."},
        "Drill": {"sfm": 70, "ipr": 0.0040, "notes": "40 series steel drilling baseline. This is your previous plain steel baseline."},
        "Tap": {"sfm": 80, "notes": "40 series steel tapping baseline. This is your previous plain steel baseline."},
        "Endmill": {"rough_sfm": 300, "rough_ipt": 0.0020, "rough_slot_doc_factor": 0.50, "rough_side_doc_factor": 1.00, "finish_sfm": 350, "finish_ipt": 0.0010, "finish_slot_doc_factor": 0.10, "finish_side_doc_factor": 0.25, "finish_radial": "0.010 - 0.020 radial", "notes": "40 series steel carbide endmill baseline. This is your previous plain steel baseline."},
    },
    "17-4 / 300 Series": {
        "Spot Drill": {"sfm": 50, "ipr": 0.0020, "notes": "Use conservative spotting."},
        "Drill": {"sfm": 45, "ipr": 0.0030, "notes": "Conservative drilling baseline."},
        "Tap": {"sfm": 50, "notes": "Tapping baseline."},
        "Endmill": {"rough_sfm": 180, "rough_ipt": 0.0015, "rough_slot_doc_factor": 0.35, "rough_side_doc_factor": 0.75, "finish_sfm": 220, "finish_ipt": 0.0008, "finish_slot_doc_factor": 0.08, "finish_side_doc_factor": 0.20, "finish_radial": "0.005 - 0.015 radial", "notes": "Conservative endmill baseline."},
    },
    "Duplex / Alloy 20": {
        "Spot Drill": {"sfm": 40, "ipr": 0.0018, "notes": "Conservative spotting."},
        "Drill": {"sfm": 35, "ipr": 0.0025, "notes": "Keep pressure on the cut."},
        "Tap": {"sfm": 30, "notes": "Slow tapping baseline."},
        "Endmill": {"rough_sfm": 140, "rough_ipt": 0.0012, "rough_slot_doc_factor": 0.30, "rough_side_doc_factor": 0.60, "finish_sfm": 170, "finish_ipt": 0.0007, "finish_slot_doc_factor": 0.08, "finish_side_doc_factor": 0.18, "finish_radial": "0.005 - 0.010 radial", "notes": "Keep chipload consistent."},
    },
    "Hastelloy": {
        "Spot Drill": {"sfm": 30, "ipr": 0.0015, "notes": "Low-speed spotting."},
        "Drill": {"sfm": 25, "ipr": 0.0020, "notes": "Heat control matters."},
        "Tap": {"sfm": 25, "notes": "Very conservative tapping baseline."},
        "Endmill": {"rough_sfm": 100, "rough_ipt": 0.0010, "rough_slot_doc_factor": 0.25, "rough_side_doc_factor": 0.50, "finish_sfm": 120, "finish_ipt": 0.0005, "finish_slot_doc_factor": 0.06, "finish_side_doc_factor": 0.15, "finish_radial": "0.003 - 0.008 radial", "notes": "Avoid rubbing."},
    },
    "Titanium": {
        "Spot Drill": {"sfm": 35, "ipr": 0.0015, "notes": "Avoid heat buildup."},
        "Drill": {"sfm": 30, "ipr": 0.0020, "notes": "Keep speed low."},
        "Tap": {"sfm": 40, "notes": "Controlled tapping baseline."},
        "Endmill": {"rough_sfm": 150, "rough_ipt": 0.0012, "rough_slot_doc_factor": 0.25, "rough_side_doc_factor": 0.50, "finish_sfm": 180, "finish_ipt": 0.0006, "finish_slot_doc_factor": 0.06, "finish_side_doc_factor": 0.15, "finish_radial": "0.003 - 0.008 radial", "notes": "Maintain chipload."},
    },
    "Monel": {
        "Spot Drill": {"sfm": 28, "ipr": 0.0014, "notes": "Conservative Monel spotting baseline."},
        "Drill": {"sfm": 22, "ipr": 0.0018, "notes": "Low-speed Monel drilling baseline. Keep pressure on the cut."},
        "Tap": {"sfm": 20, "notes": "Very conservative Monel tapping baseline."},
        "Endmill": {"rough_sfm": 90, "rough_ipt": 0.0009, "rough_slot_doc_factor": 0.22, "rough_side_doc_factor": 0.45, "finish_sfm": 115, "finish_ipt": 0.0005, "finish_slot_doc_factor": 0.05, "finish_side_doc_factor": 0.12, "finish_radial": "0.003 - 0.008 radial", "notes": "Monel likes a steady chip. Avoid light rubbing cuts."},
    },
    "Zirconium": {
        "Spot Drill": {"sfm": 22, "ipr": 0.0012, "notes": "Very conservative zirconium spotting baseline."},
        "Drill": {"sfm": 18, "ipr": 0.0016, "notes": "Slow zirconium drilling baseline. Keep heat down."},
        "Tap": {"sfm": 18, "notes": "Conservative zirconium tapping baseline."},
        "Endmill": {"rough_sfm": 75, "rough_ipt": 0.0008, "rough_slot_doc_factor": 0.20, "rough_side_doc_factor": 0.40, "finish_sfm": 95, "finish_ipt": 0.0004, "finish_slot_doc_factor": 0.05, "finish_side_doc_factor": 0.10, "finish_radial": "0.002 - 0.006 radial", "notes": "Zirconium baseline kept intentionally conservative for heat control."},
    },
}

DRILL_DATA = {
    "10 Series Steel": {
        "HSS": {"sfm": 80, "ipr": 0.0045, "notes": "10 series steel HSS drill baseline."},
        "HSS Coated": {"sfm": 100, "ipr": 0.0050, "notes": "10 series steel coated HSS baseline."},
        "Cobalt": {"sfm": 110, "ipr": 0.0055, "notes": "10 series steel cobalt drill baseline."},
        "CoroDrill": {"sfm": 240, "ipr": 0.0065, "notes": "10 series steel CoroDrill larger-hole baseline."},
    },
    "40 Series Steel": {
        "HSS": {"sfm": 70, "ipr": 0.0040, "notes": "40 series steel HSS drill baseline. This is your previous plain steel baseline."},
        "HSS Coated": {"sfm": 90, "ipr": 0.0045, "notes": "40 series steel coated HSS baseline. This is your previous plain steel baseline."},
        "Cobalt": {"sfm": 100, "ipr": 0.0050, "notes": "40 series steel cobalt drill baseline. This is your previous plain steel baseline."},
        "CoroDrill": {"sfm": 220, "ipr": 0.0060, "notes": "40 series steel CoroDrill larger-hole baseline. This is your previous plain steel baseline."},
    },
    "17-4 / 300 Series": {
        "HSS": {"sfm": 30, "ipr": 0.0025, "notes": "Conservative stainless HSS baseline."},
        "HSS Coated": {"sfm": 40, "ipr": 0.0030, "notes": "Coated HSS stainless baseline."},
        "Cobalt": {"sfm": 50, "ipr": 0.0035, "notes": "Cobalt stainless baseline."},
        "CoroDrill": {"sfm": 140, "ipr": 0.0045, "notes": "CoroDrill stainless baseline."},
    },
    "Duplex / Alloy 20": {
        "HSS": {"sfm": 20, "ipr": 0.0020, "notes": "Conservative duplex/alloy HSS baseline."},
        "HSS Coated": {"sfm": 25, "ipr": 0.0022, "notes": "Coated HSS duplex/alloy baseline."},
        "Cobalt": {"sfm": 35, "ipr": 0.0028, "notes": "Cobalt duplex/alloy baseline."},
        "CoroDrill": {"sfm": 100, "ipr": 0.0040, "notes": "CoroDrill duplex/alloy baseline."},
    },
    "Hastelloy": {
        "HSS": {"sfm": 15, "ipr": 0.0015, "notes": "Very conservative Hastelloy HSS baseline."},
        "HSS Coated": {"sfm": 20, "ipr": 0.0018, "notes": "Coated HSS Hastelloy baseline."},
        "Cobalt": {"sfm": 25, "ipr": 0.0022, "notes": "Cobalt Hastelloy baseline."},
        "CoroDrill": {"sfm": 80, "ipr": 0.0035, "notes": "CoroDrill Hastelloy baseline."},
    },
    "Titanium": {
        "HSS": {"sfm": 20, "ipr": 0.0018, "notes": "Conservative titanium HSS baseline."},
        "HSS Coated": {"sfm": 25, "ipr": 0.0020, "notes": "Coated HSS titanium baseline."},
        "Cobalt": {"sfm": 30, "ipr": 0.0025, "notes": "Cobalt titanium baseline."},
        "CoroDrill": {"sfm": 90, "ipr": 0.0038, "notes": "CoroDrill titanium baseline."},
    },
    "Monel": {
        "HSS": {"sfm": 16, "ipr": 0.0015, "notes": "Conservative Monel HSS drill baseline."},
        "HSS Coated": {"sfm": 20, "ipr": 0.0017, "notes": "Coated HSS Monel drill baseline."},
        "Cobalt": {"sfm": 24, "ipr": 0.0020, "notes": "Cobalt Monel drill baseline."},
        "CoroDrill": {"sfm": 70, "ipr": 0.0032, "notes": "CoroDrill Monel baseline with conservative feed."},
    },
    "Zirconium": {
        "HSS": {"sfm": 12, "ipr": 0.0013, "notes": "Very conservative zirconium HSS drill baseline."},
        "HSS Coated": {"sfm": 16, "ipr": 0.0015, "notes": "Coated HSS zirconium drill baseline."},
        "Cobalt": {"sfm": 20, "ipr": 0.0018, "notes": "Cobalt zirconium drill baseline."},
        "CoroDrill": {"sfm": 55, "ipr": 0.0028, "notes": "CoroDrill zirconium baseline. Watch heat closely."},
    },
}

TAP_SFM = {
    "10 Series Steel": 60,
    "40 Series Steel": 50,
    "17-4 / 300 Series": 20,
    "Duplex / Alloy 20": 15,
    "Hastelloy": 10,
    "Titanium": 15,
    "Monel": 12,
    "Zirconium": 10,
}

OD_THREADING = {
    "10 Series Steel": {"sfm": 400, "ipr": 0.0042},
    "40 Series Steel": {"sfm": 350, "ipr": 0.0040},
    "17-4 / 300 Series": {"sfm": 120, "ipr": 0.0035},
    "Duplex / Alloy 20": {"sfm": 90, "ipr": 0.003},
    "Hastelloy": {"sfm": 80, "ipr": 0.003},
    "Titanium": {"sfm": 100, "ipr": 0.003},
    "Monel": {"sfm": 75, "ipr": 0.0028},
    "Zirconium": {"sfm": 65, "ipr": 0.0025},
}

OPERATOR_NOTES = {
    "Steel": [
        "IF IT SQUEALS -> FEED TOO LIGHT -> INCREASE FEED",
        "IF IT CHATTERS -> REDUCE RPM FIRST, NOT FEED",
        "IF IT SMEARS OR BUILDS EDGE -> INCREASE CHIPLOAD",
        "IF IT OVERHEATS / BLUE CHIPS -> REDUCE RPM 10-15%",
        "IF IT HAS DUST OR POWDER CHIPS -> FEED TOO LIGHT",
        "IF HAMMERING / THUDDING -> REDUCE FEED SLIGHTLY",
        "",
        "CARBIDE LIKES PRESSURE",
        "STEEL AND STAINLESS HATE RUBBING",
        "CHATTER IS A SPEED PROBLEM FIRST",
        "DO NOT FIX CHATTER BY STARVING FEED",
        "MAKE A REAL CHIP OR IT WILL WORK HARDEN",
    ],
    "Titanium": [
        "IF IT SQUEALS -> FEED TOO LIGHT -> INCREASE FEED",
        "IF IT CHATTERS -> REDUCE DOC FIRST, THEN RPM",
        "IF TOOL GETS HOT FAST -> RPM TOO HIGH -> REDUCE 10-20%",
        "IF SMEARING OR RUB MARKS -> INCREASE FEED",
        "IF INSERT NOTCHING -> SPEED TOO HIGH OR DWELLING",
        "",
        "TITANIUM HATES HEAT",
        "KEEP SPEED LOW",
        "MAINTAIN CHIPLOAD AT ALL TIMES",
        "DO NOT DWELL",
        "DO NOT RUB",
        "CONTROL DOC BEFORE SPEED WHEN CHASING CHATTER",
    ],
    "Duplex": [
        "IF IT CHATTERS -> REDUCE RPM FIRST",
        "IF INSERT WEARS FAST -> SPEED TOO HIGH",
        "IF SMEARING -> INCREASE FEED",
        "IF WORK HARDENING -> YOU ARE RUBBING",
        "",
        "DUPLEX WORK HARDENS FAST",
        "KEEP CONSISTENT CHIPLOAD",
        "DO NOT TAKE LIGHT PASSES",
        "KEEP TOOL ENGAGED",
        "AVOID DWELLING",
    ],
    "Hastelloy": [
        "IF IT GETS HOT FAST -> SPEED TOO HIGH",
        "IF INSERT BREAKS DOWN QUICK -> REDUCE SPEED",
        "IF SMEARING -> INCREASE FEED",
        "IF CHATTER -> REDUCE RPM SLIGHTLY",
        "",
        "HEAT IS THE ENEMY",
        "KEEP FEED ON THE TOOL",
        "AVOID RUBBING",
        "TAKE CONTROLLED PASSES",
        "WATCH INSERT EDGE CLOSELY",
    ],
    "Monel": [
        "IF IT SMEARS -> INCREASE FEED OR REDUCE RPM",
        "IF IT WORK HARDENS -> DO NOT DWELL",
        "IF TOOL LIFE DROPS FAST -> SPEED TOO HIGH",
        "",
        "MONEL WORK HARDENS FAST",
        "KEEP A STEADY CHIP",
        "DO NOT RUB OR PECK LIGHTLY",
    ],
    "Zirconium": [
        "IF HEAT BUILDS FAST -> REDUCE RPM",
        "IF CUT FEELS DRY OR SMEARY -> INCREASE CHIPLOAD SLIGHTLY",
        "IF TOOL DISCOLORS QUICKLY -> SPEED IS TOO HIGH",
        "",
        "KEEP HEAT DOWN",
        "USE A STABLE CUT",
        "AVOID DWELLING AND RUBBING",
    ],
    "General": [
        "START WITH THE APP NUMBER, THEN ADJUST TO ACTUAL CUT CONDITIONS.",
        "VERIFY RIGIDITY, TOOL STICKOUT, HOLDING, AND COOLANT BEFORE PUSHING A CUT.",
        "IF THE CUT SOUNDS WRONG, CHANGE ONE THING AT A TIME.",
        "WHEN IN DOUBT, BACK RPM DOWN FIRST AND KEEP CHIPLOAD REAL.",
    ],
}
