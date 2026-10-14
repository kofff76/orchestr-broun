from pathlib import Path
from PIL import Image
import os, math, html, json, shutil, zipfile, textwrap
P=Path(__file__).resolve().parents[1]; P.mkdir(exist_ok=True)
I=P/'assets'/'images'; I.mkdir(parents=True,exist_ok=True)
src=P/'source_images' # optional folder for replacement PNG sources
images={
'orchestra':'a_wide_cinematic_high_resolution_photo_realistic_1.png',
'conductor':'a_cinematic_high_end_photorealistic_portrait_sce_2_batch_1.png',
'first-violins':'a_cinematic_high_end_realistic_photo_portrait_st_3_batch_2.png',
'second-violins':'a_luxurious_cinematic_photorealistic_portrait_st_4_batch_3.png',
'violin-solo':'an_ornate_cinematic_photorealistic_portrait_styl_5_batch_4.png',
'violins':'a_luxurious_cinematic_photorealistic_portrait_st_6_batch_5.png',
'cellos':'an_opulent_cinematic_photorealistic_scene_in_a_l_7_batch_6.png',
'basses':'an_opulent_cinematic_high_resolution_photoreali_8_batch_7.png',
'woodwinds':'wide_vertical_cinematic_high_resolution_photogr_9_batch_8.png',
'percussion':'a_grand_cinematic_photorealistic_concert_hall_po_10_batch_9.png',
'about':'a_wide_cinematic_high_detail_collage_photomontag_1_batch_1.png',
'press':'a_cinematic_collage_montage_in_a_classical_vintag_2_batch_2.png',
'photos':'a_wide_cinematic_collage_style_image_with_no_text_3_batch_3.png',
'videos':'a_cinematic_sepia_gold_black_and_white_and_warm_4_batch_4.png',
'concerts':'a_rich_cinematic_collage_style_illustration_with_a_5_batch_5.png'
}
manifest={}
for key,file in images.items():
 inp=src/file
 out=I/(key+'.webp')
 if inp.exists():
  im=Image.open(inp).convert('RGB')
  im.save(out,'WEBP',quality=82,method=6)
 elif out.exists():
  im=Image.open(out)
 else: raise FileNotFoundError(f'Missing source {inp} and optimized asset {out}')
 manifest[key]={'source':file,'webp':f'assets/images/{key}.webp','size': list(im.size), 'bytes':out.stat().st_size}
print('Images optimized',sum(i['bytes'] for i in manifest.values())/1e6, 'MB')
(P/'assets'/'image-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')

# convenience
sections=[
 dict(slug='first-violins',name='Первые скрипки',en='First violins',image='first-violins',desc='Ведущая мелодическая линия, точность интонации и единое дыхание оркестровой ткани.',person='Концертмейстер — имя будет добавлено'),
 dict(slug='second-violins',name='Вторые скрипки',en='Second violins',image='second-violins',desc='Внутренняя энергия струнной партитуры, взаимодействие голосов и богатство тембров.',person='Руководитель группы — имя будет добавлено'),
 dict(slug='strings',name='Струнная группа',en='String section',image='violins',desc='Звуковой фундамент симфонического состава: пластичность фразы и динамическая глубина.',person='Состав будет добавлен'),
 dict(slug='cellos',name='Виолончели',en='Cellos',image='cellos',desc='Благородный тембр, лирическая выразительность и насыщенный оркестровый регистр.',person='Руководитель группы — имя будет добавлено'),
 dict(slug='basses',name='Контрабасы',en='Double basses',image='basses',desc='Низкие частоты и основа гармонической архитектуры большого симфонического звучания.',person='Руководитель группы — имя будет добавлено'),
 dict(slug='woodwinds',name='Деревянные духовые',en='Woodwinds',image='woodwinds',desc='Флейта, гобой, кларнет и фагот — голос индивидуального тембра внутри симфонического полотна.',person='Солисты группы — имена будут добавлены'),
 dict(slug='percussion',name='Ударные',en='Percussion',image='percussion',desc='Ритмический рельеф, тембровые акценты и драматургические кульминации партитуры.',person='Руководитель группы — имя будет добавлено'),
]
concerts=[
 dict(slug='mahler-symphony-2',composer='Густав Малер',short='Малер',work='Симфония № 2',subtitle='«Воскресение»',en='Mahler · Symphony No. 2',image='concerts',code='01',tag='Симфонический вечер',desc='Масштабная симфоническая фреска о человеческой судьбе, надежде и преображении. Программа представлена как демонстрационный пример.',detail='Пять частей, вокальные партии и монументальный финал. Исполнительский состав и дата будут уточнены.'),
 dict(slug='mozart-symphony-40',composer='Вольфганг Амадей Моцарт',short='Моцарт',work='Симфония № 40',subtitle='Соль минор, K. 550',en='Mozart · Symphony No. 40',image='about',code='02',tag='Классический репертуар',desc='Одно из самых узнаваемых произведений венского классицизма: ясная форма и необычайная драматическая напряжённость.',detail='Форма, прозрачная оркестровка и исключительная выразительность тем определяют художественный облик программы.'),
 dict(slug='rachmaninoff-piano-2',composer='Сергей Рахманинов',short='Рахманинов',work='Концерт для фортепиано с оркестром № 2',subtitle='До минор, соч. 18',en='Rachmaninoff · Piano Concerto No. 2',image='videos',code='03',tag='Фортепиано и оркестр',desc='Романтический размах, лирическая интонация и виртуозное соединение солиста с оркестром.',detail='В программе — фортепианный концерт, соч. 18. Имя солиста, дирижёра и детали площадки уточняются.'),
]
# relative helpers

def href(path,depth=0):
 pre='../'*depth
 if path in ('','/') : return pre+'index.html'
 if path.startswith('#'): return path
 return pre+path.strip('/')+'/index.html'

def im(key,depth=0):return '../'*depth+f'assets/images/{key}.webp'
def esc(s):return html.escape(str(s),quote=True)
def btn(label,path,depth=0,variant='line',extra=''):
 return f'<a class="button button--{variant}" href="{href(path,depth)}" {extra}><span>{label}</span><span class="button__arrow" aria-hidden="true">↗</span></a>'

def pic(key,alt,depth=0,extra='',load='lazy'):
 return f'<img src="{im(key,depth)}" alt="{esc(alt)}" loading="{load}" decoding="async" {extra}>'

def kicker(ru,en=''):
 return f'<p class="eyebrow"><span class="eyebrow__rule"></span>{ru}<span class="eyebrow__en">{en}</span></p>'

def title(ru,en=''):
 return f'<div class="section-heading">{kicker('РАЗДЕЛ',en)}<h2>{ru}</h2></div>'

def poster(c,depth=0,large=False,with_btn=True):
 cls='programme-poster programme-poster--large' if large else 'programme-poster'
 small=f'<div class="programme-poster__eyebrow">VALLEYS <span>·</span> SYMPHONY</div>'
 return f'''<div class="{cls}" style="--poster-image:url('{im(c['image'],depth)}')">
 <div class="programme-poster__top">{small}<span>{c['code']} / 03</span></div>
 <div class="programme-poster__body"><span class="programme-poster__seal">V / S</span><p>{c['composer']}</p><h3>{c['work']}</h3><em>{c['subtitle']}</em></div>
 <div class="programme-poster__bottom"><span>СИМФОНИЧЕСКИЙ СЕЗОН</span><span>VALLEYS</span></div></div>'''

def concertcard(c,depth=0):
 return f'''<article class="concert-card reveal"><a class="concert-card__visual" href="{href('concerts/'+c['slug'],depth)}" aria-label="Подробнее: {esc(c['composer'])}, {esc(c['work'])}">{poster(c,depth)}</a>
 <div class="concert-card__meta"><span>Дата уточняется</span><span>{c['tag']}</span></div><h3>{c['composer']}<br><em>{c['work']}</em></h3>
 <div class="concert-card__actions">{btn('Подробнее','concerts/'+c['slug'],depth)}<span class="muted-label">БИЛЕТЫ ПОЗЖЕ</span></div></article>'''

def feature(sec,depth=0):
 return f'''<a class="instrument-card reveal" href="{href('musicians/'+sec['slug'],depth)}">
 <div class="instrument-card__image">{pic(sec['image'],sec['name']+' на концертной сцене',depth)}</div><div class="instrument-card__content"><span>{sec['en']}</span><h3>{sec['name']}</h3><span class="instrument-card__arrow" aria-hidden="true">↗</span></div></a>'''

def pagehero(heading,en,key,depth=0,small=''):
 return f'''<section class="page-hero"><div class="page-hero__image">{pic(key,'Художественный коллаж с фрагментами симфонической жизни',depth,load='eager')}</div><div class="page-hero__shade"></div>
 <div class="page-hero__content container">{kicker('VALLEYS SYMPHONY ORCHESTRA',en)}<h1>{heading}</h1><p>{small}</p></div><div class="page-hero__index">V / S &nbsp; — &nbsp; 2026</div></section>'''

def statstrip():
 return '''<div class="statistics"><div><strong>120<span class="gold">*</span></strong><small>МУЗЫКАНТОВ <span>· MUSICIANS</span></small></div><div><strong>150<span class="gold">*</span></strong><small>ЛЕТ ОПЫТА <span>· YEARS OF EXPERIENCE</span></small></div><div><strong>50+<span class="gold">*</span></strong><small>КОНЦЕРТОВ <span>· CONCERTS</span></small></div></div><p class="demo-note">* Демонстрационные показатели. Замените на реальные данные оркестра.</p>'''

menu=[('Об оркестре','about'),('Дирижёр','conductor'),('Состав','musicians'),('Афиша','concerts'),('Медиа','media'),('Записи','recordings'),('Студия','production'),('Контакты','contacts')]

def header(depth=0,current=''):
 links=''.join(f'<a class="nav-link {"is-current" if current==path else ""}" href="{href(path,depth)}">{name}</a>' for name,path in menu)
 return f'''<header class="site-header" id="site-header"><div class="site-header__inner">
 <a href="{href('/',depth)}" class="site-logo" aria-label="Valleys Symphony Orchestra — на главную"><span class="site-logo__mark">V<span>·</span>S</span><span class="site-logo__letters">VALLEYS <small>SYMPHONY ORCHESTRA</small></span></a>
 <nav class="desktop-nav" aria-label="Основная навигация">{links}</nav>
 <a class="group-mark" href="{href('partners',depth)}" title="Valleys Cultural Group"><span>VALLEYS</span><small>CULTURAL GROUP</small></a>
 <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="mobile-navigation" aria-label="Открыть меню"><span></span><span></span></button></div>
 <nav class="mobile-nav" id="mobile-navigation" aria-label="Мобильное меню" hidden>{links}<div class="mobile-nav__secondary"><a href="{href('partners',depth)}">Партнёры</a><a href="{href('media/press',depth)}">Пресса</a><a href="{href('media/photos',depth)}">Фото</a><a href="{href('media/videos',depth)}">Видео</a></div></nav></header>'''

def footer(depth=0):
 return f'''<footer class="site-footer" id="footer"><div class="container"><div class="footer-top"><div><span class="footer-pretitle">VALLEYS CULTURAL GROUP</span><h2>Музыка.<br><em>Вне времени.</em></h2><p>Music beyond time.</p></div><div class="footer-columns"><div><h3>НАВИГАЦИЯ</h3><a href="{href('about',depth)}">Об оркестре</a><a href="{href('musicians',depth)}">Состав</a><a href="{href('concerts',depth)}">Афиша</a><a href="{href('media',depth)}">Медиатека</a></div><div><h3>ПРОЕКТЫ ГРУППЫ</h3><a href="{href('production',depth)}">Creative Development Studio</a><a href="{href('partners',depth)}#ecosystem">The Valleys Musical Agency</a><a href="{href('partners',depth)}#ecosystem">Opera Professional</a><a href="{href('contacts',depth)}">Сотрудничество</a></div></div></div>
 <div class="footer-bottom"><span>Проект Valleys Cultural Group. © 2024 <span class="demo-label">· Демонстрационный сайт</span></span><span>VALLEYS SYMPHONY ORCHESTRA</span><a href="{href('/',depth)}">НАВЕРХ ↑</a></div></div></footer>'''

def shell(content,page,depth=0,current='',description='Премиальный демонстрационный сайт симфонического оркестра Valleys Symphony Orchestra.'):
 return f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#080808"><meta name="description" content="{esc(description)}"><title>{esc(page)} — Valleys Symphony Orchestra</title><link rel="icon" href="{'../'*depth}assets/favicon.svg" type="image/svg+xml"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400;1,500&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet"><link rel="stylesheet" href="{'../'*depth}assets/css/site.css"><script defer src="{'../'*depth}assets/js/site.js"></script></head><body data-page="{esc(current)}">{header(depth,current)}<main id="main">{content}</main>{footer(depth)}<div id="site-toast" class="site-toast" role="status" aria-live="polite"></div></body></html>'''

def save(route,html_content):
 path=P/route/'index.html' if route else P/'index.html'
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(html_content,encoding='utf-8')

# Home
home=f'''<section class="home-hero"><div class="home-hero__image">{pic('orchestra','Симфонический оркестр на сцене роскошного исторического зала',0,load='eager')}</div><div class="home-hero__screen"></div>
 <div class="home-hero__frame container"><div class="hero__eyebrow reveal">VALLEYS CULTURAL GROUP <span> / </span> THE SYMPHONY COLLECTION</div><h1 class="hero-title reveal">Симфонический<br><em>оркестр Valleys</em></h1><p class="hero-subtitle reveal">Искусство, возведённое в абсолют <span>(Art Elevated to Perfection)</span></p><div class="hero-actions reveal">{btn('Программа сезона','concerts',variant='solid')}{btn('Об оркестре','about')}</div></div>
 <div class="home-hero__bottom container"><span>THE ART OF LISTENING</span><span>SCROLL TO EXPLORE <span aria-hidden="true">↓</span></span></div></section>
 <section class="intro-section section-block"><div class="container"><div class="intro-grid"><div>{kicker('01 / НАСЛЕДИЕ','Legacy')}<h2 class="display-heading reveal">Звук,<br><em>который остаётся.</em></h2></div><div class="intro-grid__right"><p class="editorial-lead reveal">Симфоническая традиция раскрывается там, где совершенство исполнения встречается с живой энергией сцены.</p><p>Мы создаём художественную среду, в которой престиж академической музыки соединяется с открытостью новому поколению слушателей.</p>{btn('Философия оркестра','about')}</div></div>{statstrip()}</div></section>
 <section class="director-feature"><div class="director-feature__image">{pic('conductor','Дирижёр в концертном фраке на золочёной сцене')}</div><div class="director-feature__content"><div class="director-feature__inner">{kicker('02 / ХУДОЖЕСТВЕННЫЙ РУКОВОДИТЕЛЬ','Artistic direction')}<h2 class="display-heading">Музыка начинается <em>с жеста.</em></h2><p class="editorial-lead">Диалог дирижёра с оркестром — тонкая архитектура времени, тишины и звучания.</p><p class="muted">Персональные сведения будут добавлены после утверждения состава.</p>{btn('Художественный руководитель','conductor')}</div></div></section>
 <section class="section-block seating-preview"><div class="container">{kicker('03 / АНАТОМИЯ ЗВУКА','Inside the orchestra')}<div class="section-topline"><h2 class="display-heading">Сто двадцать голосов.<br><em>Единое целое.</em></h2><p>Исследуйте сцену, выбирайте инструментальные группы и знакомьтесь с тембрами симфонического оркестра.</p></div>{'<div data-seating-map></div>'}{btn('Весь состав оркестра','musicians')}</div></section>
 <section class="season-section section-block"><div class="container">{kicker('04 / КОНЦЕРТНЫЙ СЕЗОН','The season')}<div class="section-topline"><h2 class="display-heading">Афиша <em>сезона.</em></h2><p>Избранные произведения симфонической литературы. Демонстрационная программа без назначенных дат.</p></div><div class="concert-grid">{''.join(concertcard(c) for c in concerts)}</div><div class="section-bottom-action">{btn('Полная афиша','concerts',variant='solid')}</div></div></section>
 <section class="media-home section-block"><div class="container">{kicker('05 / ЖИЗНЬ ОРКЕСТРА','Beyond the stage')}<h2 class="display-heading">Сцена. <em>И то, что за ней.</em></h2><div class="media-home__grid">
 <a class="media-home__card media-home__card--wide" href="{href('media/press')}">{pic('press','Безтекстовый коллаж, посвящённый прессе и истории концертных выступлений')}<span><small>01 — PRESS</small><strong>Пресса</strong><i>↗</i></span></a>
 <a class="media-home__card" href="{href('media/photos')}">{pic('photos','Коллаж из фотографий симфонического оркестра')}<span><small>02 — PHOTOGRAPHY</small><strong>Фото</strong><i>↗</i></span></a>
 <a class="media-home__card" href="{href('media/videos')}">{pic('videos','Коллаж из кинематографических кадров и видеокамер')}<span><small>03 — MOVING IMAGE</small><strong>Видео</strong><i>↗</i></span></a></div></div></section>
 <section class="records-home section-block"><div class="container"><div class="split-editorial"><div>{kicker('06 / АУДИОАРХИВ','Recordings')}<h2 class="display-heading">Музыка <em>на века.</em></h2><p>Коллекция записей, изданий и концертных впечатлений. Раздел подготовлен для будущих релизов оркестра.</p>{btn('К каталогу записей','recordings')}</div><div class="vinyl-preview" aria-hidden="true"><div class="vinyl-preview__sleeve">{pic('orchestra','',extra='aria-hidden="true"')}<span>VALLEYS<br><small>THE SYMPHONY EDITIONS</small></span></div><div class="vinyl-preview__disc"><span>VALLEYS<br>33 RPM</span></div></div></div></div></section>
 <section class="studio-home section-block"><div class="studio-home__image">{pic('videos','Кинематографический коллаж оркестрового видеопроизводства')}</div><div class="container studio-home__content">{kicker('07 / CREATIVE DEVELOPMENT STUDIO','The studio')}<h2 class="display-heading">Музыка.<br><em>Новые измерения.</em></h2><p>Промо-ролики, визуальные музыкальные издания и концепции иммерсивных трансляций.</p>{btn('Исследовать студию','production',variant='solid')}</div></section>
 <section class="section-block partner-preview"><div class="container">{kicker('08 / СОТРУДНИЧЕСТВО','Partnerships')}<div class="section-topline"><h2 class="display-heading">Создаём <em>будущее вместе.</em></h2><p>Сотрудничество с филармониями, культурными институциями и партнёрами в области искусства.</p></div><div class="sponsor-letters" aria-label="Категории партнёров"><span>КУЛЬТУРА</span><span>ИСКУССТВО</span><span>НАСЛЕДИЕ</span><span>ИННОВАЦИИ</span></div>{btn('Партнёрские возможности','partners')}</div></section>'''
save('',shell(home,'Главная'))

about=f'''{pagehero('Об оркестре','About the orchestra','about',1,small='Традиция исполнения. Свобода интерпретации. Диалог со временем.')}
<section class="section-block"><div class="container"><div class="editorial-spread"><div>{kicker('НАША ФИЛОСОФИЯ','Our philosophy')}<h2 class="display-heading">Услышать <em>больше.</em></h2></div><div><p class="editorial-lead">Академическая музыка живёт не только в партитуре. Она рождается в пространстве между исполнителем, залом и слушателем.</p><p>Valleys Symphony Orchestra — демонстрационный художественный образ современного симфонического коллектива. Он основан на традиции точного ансамблевого исполнения, культуре звука и уважении к историческому наследию.</p><p>В представлении оркестра важны баланс тембров, акустика и внимательное отношение к каждому музыкальному голосу. Этот сайт подготовлен как редактируемая платформа для реального коллектива.</p></div></div><div class="wide-photograph reveal">{pic('orchestra','Общий портрет оркестра на исторической сцене',1)}</div>{statstrip()}</div></section>
<section class="section-block light-section"><div class="container"><div class="triad-grid"><article><span>01 / TRADITION</span><h3>Традиции</h3><p>Уважение к партитуре, стилю и исполнительской школе.</p></article><article><span>02 / ACOUSTICS</span><h3>Акустика</h3><p>Культура тембрового равновесия и естественного звучания.</p></article><article><span>03 / INNOVATION</span><h3>Инновации</h3><p>Новые технологии как продолжение художественного высказывания.</p></article></div></div></section><section class="section-block"><div class="container"><div class="editorial-spread"><div>{kicker('ХУДОЖЕСТВЕННОЕ РУКОВОДСТВО','Leadership')}<h2 class="display-heading">Искусство <em>управлять тишиной.</em></h2></div><div><p class="editorial-lead">От замысла дирижёра до общего дыхания струнной группы — симфония объединяет множество индивидуальностей.</p>{btn('Знакомство с дирижёром','conductor',1)} {btn('Состав оркестра','musicians',1)}</div></div></div></section>'''
save('about',shell(about,'Об оркестре',1,'about'))

cond=f'''<section class="conductor-hero"><div class="conductor-hero__portrait">{pic('conductor','Дирижёр на сцене в историческом зале',1,load='eager')}</div><div class="conductor-hero__text">{kicker('ХУДОЖЕСТВЕННОЕ РУКОВОДСТВО','The conductor')}<h1>Мастерство<br><em>слышать целое.</em></h1><div class="gold-line"></div><p class="editorial-lead">Дирижёр как носитель музыкальной идеи: от первого жеста до последнего затихающего аккорда.</p><p class="muted">Фотография и биография приведены в качестве демонстрационного наполнения. Имя дирижёра будет добавлено владельцем сайта.</p>{btn('Состав оркестра','musicians',1)}</div></section>
<section class="section-block"><div class="container"><div class="editorial-spread"><div>{kicker('ХУДОЖЕСТВЕННОЕ КРЕДО','Artistic vision')}<h2 class="display-heading">Жест.<br><em>Дыхание. Звук.</em></h2></div><div><p class="editorial-lead">Симфоническое исполнение начинается с внимательного прочтения партитуры и продолжается в живом диалоге музыкантов.</p><p>Здесь будет размещена биография художественного руководителя, перечень его творческих проектов, репертуар и избранные записи.</p>{btn('Афиша концертов','concerts',1)}</div></div></div></section><section class="conductor-strip">{pic('about','Коллаж из театральной архитектуры и концертных фотографий',1)}</section>'''
save('conductor',shell(cond,'Дирижёр',1,'conductor'))

mus=f'''{pagehero('Состав оркестра','Our musicians','about',1,'Индивидуальности, объединённые одним звуком.')}
<section class="section-block"><div class="container">{kicker('ИНТЕРАКТИВНАЯ СЦЕНА','Explore the sections')}<h2 class="display-heading">Архитектура <em>оркестра.</em></h2><p class="lead-short">Выберите инструментальную группу на схеме или в списке. Рассадка иллюстративная и не обозначает фактическую сценическую конфигурацию коллектива.</p><div data-seating-map></div></div></section><section class="section-block instruments-section"><div class="container">{kicker('ГРУППЫ МУЗЫКАНТОВ','Meet the ensemble')}<h2 class="display-heading">Лица и <em>тембры.</em></h2><div class="instrument-grid">{''.join(feature(s,1) for s in sections)}</div><p class="demo-note">Фотографии сгенерированы для демонстрационного сайта. Имена музыкантов не указываются.</p></div></section>'''
save('musicians',shell(mus,'Состав оркестра',1,'musicians'))
for s in sections:
 d=2
 secpage=f'''<section class="instrument-detail"><div class="instrument-detail__picture">{pic(s['image'],s['name']+' — концертная фотография',d,load='eager')}</div><div class="instrument-detail__text">{kicker('СОСТАВ ОРКЕСТРА',s['en'])}<h1>{s['name']}</h1><p class="editorial-lead">{s['desc']}</p><p class="muted">{s['person']}.</p><div class="detail-facts"><div><span>РАЗДЕЛ</span><b>Симфонический оркестр</b></div><div><span>СОСТАВ</span><b>Данные уточняются</b></div></div>{btn('Все инструментальные группы','musicians',d)}</div></section><section class="section-block"><div class="container">{kicker('ВМЕСТЕ НА СЦЕНЕ','The complete ensemble')}<h2 class="display-heading">Единый <em>оркестр.</em></h2><div class="related-grid">{''.join(feature(x,d) for x in sections if x['slug']!=s['slug'])}</div></div></section>'''
 save('musicians/'+s['slug'],shell(secpage,s['name'],d,'musicians'))

concertpage=f'''{pagehero('Афиша','Concert season','concerts',1,'Мир симфонических произведений. Три программы для демонстрации оформления.')}
<section class="section-block"><div class="container">{kicker('ПРОГРАММА','Concert calendar')}<div class="section-topline"><h2 class="display-heading">Звук <em>сезона.</em></h2><p>Программы являются примерами наполнения. Даты, дирижёры, солисты и билеты не назначены.</p></div><div class="concert-controls" id="concert-controls"><label>КОМПОЗИТОР <select id="composer-filter" aria-label="Фильтр концертов по композитору"><option value="all">Все композиторы</option><option value="Малер">Густав Малер</option><option value="Моцарт">Вольфганг Амадей Моцарт</option><option value="Рахманинов">Сергей Рахманинов</option></select></label><div class="view-switch" role="group" aria-label="Вид афиши"><button type="button" class="is-active" data-view="grid" aria-pressed="true">СЕТКА</button><button type="button" data-view="list" aria-pressed="false">СПИСОК</button></div></div><div class="concert-grid" id="concert-grid">{''.join(concertcard(c,1) for c in concerts)}</div><p class="filter-empty" id="filter-empty" hidden>Для выбранного фильтра концерты не найдены.</p></div></section>'''
save('concerts',shell(concertpage,'Афиша',1,'concerts'))
for c in concerts:
 d=2
 detail=f'''<section class="concert-detail"><div class="container concert-detail__grid"><div class="concert-detail__art">{poster(c,d,True)}</div><div class="concert-detail__info">{kicker('КОНЦЕРТНАЯ ПРОГРАММА','Concert programme')}<p class="concert-detail__number">{c['code']} / 03</p><h1>{c['composer']}<br><em>{c['work']}</em></h1><p class="editorial-lead">{c['desc']}</p><div class="detail-facts"><div><span>ДАТА И ВРЕМЯ</span><b>Уточняются</b></div><div><span>МЕСТО ПРОВЕДЕНИЯ</span><b>Будет объявлено</b></div><div><span>ДИРИЖЁР</span><b>Информация появится позднее</b></div><div><span>СОЛИСТЫ</span><b>Состав уточняется</b></div><div><span>ПРОГРАММА</span><b>{c['subtitle']}</b></div></div><div class="detail-buttons"><button type="button" class="button button--solid notify-button" data-toast="Билетная система ещё не подключена. Это демонстрационный сайт."><span>Билеты скоро</span><span class="button__arrow">↗</span></button>{btn('Назад к афише','concerts',d)}</div></div></div></section><section class="section-block light-section"><div class="container"><div class="editorial-spread"><div>{kicker('О ПРОИЗВЕДЕНИИ','About the music')}<h2 class="display-heading">Музыкальная <em>история.</em></h2></div><div><p class="editorial-lead">{c['detail']}</p><p>Материал служит примером для страницы отдельного концерта. После добавления реальной программы здесь могут появиться комментарий дирижёра, состав исполнителей и ссылки на билеты.</p></div></div></div></section>'''
 save('concerts/'+c['slug'],shell(detail,f"{c['composer']} — {c['work']}",d,'concerts'))

mediaitems=[('press','Пресса','Press','media/press','Рецензии, интервью и материалы для СМИ.'),('photos','Фотогалерея','Photography','media/photos','Моменты концертов, репетиций и закулисья.'),('videos','Видео','Film & video','media/videos','Кинематографические истории оркестровой жизни.')]
media=f'''{pagehero('Медиатека','Media library','photos',1,'Художественная жизнь, зафиксированная в изображениях, словах и звуке.')}
<section class="section-block"><div class="container">{kicker('АРХИВ ВПЕЧАТЛЕНИЙ','The collection')}<h2 class="display-heading">За пределами <em>сцены.</em></h2><div class="media-directory">{''.join(f'<a class="media-directory__item reveal" href="{href(path,1)}">{pic(img,name,1)}<span class="media-directory__overlay"><small>{en}</small><strong>{name}</strong><em>{desc}</em><b>↗</b></span></a>' for img,name,en,path,desc in mediaitems)}</div></div></section>'''
save('media',shell(media,'Медиатека',1,'media'))

press=f'''{pagehero('Пресса','Press & reviews','press',2,'Публикации, критический взгляд и разговор об искусстве исполнения.')}
<section class="section-block"><div class="container">{kicker('РЕДАКЦИОННЫЙ АРХИВ','Editorial archive')}<div class="section-topline"><h2 class="display-heading">Искусство <em>в словах.</em></h2><p>Раздел создан как структура для будущих настоящих публикаций. Заглушки не являются цитатами СМИ.</p></div><div class="press-features"><article class="press-feature"><div class="press-feature__photo">{pic('conductor','Дирижёр симфонического оркестра',2)}</div><div><span class="tiny-label">МАТЕРИАЛ ДЛЯ ПУБЛИКАЦИИ / EDITORIAL</span><h3>Разговор об искусстве<br><em>симфонического исполнения.</em></h3><p>Место для большого интервью с художественным руководителем, авторского эссе или критической статьи.</p><span class="muted-label">Публикация ещё не добавлена</span></div></article><div class="press-list"><article><span>01 / INTERVIEW</span><h4>Личность дирижёра и язык оркестра</h4><p>Шаблон интервью · материал отсутствует</p></article><article><span>02 / REVIEWS</span><h4>Критика и концертные рецензии</h4><p>Будущая подборка рецензий с указанием источников</p></article><article><span>03 / JOURNAL</span><h4>Музыка как культурный диалог</h4><p>Редакционные материалы · раздел под наполнением</p></article></div></div></div></section>'''
save('media/press',shell(press,'Пресса',2,'media'))

all_photos=[('orchestra','Оркестр на сцене исторического концертного зала'),('conductor','Портрет дирижёра'),('violins','Группа скрипачей'),('first-violins','Портрет концертмейстера'),('second-violins','Скрипачка во время исполнения'),('violin-solo','Скрипачка на концертной сцене'),('cellos','Виолончельная группа'),('basses','Группа контрабасов'),('woodwinds','Деревянные духовые'),('percussion','Ударная группа'),('about','Художественный симфонический коллаж'),('photos','Коллаж концертных фотографий')]
photos=f'''{pagehero('Фотогалерея','Photography','photos',2,'Люди. Звучание. Пространство.')}
<section class="section-block"><div class="container">{kicker('ВИЗУАЛЬНЫЙ АРХИВ','Through the lens')}<h2 class="display-heading">Музыка <em>в кадре.</em></h2><p class="lead-short">Выберите фотографию, чтобы открыть её в полноэкранном режиме.</p><div class="gallery-grid" id="gallery-grid">{''.join(f'<button class="gallery-tile reveal" type="button" data-lightbox="{idx}" aria-label="Увеличить фото: {esc(alt)}">{pic(key,alt,2)}<span class="gallery-tile__zoom">↗</span></button>' for idx,(key,alt) in enumerate(all_photos))}</div></div></section>
<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Просмотр фотографии" hidden><button class="lightbox__close" type="button" aria-label="Закрыть">×</button><button class="lightbox__prev" type="button" aria-label="Предыдущее фото">‹</button><figure><img id="lightbox-image" alt=""><figcaption id="lightbox-caption"></figcaption></figure><button class="lightbox__next" type="button" aria-label="Следующее фото">›</button><div id="lightbox-counter" class="lightbox__counter"></div></div><script type="application/json" id="gallery-data">{json.dumps([{'src':im(k,2),'alt':a} for k,a in all_photos],ensure_ascii=False)}</script>'''
save('media/photos',shell(photos,'Фотогалерея',2,'media'))

videos=f'''{pagehero('Видео','Film & performances','videos',2,'Движение дирижёрской руки, энергия оркестра и атмосфера концертного пространства.')}
<section class="section-block"><div class="container">{kicker('ВИДЕОАРХИВ','Moving image')}<h2 class="display-heading">Моменты, <em>которые звучат.</em></h2><p class="lead-short">Демонстрационный каталог: настоящие видеозаписи ещё не предоставлены. Обложки используются как визуальное оформление, не как видеоплееры.</p><div class="video-grid">{''.join(f'<article class="video-card"><div class="video-card__cover">{pic(k,alt,2)}<span class="video-card__status">ВИДЕО ПЛАНИРУЕТСЯ</span></div><div class="video-card__meta"><span>{n} / VIDEO ARCHIVE</span><h3>{title}</h3><p>{sub}</p></div></article>' for n,(k,alt,title,sub) in enumerate([('videos','Киноколлаж с оркестровой съёмкой','Концертные исполнения','Полные выступления и фрагменты'),('orchestra','Общая фотография симфонического оркестра','Большой концертный зал','Избранные музыкальные программы'),('conductor','Дирижёр в концертном зале','За кулисами','Репетиции, беседы и подготовка')],1))}</div></div></section>'''
save('media/videos',shell(videos,'Видео',2,'media'))

recordings=f'''{pagehero('Записи','Recordings & editions','about',1,'Каталог будущих аудиорелизов и коллекционных изданий.')}
<section class="section-block"><div class="container">{kicker('КОЛЛЕКЦИЯ','The recordings')}<h2 class="display-heading">Искусство <em>сохранять звук.</em></h2><p class="lead-short">Концептуальные обложки, созданные из уже подготовленных фотографий. Реальных альбомов, аудиофайлов и буклетов пока нет.</p><div class="records-grid">{''.join(f'<article class="record-tile"><div class="record-cover record-cover--{n}">{pic(key,'Демонстрационная обложка альбома с оркестровой фотографией',1)}<span class="record-cover__head">VALLEYS SYMPHONY</span><strong>{t}</strong><small>COLLECTOR’S EDITION / CONCEPT</small></div><div class="record-tile__meta"><h3>{t}</h3><p>Демонстрационный макет · запись не опубликована</p><button type="button" class="text-action" data-toast="Аудиозапись и буклет пока не предоставлены.">Материалы пока недоступны ↗</button></div></article>' for n,(key,t) in enumerate([('orchestra','THE SYMPHONY'),('violins','STRINGS'),('conductor','THE CONDUCTOR')],1))}</div></div></section>'''
save('recordings',shell(recordings,'Записи',1,'recordings'))

production=f'''{pagehero('Creative Development Studio','Digital production','videos',1,'Технологии на службе музыкального искусства.')}
<section class="section-block"><div class="container"><div class="editorial-spread"><div>{kicker('ВИЗУАЛЬНОЕ ПРОИЗВОДСТВО','Creative production')}<h2 class="display-heading">Продолжение музыки <em>за пределами зала.</em></h2></div><div><p class="editorial-lead">Разрабатываем художественный язык для цифрового присутствия оркестров: от первых кадров анонса до концепции иммерсивного концертного опыта.</p><p>Услуги представлены как направления студии. Примеры работ, технические параметры и реализованные кейсы добавляются после подтверждения.</p></div></div><div class="services-grid">{''.join(f'<article class="service-card"><div class="service-card__image">{pic(key,title,1)}</div><div class="service-card__body"><span>{idx} / {en}</span><h3>{title}</h3><p>{descr}</p></div></article>' for idx,(key,en,title,descr) in enumerate([('videos','ANIMATED TEASERS','Анимированный тизер','Промо-ролики, музыкальные заставки, видеографика и анонсы.'),('orchestra','ALBUM PRODUCTION','Производство альбома','Концепция записи, визуальная система релиза и материалы для публикации.'),('photos','IMMERSIVE BROADCAST','Иммерсивная трансляция','Проработка VR- и 360°-форматов для будущих концертных проектов.')],1))}</div><div class="section-bottom-action">{btn('Обсудить проект','contacts',1,variant='solid')}</div></div></section>'''
save('production',shell(production,'Creative Development Studio',1,'production'))

partners=f'''{pagehero('Партнёры','Partners & patrons','about',1,'Культура развивается через долгосрочное сотрудничество.')}
<section class="section-block"><div class="container">{kicker('КУЛЬТУРНЫЙ ДИАЛОГ','Partnership')}<div class="editorial-spread"><h2 class="display-heading">Создавать <em>вместе.</em></h2><p class="editorial-lead">Мы открыты к профессиональному диалогу с филармониями, фестивалями, культурными институциями и представителями бизнеса.</p></div><div class="partner-types"><div><span>01 / GENERAL</span><h3>Генеральные партнёры</h3><p>Место для согласованных логотипов и информации о сотрудничестве.</p></div><div><span>02 / CULTURE</span><h3>Культурные партнёры</h3><p>Резиденции, оркестры, театры, фестивали и филармонические площадки.</p></div><div><span>03 / MEDIA</span><h3>Информационные партнёры</h3><p>Профессиональные медиа и культурные издания.</p></div></div><div class="ecosystem" id="ecosystem">{kicker('VALLEYS CULTURAL GROUP','The ecosystem')}<h2>Единая культурная экосистема</h2><div class="ecosystem__grid"><div><strong>VALLEYS</strong><small>SYMPHONY ORCHESTRA</small></div><div><strong>THE VALLEYS</strong><small>MUSICAL AGENCY · КОНЦЕПЦИЯ</small></div><div><strong>OPERA</strong><small>PROFESSIONAL · КОНЦЕПЦИЯ</small></div><div><strong>CREATIVE</strong><small>DEVELOPMENT STUDIO</small></div></div></div>{btn('Связаться по вопросам партнёрства','contacts',1,variant='solid')}</div></section>'''
save('partners',shell(partners,'Партнёры',1,'partners'))

contacts=f'''{pagehero('Контакты','Contact & cooperation','about',1,'Открыты к профессиональному диалогу и новым культурным проектам.')}
<section class="section-block"><div class="container"><div class="contact-grid"><div>{kicker('ОБРАТНАЯ СВЯЗЬ','Get in touch')}<h2 class="display-heading">Начнём <em>диалог.</em></h2><p class="editorial-lead">Гастрольная деятельность, концертные проекты, медиасотрудничество и партнёрские программы.</p><div class="contact-lines"><div><span>БУКИНГ / BOOKING</span><p>Контактный адрес будет добавлен</p></div><div><span>ПРЕССА / PRESS</span><p>Контактный адрес будет добавлен</p></div><div><span>КОНЦЕРТНАЯ ПЛОЩАДКА / VENUE</span><p>Адрес будет добавлен</p></div></div></div><form class="contact-form" id="contact-form"><p class="contact-form__intro">Составьте заявку — сайт поможет скопировать её текст. Отправка писем не подключена.</p><label>Имя / Name<input name="name" type="text" autocomplete="name" required placeholder="Ваше имя"></label><label>Организация / Organisation<input name="org" type="text" placeholder="Название организации"></label><label>Email<input name="email" type="email" autocomplete="email" required placeholder="name@example.com"></label><label>Тип обращения / Request type<select name="type" required><option value="">Выберите тип</option><option>Концертный букинг</option><option>Партнёрство</option><option>Медиа и пресса</option><option>Creative Development Studio</option><option>Другое</option></select></label><label>Сообщение / Message<textarea name="message" rows="5" required placeholder="Опишите задачу или предложение"></textarea></label><label class="check-row"><input name="consent" type="checkbox" required><span>Я согласен(на) сформировать текст обращения локально в браузере. Данные никуда автоматически не отправляются.</span></label><button class="button button--solid" type="submit"><span>Скопировать заявку</span><span class="button__arrow">↗</span></button><p class="form-result" id="form-result" role="status" aria-live="polite"></p></form></div></div></section>'''
save('contacts',shell(contacts,'Контакты',1,'contacts'))

# save JS setup data
seating_data=[{**s,'img':'assets/images/'+s['image']+'.webp','href':'musicians/'+s['slug']+'/index.html'} for s in sections]
(P/'assets'/'seating-data.json').write_text(json.dumps(seating_data,ensure_ascii=False,indent=2),encoding='utf-8')
# favicon
(P/'assets'/'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#080808"/><path d="M10 16l17 34 9-20 9 20 9-34" fill="none" stroke="#c6a76b" stroke-width="3"/></svg>',encoding='utf-8')
print('pages created',len(list(P.rglob('index.html'))))
