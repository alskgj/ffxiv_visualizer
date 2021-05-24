import json

# todo automate this

data = {'Syrcus Tower': ['Shinobi'], 'the World of Darkness': ['Garm'], "Eden's Verse: Fulmination": ['Ramuh'],
        "Eden's Verse: Furor": ['Garuda'], "Eden's Verse: Fulmination (Savage)": ['Ramuh'],
        "Eden's Verse: Iconoclasm": ['The Idol Of Darkness'], "Eden's Verse: Refulgence": ['Shiva'],
        'The Copied Factory': ['Serial-Jointed Command Model'], "the Puppets' Bunker": ['813P-Operated Aegis Unit'],
        "Eden's Verse: Furor (Savage)": ['Garuda'], "Eden's Verse: Iconoclasm (Savage)": ['The Idol Of Darkness'],
        'the Labyrinth of the Ancients': ['Earth Homunculus'], "Eden's Gate: Resurrection": ['Eden Prime'],
        "Eden's Gate: Descent": ['Voidwalker'], "Eden's Gate: Inundation": ['Leviathan'],
        "Eden's Gate: Sepulture": ['Titan'], 'the Royal City of Rabanastre': ['Mateus, The Corrupt'],
        'the Ridorana Lighthouse': ['Famfrit, The Darkening Cloud'], 'the Orbonne Monastery': ['Harpy'],
        "Eden's Verse: Refulgence (Savage)": ['Shiva'], 'Deltascape V4.0 (Savage)': ['Exdeath'],
        'the Unending Coil of Bahamut (Ultimate)': ['Twintania'], 'Alexander - The Fist of the Father': ['Faust'],
        'Alexander - The Cuff of the Father': ['Gordian Footman'], "Eden's Promise: Eternity": ["Eden's Promise"],
        "Eden's Promise: Umbra (Savage)": ['Cloud Of Darkness'], "Eden's Promise: Litany (Savage)": ['Shadowkeeper'],
        "Eden's Promise: Umbra": ['Cloud Of Darkness'], "Eden's Promise: Litany": ['Shadowkeeper'],
        "Eden's Promise: Anamorphosis (Savage)": ['Fatebreaker'], "Eden's Promise: Anamorphosis": ['Fatebreaker'],
        "Eden's Promise: Eternity (Savage)": ["Eden's Promise"], "Eden's Gate: Resurrection (Savage)": ['Eden Prime'],
        "Eden's Gate: Descent (Savage)": ['Voidwalker'], "Eden's Gate: Inundation (Savage)": ['Leviathan'],
        "Eden's Gate: Sepulture (Savage)": ['Titan'], 'The Epic of Alexander (Ultimate)': ['Living Liquid'],
        "The Tower at Paradigm's Breach": ['Knave Of Hearts'], 'Sigmascape V4.0 (Savage)': ['Kefka'],
        "the Weapon's Refrain (Ultimate)": ['Garuda']}
data.update({'the Navel': ['Titan'], 'the Howling Eye': ['Garuda'], 'Cape Westwind': ['Rhitahtyn Sas Arvina'],
             'Thornmarch (Hard)': ['Whiskerwall Kupdi Koop'], 'the Whorleater (Hard)': ['Leviathan'],
             'the Striking Tree (Hard)': ['Grey Arbiter'], 'the Bowl of Embers (Hard)': ['Ifrit'],
             'the Howling Eye (Hard)': ['Garuda'], 'the Navel (Hard)': ['Titan'], 'the Chrysalis': ['Nabriales'],
             'the Steps of Faith': ['Vishap'], 'Thok ast Thok (Hard)': ['Ravana'],
             'the Limitless Blue (Hard)': ["Vuk'maii Vundu"], 'the Singularity Reactor': ['King Thordan'],
             'the Final Steps of Faith': ['Nidhogg'], 'the Limitless Blue (Extreme)': ["Vuk'maii Vundu"],
             'Containment Bay P1T6 (Extreme)': ['Sophia'], 'the Pool of Tribute': ['Susano'],
             'Emanation': ['Dreaming Kshatriya'], 'the Royal Menagerie': ['Shinryu'], 'Castrum Fluminis': ['Tsukuyomi'],
             'the Bowl of Embers': ['Infernal Nail'], 'the Seat of Sacrifice': ['Warrior Of Light'],
             "the Minstrel's Ballad: Thordan's Reign": ['King Thordan'],
             'Memoria Misera (Extreme)': ['Varis Yae Galvus'], 'the Dancing Plague (Extreme)': ['Titania'],
             'the Great Hunt': ['Rathalos'], 'the Great Hunt (Extreme)': ['Rathalos'],
             'the Crown of the Immaculate (Extreme)': ['Innocence'],
             "the Minstrel's Ballad: Tsukuyomi's Pain": ['Tsukuyomi'],
             "The Minstrel's Ballad: Hades's Elegy": ['Hades'], 'Containment Bay Z1T9 (Extreme)': ['Zurvan'],
             'Thok ast Thok (Extreme)': ['Ravana'], 'Containment Bay S1T7 (Extreme)': ['Sephirot'],
             'The Dying Gasp': ['Hades'],
             'The Dancing Plague': ['Mustardseed'], 'The Crown of the Immaculate': ['Innocence'],
             'Cinder Drift': ['The Ruby Weapon'], 'Castrum Marinum': ['The Emerald Weapon'],
             'Castrum Marinum (Extreme)': ['The Emerald Weapon'], "the Minstrel's Ballad: Nidhogg's Rage": ['Nidhogg'],
             'The Cloud Deck (Extreme)': ['The Diamond Weapon']})

with open('first_boss.json', 'w') as fo:
    json.dump(data, fo, indent=2, sort_keys=True)
