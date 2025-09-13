from picosdk.ps3000a import ps3000a as ps
from ctypes import byref, c_int16

status = {}
chandle = c_int16()

# Próba otwarcia pierwszego dostępnego urządzenia
status["openunit"] = ps.ps3000aOpenUnit(byref(chandle), None)

if status["openunit"] == 0:
    print("✅ Oscyloskop został wykryty! Handle =", chandle.value)
    ps.ps3000aCloseUnit(chandle)  # zamykamy połączenie
else:
    print("❌ Brak urządzenia lub błąd. Kod błędu:", status["openunit"])
