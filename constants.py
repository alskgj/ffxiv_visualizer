from datetime import timedelta

ACTOR_CONTROL_LINES = 33
INSTANCED = 8003
ACTOR_CONTROL_LINES_WIPE = 40000005
NetworkAbility = 21  # 0x15

# phases - always until
enrage_time_twintania = timedelta(minutes=3, seconds=3)
enrage_time_nael = enrage_time_twintania + timedelta(minutes=3, seconds=25)
enrage_time_bahamut_prime = enrage_time_nael + timedelta(minutes=5, seconds=34)
enrage_time_nael_twintania = enrage_time_bahamut_prime + timedelta(minutes=2, seconds=19)
enrage_time_gold_bahamut = enrage_time_nael_twintania + timedelta(minutes=3, seconds=29)
