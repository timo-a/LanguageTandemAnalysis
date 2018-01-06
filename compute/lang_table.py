import pycountry
import gettext

lang_table= { 'ara':['Arabisch'],
              'ary':['Moroccan','Marokkanisch'],
              'arz':['Ägyptisch'],
              'bel':['Weißrussisch'],
              'bul':['Bulgarisch'],
              'cat':['Katalanisch'],
              'cmn':['Mandarin'],
              'deu':['Deutsch','deutsch','Detusch','Allemand'],
              'ell':['Griechisch'],
              'eng':['Englisch','English','english'],
              'fas':['Farsisch', 'Persian','Persisch'],
              'fra':['Französisch', 'Franzöisch','Français'],
              'hak':['Hakka'],
              'hin':['Hindi'],
              'hun':['Ungarisch'],
              'hrv':['Kroatisch'],
              'ind':['Indonesisch'],
              'isl':['Icelandic','Isländisch'],
              'ita':['Italienisch'],
              'jpn':['Japanisch','Japanese','日本語'],
              'kok':['Konkani'],
              'kor':['Koreanisch'],
              'lit':['Litauisch'],
              'msa':['Malayalam'],
              'mon':['Mongolisch'],
              'nan':['Taiwanesisch'],
              'nld':['Niederländisch'],
              'nor':['Norwegisch'],
              'pol':['Polnisch'],
              'por':['Portugiesisch','Portugesisch','Brasilianisches Portugiesisch'],
              'ron':['Rumänisch'],
              'rus':['Russisch','Ruschisch'],
              'spa':['Spanisch','Spanish'],
              'srp':['Serbian','Serbisch'],
              'swa':['Swahili'],
              'swe':['Schwedisch'],
              'tha':['Thailändisch','Thai','thaländisch'],
              'tur':['Türkisch'],
              'ukr':['Ukrainisch'],
              'vie':['Vietnamesisch','Vietnamesich'],
              'yue':['Kantonesisch'],
              'zho':['Chinesisch','chinese','Chinesish'],
             }

lang_dict = {}
for abbrev,list_ in lang_table.items():
    for l in list_:
        lang_dict[l]= abbrev

def code_to_language(code):
    lang = pycountry.languages.get(alpha_3=code).name
    cleaned = lang.split('(')[0].strip() # split away '(makrolanguage)'
    return cleaned
"""
bsp
> german = gettext.translation('iso639-3', pycountry.LOCALES_DIR, languages=['de'])
> german.install()
> _('Mandarin Chinese')
'Mandarin-Chinesisch'

"""
