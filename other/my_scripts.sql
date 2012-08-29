delete from kanjidic_kanji_pronunciations;
delete from kanjidic_kanji;
delete from kanjidic_pronunciation;

select * from kanjidic_kanji;
select * from kanjidic_pronunciation;
select * from kanjidic_kanji_pronunciations;

select * from kanjidic_kanji_pronunciations where pronunciation_id = 1

select k.character, p.text
from kanjidic_kanji k, kanjidic_pronunciation p, kanjidic_kanji_pronunciations kp
where k.id = kp.kanji_id and kp.pronunciation_id = p.id and k.character = '私' and p.ptype = 'KN'