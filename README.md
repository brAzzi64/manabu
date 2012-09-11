Bun
---

A new approach for a Japanese language learning aid application.

The backend, written in Python using Django, grabs sentences for a given Kanji from Jisho.org and Tatoeba.org through scraping using PyQuery. Then it joins this data with the pronunciations for each ocurring Kanjis, taken from KanjiDic, and feeds it to the UI (HTML/CSS, JQuery, JavaScript, AJAX, Bootstrap). There the sentence is displayed for the user to learn, disect, and understand, manually chosing to store it, after fixing some possible errors, for later review. Each new scraped sentence is restricted to the Kanjis that the user already knows, plus the newly learnt Kanji.

Deployed in: http://pacific-castle-4908.herokuapp.com/bun

