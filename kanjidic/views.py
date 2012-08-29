from django.shortcuts import render_to_response
from kanjidic.models import Kanji

def index(request):
    return render_to_response('kanjidic/index.html')

def kanji(request, kanji):
    try:
        k = Kanji.objects.get(character = kanji)
        onyomis =  [p.text for p in k.pronunciations.all() if p.ptype == u'ON']
        kunyomis = [p.text for p in k.pronunciations.all() if p.ptype == u'KN']
        data = {'character' : k.character, 'onyomis' : onyomis, 'kunyomis' : kunyomis}
    except Kanji.DoesNotExist:
        raise Http404
    return render_to_response('kanjidic/kanji.html', {'kanji' : data})

