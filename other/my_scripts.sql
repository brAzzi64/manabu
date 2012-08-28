delete from kdic_kanji_pronunciations;
delete from kdic_kanji;
delete from kdic_pronunciation;

select * from kdic_kanji;
select * from kdic_pronunciation;
select * from kdic_kanji_pronunciations;

select * from kdic_kanji_pronunciations where pronunciation_id = 1

select k.character, p.text
from kdic_kanji k, kdic_pronunciation p, kdic_kanji_pronunciations kp
where k.id = kp.kanji_id and kp.pronunciation_id = p.id and k.character = '私' and p.ptype = 'KUN'