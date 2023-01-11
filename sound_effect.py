from gtts import gTTS
import numpy as np
import os

text1 = "good"
text2 = "bad"

language = "en"

myobj1 = gTTS(text=text1, lang=language, slow=False)
myobj1.save("good.mp3")

myobj2 = gTTS(text=text2, lang=language, slow=False)
myobj2.save("bad.mp3")

os.system("mpg123 good.mp3")