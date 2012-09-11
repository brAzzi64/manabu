delete from bun_kanji_pronunciations;
delete from bun_kanji;
delete from bun_pronunciation;

select * from bun_kanji;
select * from bun_pronunciation;
select * from bun_kanji_pronunciations;

select * from bun_kanji_pronunciations where pronunciation_id = 1

select k.character, p.text
from bun_kanji k, bun_pronunciation p, bun_kanji_pronunciations kp
where k.id = kp.kanji_id and kp.pronunciation_id = p.id and k.character = '私' and p.ptype = 'KN'
