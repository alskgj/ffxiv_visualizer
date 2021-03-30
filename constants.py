from datetime import timedelta
import re
from enum import Enum

ACTOR_CONTROL_LINES = 33
INSTANCED = 8003
ACTOR_CONTROL_LINES_WIPE = 40000005
NetworkAbility = 21  # 0x15
NetworkDeath = 0x19

# phases - always until
enrage_time_twintania = timedelta(minutes=3, seconds=4)
enrage_time_nael = enrage_time_twintania + timedelta(minutes=3, seconds=25)
enrage_time_bahamut_prime = enrage_time_nael + timedelta(minutes=5, seconds=34)
enrage_time_nael_twintania = enrage_time_bahamut_prime + timedelta(minutes=2, seconds=19)
enrage_time_gold_bahamut = enrage_time_nael_twintania + timedelta(minutes=3, seconds=29)


# maps different things that kill to the corresponding phase
kill_mechanics = {
    'Twintania': 'Twintania',
    'Oviform': 'Twintania',  # hatch


    'Nael Deus Darnus': 'Neal Deus Darnus',

    # Neal add dragons
    'Firehorn': 'Neal Deus Darnus',
    'Thunderwing': 'Neal Deus Darnus',
    'Tail Of Darkness': 'Neal Deus Darnus',
    'Fang Of Light': 'Neal Deus Darnus',
    'Iceclaw': 'Neal Deus Darnus',
    'Nael Geminus': 'Neal Deus Darnus',
    'Ragnarok': 'Neal Deus Darnus',

    # Not sure about those
    '': 'Edge',

    'Bahamut Prime': 'Bahamut Prime'
}

ucob = {
    'start_pattern': re.compile(r'01\|.+the Unending Coil of Bahamut \(Ultimate\)\|')
}

# e12s
e12s = {
    'start_pattern': re.compile(r"01\|.+Eden's Promise: Eternity \(Savage\)\|")

}


class Fights(Enum):
    UNKNOWN = 1
    UCOB = 2


class LogTypes(Enum):
    LogLine = 1
    ChangeZone = 2
    ChangePrimaryPlayer = 3
    AddCombatant = 4
    PlayerStats = 5
    PartyList = 6
    NetworkBuff = 7
    NetworkStatusEffect = 8
    NetworkUpdateHP = 9

    NetworkRaidMarker = 10
    NetworkNameToggle = 11

    NetworkAbility = 12

    NetworkActionSync = 13
    NetworkStartsCasting = 14
    NetworkBuffRemove = 15

    NetworkAOEAbility = 16
    NetworkCancelAbility = 17

    NetworkDoT = 18

    NetworkGauge = 19
    LimitBreak = 20

    NetworkTargetIcon = 21
    NetworkDeath = 22
    ActorControlLine = 23
    RemoveCombatant = 24
    NetworkTether = 25

    Debug = 26

    Unknown = 100


class ActorControlTypes(Enum):
    InitialCommence = 1
    Recommence = 2
    LockoutTimeAdjust = 3
    ChargeBossLimitBreak = 4
    MusicChange = 5
    FadeOut = 6
    FadeIn = 7
    BarrierUp = 8
    Victory = 9

    UnknownActorControlD = 10
    UnknownActorControl7 = 11
    UnknownActorControl8D = 12
    UnknownActorControl8 = 13
    UnknownActorControl9 = 14



actor_control_types_mapping = {
    '40000001': ActorControlTypes.InitialCommence,
    '40000006': ActorControlTypes.Recommence,
    '80000004': ActorControlTypes.LockoutTimeAdjust,
    '8000000C': ActorControlTypes.ChargeBossLimitBreak,
    '80000001': ActorControlTypes.MusicChange,
    '40000005': ActorControlTypes.FadeOut,
    '40000010': ActorControlTypes.FadeIn,
    '40000012': ActorControlTypes.BarrierUp,
    '40000003': ActorControlTypes.Victory,

    '4000000D': ActorControlTypes.UnknownActorControlD,
    '8000000D': ActorControlTypes.UnknownActorControl8D,
    '40000007': ActorControlTypes.UnknownActorControl7,
    '80000008': ActorControlTypes.UnknownActorControl8,
    '80000009': ActorControlTypes.UnknownActorControl9

}


class LogLineType(Enum):
    SYSTEMMESSAGE = 0x0839
    PLAYERMESSAGE = 0x000e
    DAMAGEMESSAGE = 0x1329
    COUNTDOWNMESSAGE = 0x0039

    UNKNOWN = 0xFFFF


# can be used to detect start of fights
object_ids = {
    'Twintania': 'UCoB',
    'The Idol Of Darkness': 'e7',
    'Shiva': 'e8',
    'Neo Exdeath': 'o4',
    'Striking Dummy': 'Dummy'
}

# from https://github.com/quisquous/cactbot/blob/main/resources/zone_id.js
zone_ids = {'230': 'ABloodyReunion', '170': 'ARelicRebornTheChimera', '171': 'ARelicRebornTheHydra',
            '33e': 'ARequiemForHeroes', '392': 'ASleepDisturbed', '215': 'ASpectacleForTheAges',
            '21c': 'AccrueEnmityFromMultipleTargets', '340': 'AirForceOne', '349': 'AkadaemiaAnyder', '2b1': 'AlaMhigo',
            '1bc': 'AlexanderTheArmOfTheFather', '1c3': 'AlexanderTheArmOfTheFatherSavage',
            '20a': 'AlexanderTheArmOfTheSon', '213': 'AlexanderTheArmOfTheSonSavage',
            '245': 'AlexanderTheBreathOfTheCreator', '249': 'AlexanderTheBreathOfTheCreatorSavage',
            '1bd': 'AlexanderTheBurdenOfTheFather', '1c4': 'AlexanderTheBurdenOfTheFatherSavage',
            '20b': 'AlexanderTheBurdenOfTheSon', '214': 'AlexanderTheBurdenOfTheSonSavage',
            '1bb': 'AlexanderTheCuffOfTheFather', '1c2': 'AlexanderTheCuffOfTheFatherSavage',
            '209': 'AlexanderTheCuffOfTheSon', '212': 'AlexanderTheCuffOfTheSonSavage',
            '244': 'AlexanderTheEyesOfTheCreator', '248': 'AlexanderTheEyesOfTheCreatorSavage',
            '1ba': 'AlexanderTheFistOfTheFather', '1c1': 'AlexanderTheFistOfTheFatherSavage',
            '208': 'AlexanderTheFistOfTheSon', '211': 'AlexanderTheFistOfTheSonSavage',
            '246': 'AlexanderTheHeartOfTheCreator', '24a': 'AlexanderTheHeartOfTheCreatorSavage',
            '247': 'AlexanderTheSoulOfTheCreator', '24b': 'AlexanderTheSoulOfTheCreatorSavage',
            'dc': 'AllsWellThatEndsInTheWell', '31c': 'AllsWellThatStartsWell', '31e': 'AlphascapeV10',
            '322': 'AlphascapeV10Savage', '31f': 'AlphascapeV20', '323': 'AlphascapeV20Savage', '320': 'AlphascapeV30',
            '324': 'AlphascapeV30Savage', '321': 'AlphascapeV40', '325': 'AlphascapeV40Savage', '346': 'Amaurot',
            'a7': 'AmdaporKeep', 'bd': 'AmdaporKeepHard', '32f': 'AmhAraeng', '382': 'AnamnesisAnyder',
            'de': 'AnnoyTheVoid', '37e': 'AsTheHeartBids', '220': 'AssistAlliesInDefeatingATarget', '2d9': 'Astragalos',
            '219': 'AvoidAreaOfEffectAttacks', '192': 'AzysLla', '267': 'BaelsarsWall', '26f': 'BardamsMettle',
            'd6': 'BasicTrainingEnemyParties', 'd7': 'BasicTrainingEnemyStrongholds', '18c': 'BattleInTheBigKeep',
            '16e': 'BattleOnTheBigBridge', '2c4': 'BloodOnTheDeck', '9e': 'BrayfloxsLongstop',
            '16a': 'BrayfloxsLongstopHard', '14c': 'CapeWestwind', '295': 'CastrumAbania', '30a': 'CastrumFluminis',
            '3a6': 'CastrumMarinum', '3c7': 'CastrumMarinumDrydocks', '3a7': 'CastrumMarinumExtreme',
            'd9': 'CastrumMeridianum', '94': 'CentralShroud', '8d': 'CentralThanalan', '185': 'ChocoboRaceCostaDelSol',
            '186': 'ChocoboRaceSagoliiRoad', '187': 'ChocoboRaceTranquilPaths', '1a1': 'ChocoboRaceTutorial',
            '381': 'CinderDrift', '390': 'CinderDriftExtreme', '9b': 'CoerthasCentralHighlands',
            '18d': 'CoerthasWesternHighlands', '35c': 'ComingClean', '240': 'ContainmentBayP1T6',
            '241': 'ContainmentBayP1T6Extreme', '205': 'ContainmentBayS1T7', '20c': 'ContainmentBayS1T7Extreme',
            '27d': 'ContainmentBayZ1T9', '27e': 'ContainmentBayZ1T9Extreme', 'a1': 'CopperbellMines',
            '15d': 'CopperbellMinesHard', '2cd': 'CuriousGorgeMeetsHisMatch', 'aa': 'CuttersCry',
            '2c9': 'DarkAsTheNightSky', '221': 'DefeatAnOccupiedTarget', '2b3': 'DeltascapeV10',
            '2b7': 'DeltascapeV10Savage', '2b4': 'DeltascapeV20', '2b8': 'DeltascapeV20Savage', '2b5': 'DeltascapeV30',
            '2b9': 'DeltascapeV30Savage', '2b6': 'DeltascapeV40', '2ba': 'DeltascapeV40Savage',
            '3a8': 'DelubrumReginae', '3a9': 'DelubrumReginaeSavage', '335': 'DohnMheg', '294': 'DomaCastle',
            '2ca': 'DragonSound', '273': 'DunScaith', 'ab': 'DzemaelDarkhold', '98': 'EastShroud',
            '89': 'EasternLaNoscea', '91': 'EasternThanalan', '352': 'EdensGateDescent',
            '356': 'EdensGateDescentSavage', '353': 'EdensGateInundation', '357': 'EdensGateInundationSavage',
            '351': 'EdensGateResurrection', '355': 'EdensGateResurrectionSavage', '354': 'EdensGateSepulture',
            '358': 'EdensGateSepultureSavage', '3b0': 'EdensPromiseAnamorphosis',
            '3b4': 'EdensPromiseAnamorphosisSavage', '3b1': 'EdensPromiseEternity', '3b5': 'EdensPromiseEternitySavage',
            '3af': 'EdensPromiseLitany', '3b3': 'EdensPromiseLitanySavage', '3ae': 'EdensPromiseUmbra',
            '3b2': 'EdensPromiseUmbraSavage', '386': 'EdensVerseFulmination', '38a': 'EdensVerseFulminationSavage',
            '387': 'EdensVerseFuror', '38b': 'EdensVerseFurorSavage', '388': 'EdensVerseIconoclasm',
            '38c': 'EdensVerseIconoclasmSavage', '389': 'EdensVerseRefulgence', '38d': 'EdensVerseRefulgenceSavage',
            '2cf': 'Emanation', '2d0': 'EmanationExtreme', '301': 'EmissaryOfTheDawn', '21d': 'EngageMultipleTargets',
            '334': 'Eulmore', '21b': 'ExecuteAComboInBattle', '21a': 'ExecuteAComboToIncreaseEnmity',
            '21e': 'ExecuteARangedAttackToIncreaseEnmity', '3a4': 'FadedMemories', '228': 'FinalExercise',
            '3bb': 'FitForAQueen', 'db': 'FlickingSticksAndTakingNames', '1a2': 'Foundation',
            '33f': 'FourPlayerMahjongQuickMatchKuitanDisabled', 'a2': 'Halatali', '168': 'HalataliHard',
            'a6': 'HaukkeManor', '15e': 'HaukkeManorHard', '225': 'HealAnAlly', '226': 'HealMultipleAllies',
            '303': 'HeavenOnHighFloors11_20', '302': 'HeavenOnHighFloors1_10', '304': 'HeavenOnHighFloors21_30',
            '30e': 'HeavenOnHighFloors31_40', '305': 'HeavenOnHighFloors41_50', '30f': 'HeavenOnHighFloors51_60',
            '306': 'HeavenOnHighFloors61_70', '310': 'HeavenOnHighFloors71_80', '307': 'HeavenOnHighFloors81_90',
            '311': 'HeavenOnHighFloors91_100', '32a': 'HellsKier', '32b': 'HellsKierExtreme', '2e6': 'HellsLid',
            'd8': 'HeroOnTheHalfShell', '317': 'HiddenGorge', '345': 'HolminsterSwitch', '169': 'HullbreakerIsle',
            '22d': 'HullbreakerIsleHard', '1de': 'Idyllshire', '330': 'IlMheg', '2c1': 'InThalsName',
            '224': 'InteractWithTheBattlefield', '2b2': 'InterdimensionalRift', '299': 'ItsProbablyATrap',
            '32e': 'Kholusia', '274': 'Kugane', '296': 'KuganeCastle', '326': 'KuganeOhashi', '32d': 'Lakeland',
            '35b': 'LegendOfTheNotSoHiddenTemple', '81': 'LimsaLominsaLowerDecks', '80': 'LimsaLominsaUpperDecks',
            '12a': 'LongLiveTheQueen', '1fa': 'LovmMasterTournament', '24f': 'LovmPlayerBattleNonRp',
            '24d': 'LovmPlayerBattleRp', '24e': 'LovmTournament', '87': 'LowerLaNoscea', '344': 'MalikahsWell',
            '3a5': 'MatoyasRelict', '2c6': 'MatsubaMayhem', '391': 'MemoriaMiseraExtreme', '342': 'MessengerOfTheWinds',
            '86': 'MiddleLaNoscea', '88': 'Mist', '9c': 'MorDhona', 'dd': 'MoreThanAFeeler', '336': 'MtGulg',
            '2b0': 'Naadam', '1a4': 'Neverreap', '84': 'NewGridania', '9a': 'NorthShroud', '93': 'NorthernThanalan',
            '36c': 'NyelbertsLament', '384': 'OceanFishing', '85': 'OldGridania', '250': 'OneLifeForOneWorld',
            '378': 'OnsalHakairDanshigNaadam', '2cc': 'OurCompromise', '2d2': 'OurUnsungHeroes', 'b4': 'OuterLaNoscea',
            'a0': 'PharosSirius', '1fe': 'PharosSiriusHard', 'bf': 'PullingPoisonPosies', '2c2': 'RaisingTheSword',
            '193': 'ReturnOfTheBull', '27b': 'RhalgrsReach', '1ff': 'SaintMociannesArboretum',
            '314': 'SaintMociannesArboretumHard', '9d': 'Sastasha', '183': 'SastashaHard', '1af': 'SealRockSeize',
            'df': 'ShadowAndClaw', '268': 'ShisuiOfTheVioletTides', '2ec': 'SigmascapeV10',
            '2f0': 'SigmascapeV10Savage', '2ed': 'SigmascapeV20', '2f1': 'SigmascapeV20Savage', '2ee': 'SigmascapeV30',
            '2f2': 'SigmascapeV30Savage', '2ef': 'SigmascapeV40', '2f3': 'SigmascapeV40Savage', '173': 'Snowcloak',
            '1b9': 'SohmAl', '269': 'SohmAlHard', '22b': 'SohrKhai', '12c': 'SolemnTrinity', '99': 'SouthShroud',
            '92': 'SouthernThanalan', '161': 'SpecialEventI', '162': 'SpecialEventIi', '1fd': 'SpecialEventIii',
            'c0': 'StingingBack', '174': 'SyrcusTower', '1b3': 'TheAery', '1b6': 'TheAetherochemicalResearchFacility',
            '17a': 'TheAkhAfahAmphitheatreExtreme', '179': 'TheAkhAfahAmphitheatreHard',
            '3a2': 'TheAkhAfahAmphitheatreUnreal', '204': 'TheAntitower', '22e': 'TheAquapolis', 'ac': 'TheAurumVale',
            '26e': 'TheAzimSteppe', '2c7': 'TheBattleOnBekko', 'f1': 'TheBindingCoilOfBahamutTurn1',
            'f2': 'TheBindingCoilOfBahamutTurn2', 'f3': 'TheBindingCoilOfBahamutTurn3',
            'f4': 'TheBindingCoilOfBahamutTurn4', 'f5': 'TheBindingCoilOfBahamutTurn5',
            '178': 'TheBorderlandRuinsSecure', 'ca': 'TheBowlOfEmbers', '127': 'TheBowlOfEmbersExtreme',
            '124': 'TheBowlOfEmbersHard', '38f': 'TheBozjaIncident', '398': 'TheBozjanSouthernFront', '315': 'TheBurn',
            '316': 'TheCalamityRetold', '279': 'TheCarteneauFlatsHeliodrome', '1aa': 'TheChrysalis',
            '190': 'TheChurningMists', '372': 'TheCopiedFactory', '34e': 'TheCrownOfTheImmaculate',
            '350': 'TheCrownOfTheImmaculateExtreme', '333': 'TheCrystarium', '34d': 'TheDancingPlague',
            '35a': 'TheDancingPlagueExtreme', '3a1': 'TheDiadem', '385': 'TheDiadem521', '200': 'TheDiademEasy',
            '203': 'TheDiademHard', '271': 'TheDiademHuntingGrounds', '270': 'TheDiademHuntingGroundsEasy',
            '276': 'TheDiademTrialsOfTheFury', '290': 'TheDiademTrialsOfTheMatron', '2f7': 'TheDomanEnclave',
            '8e': 'TheDragonsNeck', '18e': 'TheDravanianForelands', '18f': 'TheDravanianHinterlands',
            '2db': 'TheDrownedCityOfSkalla', '36f': 'TheDungeonsOfLyheGhiah', '1b2': 'TheDuskVigil',
            '34f': 'TheDyingGasp', '377': 'TheEpicOfAlexanderUltimate', '2c5': 'TheFaceOfTrueEvil',
            '2ff': 'TheFeastCustomMatchCrystalTower', '26b': 'TheFeastCustomMatchFeastingGrounds',
            '286': 'TheFeastCustomMatchLichenweed', '2fd': 'TheFeastRanked', '2e9': 'TheFeastTeamRanked',
            '2fe': 'TheFeastTraining', '22a': 'TheFieldsOfGloryShatter', 'c1': 'TheFinalCoilOfBahamutTurn1',
            'c2': 'TheFinalCoilOfBahamutTurn2', 'c3': 'TheFinalCoilOfBahamutTurn3', 'c4': 'TheFinalCoilOfBahamutTurn4',
            '22f': 'TheFinalStepsOfFaith', '2dc': 'TheForbiddenLandEurekaAnemos',
            '33b': 'TheForbiddenLandEurekaHydatos', '2fb': 'TheForbiddenLandEurekaPagos',
            '31b': 'TheForbiddenLandEurekaPyros', '1ae': 'TheFractalContinuum', '2e7': 'TheFractalContinuumHard',
            '264': 'TheFringes', '319': 'TheGhimlytDark', '374': 'TheGrandCosmos', '1a0': 'TheGreatGubalLibrary',
            '242': 'TheGreatGubalLibraryHard', '2f9': 'TheGreatHunt', '2fa': 'TheGreatHuntExtreme',
            '3ba': 'TheGreatShipVylbrand', '369': 'TheHardenedHeart', '23b': 'TheHauntedManor',
            '2ce': 'TheHeartOfTheProblem', '394': 'TheHeroesGauntlet', '2d5': 'TheHiddenCanalsOfUznair',
            'd0': 'TheHowlingEye', '129': 'TheHowlingEyeExtreme', '126': 'TheHowlingEyeHard', '36b': 'TheHuntersLegacy',
            '2ea': 'TheJadeStoa', '2f6': 'TheJadeStoaExtreme', '96': 'TheKeeperOfTheLake',
            'ae': 'TheLabyrinthOfTheAncients', '1bf': 'TheLimitlessBlueExtreme', '1b4': 'TheLimitlessBlueHard',
            '26d': 'TheLochs', '36a': 'TheLostAndTheFound', '2c8': 'TheLostCanalsOfUznair',
            '16b': 'TheLostCityOfAmdapor', '207': 'TheLostCityOfAmdaporHard', '375': 'TheMinstrelsBalladHadessElegy',
            '236': 'TheMinstrelsBalladNidhoggsRage', '2da': 'TheMinstrelsBalladShinryusDomain',
            '1c0': 'TheMinstrelsBalladThordansReign', '30b': 'TheMinstrelsBalladTsukuyomisPain',
            '15c': 'TheMinstrelsBalladUltimasBane', 'ce': 'TheNavel', '128': 'TheNavelExtreme', '125': 'TheNavelHard',
            '3b9': 'TheNavelUnreal', '33a': 'TheOrbonneMonastery', '2cb': 'TheOrphansAndTheBrokenBlade',
            '256': 'ThePalaceOfTheDeadFloors101_110', '257': 'ThePalaceOfTheDeadFloors111_120',
            '232': 'ThePalaceOfTheDeadFloors11_20', '258': 'ThePalaceOfTheDeadFloors121_130',
            '259': 'ThePalaceOfTheDeadFloors131_140', '25a': 'ThePalaceOfTheDeadFloors141_150',
            '25b': 'ThePalaceOfTheDeadFloors151_160', '25c': 'ThePalaceOfTheDeadFloors161_170',
            '25d': 'ThePalaceOfTheDeadFloors171_180', '25e': 'ThePalaceOfTheDeadFloors181_190',
            '25f': 'ThePalaceOfTheDeadFloors191_200', '231': 'ThePalaceOfTheDeadFloors1_10',
            '233': 'ThePalaceOfTheDeadFloors21_30', '234': 'ThePalaceOfTheDeadFloors31_40',
            '235': 'ThePalaceOfTheDeadFloors41_50', '251': 'ThePalaceOfTheDeadFloors51_60',
            '252': 'ThePalaceOfTheDeadFloors61_70', '253': 'ThePalaceOfTheDeadFloors71_80',
            '254': 'ThePalaceOfTheDeadFloors81_90', '255': 'ThePalaceOfTheDeadFloors91_100', '26c': 'ThePeaks',
            '1a3': 'ThePillars', '2a2': 'ThePoolOfTribute', '2a5': 'ThePoolOfTributeExtreme', 'e0': 'ThePraetorium',
            '395': 'ThePuppetsBunker', '337': 'TheQitanaRavel', '331': 'TheRaktikaGreatwood', '2ac': 'TheResonant',
            '308': 'TheRidoranaLighthouse', '2de': 'TheRoyalCityOfRabanastre', '2a7': 'TheRoyalMenagerie',
            '265': 'TheRubySea', '191': 'TheSeaOfClouds', '39a': 'TheSeatOfSacrifice',
            '39b': 'TheSeatOfSacrificeExtreme', '17c': 'TheSecondCoilOfBahamutSavageTurn1',
            '17d': 'TheSecondCoilOfBahamutSavageTurn2', '17e': 'TheSecondCoilOfBahamutSavageTurn3',
            '17f': 'TheSecondCoilOfBahamutSavageTurn4', '163': 'TheSecondCoilOfBahamutTurn1',
            '164': 'TheSecondCoilOfBahamutTurn2', '165': 'TheSecondCoilOfBahamutTurn3',
            '166': 'TheSecondCoilOfBahamutTurn4', '31a': 'TheShiftingAltarsOfUznair',
            '39c': 'TheShiftingOubliettesOfLyheGhiah', '1b5': 'TheSingularityReactor', '272': 'TheSirensongSea',
            '8f': 'TheStepsOfFaith', 'a8': 'TheStoneVigil', '16d': 'TheStoneVigilHard', '177': 'TheStrikingTreeExtreme',
            '176': 'TheStrikingTreeHard', 'a3': 'TheSunkenTempleOfQarn', '16f': 'TheSunkenTempleOfQarnHard',
            '300': 'TheSwallowsCompass', 'a4': 'TheTamTaraDeepcroft', '175': 'TheTamTaraDeepcroftHard',
            '332': 'TheTempest', '297': 'TheTempleOfTheFist', 'a9': 'TheThousandMawsOfTotoRak',
            '243': 'TheTripleTriadBattlehall', '348': 'TheTwinning', '2dd': 'TheUnendingCoilOfBahamutUltimate',
            '2e5': 'TheValentionesCeremony', '1a5': 'TheVault', '1fc': 'TheVoidArk', '9f': 'TheWanderersPalace',
            'bc': 'TheWanderersPalaceHard', '309': 'TheWeaponsRefrainUltimate', '22c': 'TheWeepingCityOfMhach',
            '167': 'TheWhorleaterExtreme', '119': 'TheWhorleaterHard', '31d': 'TheWillOfTheMoon',
            '97': 'TheWorldOfDarkness', '338': 'TheWreathOfSnakes', '339': 'TheWreathOfSnakesExtreme',
            '1be': 'ThokAstThokExtreme', '1b0': 'ThokAstThokHard', '16c': 'ThornmarchExtreme', 'cf': 'ThornmarchHard',
            '3ad': 'TripleTriadInvitationalParlor', '3ac': 'TripleTriadOpenTournament', '82': 'UldahStepsOfNald',
            '83': 'UldahStepsOfThal', 'be': 'UnderTheArmor', '8b': 'UpperLaNoscea', '18a': 'UrthsFount',
            '37d': 'VowsOfVirtueDeedsOfCruelty', '12b': 'WardUp', '8a': 'WesternLaNoscea', '8c': 'WesternThanalan',
            '2d3': 'WhenClansCollide', '2c3': 'WithHeartAndSteel', 'fa': 'WolvesDenPier', '23c': 'Xelphatol',
            '266': 'Yanxia'}
