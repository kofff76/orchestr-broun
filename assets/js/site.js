(() => {
  'use strict';
  const scriptURL = document.currentScript?.src || location.href;
  const siteRoot = new URL('../../', scriptURL).href;
  const imageURL = key => new URL('assets/images/' + key + '.webp', siteRoot).href;
  const pageURL = path => new URL(path.replace(/^\//, '') + (path.endsWith('/') ? '' : '/index.html'), siteRoot).href;
  const toastEl = document.getElementById('site-toast');
  let toastTimer;
  function notify(message) {
    if (!toastEl) return;
    toastEl.textContent = message;
    toastEl.classList.add('is-visible');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toastEl.classList.remove('is-visible'), 4400);
  }

  // Navigation. It remains usable with keyboard and without hover.
  const header = document.getElementById('site-header');
  const toggle = document.querySelector('.menu-toggle');
  const mobile = document.getElementById('mobile-navigation');
  function openMenu(open) {
    if (!toggle || !mobile) return;
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Закрыть меню' : 'Открыть меню');
    mobile.hidden = !open;
    document.body.classList.toggle('is-locked', open);
    header?.classList.toggle('is-open', open);
    if (open) mobile.querySelector('a')?.focus();
    else toggle.focus();
  }
  toggle?.addEventListener('click', () => openMenu(toggle.getAttribute('aria-expanded') !== 'true'));
  mobile?.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
    mobile.hidden = true;
    document.body.classList.remove('is-locked');
    toggle?.setAttribute('aria-expanded', 'false');
  }));
  function updateHeader() { header?.classList.toggle('is-scrolled', window.scrollY > 46); }
  updateHeader();
  window.addEventListener('scroll', updateHeader, { passive: true });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && toggle?.getAttribute('aria-expanded') === 'true') openMenu(false);
  });
  window.addEventListener('resize', () => {
    if (window.innerWidth > 1190 && toggle?.getAttribute('aria-expanded') === 'true') openMenu(false);
  });

  // An unobtrusive one-time reveal; respects reduced motion and no-JS display.
  const revealNodes = Array.from(document.querySelectorAll('.reveal'));
  if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: .08, rootMargin: '0px 0px 65px 0px' });
    document.documentElement.classList.add('js-ready');
    revealNodes.forEach(node => observer.observe(node));
  } else revealNodes.forEach(node => node.classList.add('is-visible'));

  document.querySelectorAll('[data-toast]').forEach(button => {
    button.addEventListener('click', () => notify(button.dataset.toast));
  });

  const sections = [
    { id: 'first-violins', ru: 'Первые скрипки', en: 'First violins', image: 'first-violins', start: -166, end: -129, radius: [150, 195, 240], count: [5, 8, 10], description: 'Ведущая мелодическая линия, единство тембра и интонационная точность.' },
    { id: 'second-violins', ru: 'Вторые скрипки', en: 'Second violins', image: 'second-violins', start: -126, end: -96, radius: [150, 195, 240], count: [5, 6, 8], description: 'Гармоническая опора и движение внутренних музыкальных голосов.' },
    { id: 'strings', ru: 'Струнная группа', en: 'Strings', image: 'violins', start: -94, end: -71, radius: [157, 204, 246], count: [4, 6, 6], description: 'Единое дыхание и богатство струнных тембров оркестра.' },
    { id: 'cellos', ru: 'Виолончели', en: 'Cellos', image: 'cellos', start: -68, end: -43, radius: [165, 212, 252], count: [4, 5, 6], description: 'Насыщенный лирический тембр и выразительность нижнего регистра.' },
    { id: 'basses', ru: 'Контрабасы', en: 'Double basses', image: 'basses', start: -40, end: -17, radius: [180, 225, 270], count: [3, 4, 4], description: 'Глубина и устойчивость гармонического фундамента.' },
    { id: 'woodwinds', ru: 'Деревянные духовые', en: 'Woodwinds', image: 'woodwinds', start: -156, end: -93, radius: [290, 332], count: [9, 11], description: 'Флейта, гобой, кларнет и фагот — индивидуальность тембров.' },
    { id: 'percussion', ru: 'Ударные', en: 'Percussion', image: 'percussion', start: -85, end: -22, radius: [295, 338], count: [8, 9], description: 'Точная ритмика и динамические кульминации оркестровой партитуры.' }
  ];
  function stageMarkup() {
    const groups = sections.map(section => {
      const dots = [];
      section.radius.forEach((r, row) => {
        const count = section.count[row];
        for (let i = 0; i < count; i++) {
          const angle = (section.start + (section.end - section.start) * ((i + .5) / count)) * Math.PI / 180;
          const cx = 500 + Math.cos(angle) * r;
          const cy = 455 + Math.sin(angle) * r;
          dots.push(`<circle class="seat" cx="${cx.toFixed(1)}" cy="${cy.toFixed(1)}" r="8.8" />`);
        }
      });
      return `<g class="group" data-section="${section.id}" role="button" tabindex="0" aria-label="Выбрать секцию: ${section.ru}">${dots.join('')}</g>`;
    });
    return `<svg viewBox="0 0 1000 535" role="group" aria-label="Схематичное расположение инструментальных групп оркестра" xmlns="http://www.w3.org/2000/svg">
      <path class="stage-line" d="M103 455 A397 397 0 0 1 897 455" />
      <path class="stage-line" d="M137 455 A363 363 0 0 1 863 455" />
      ${groups.join('')}
      <rect class="stage-center" x="490" y="449" width="20" height="30" rx="2" />
      <path class="stage-line" d="M450 493 L550 493" />
      <text x="500" y="515" text-anchor="middle">ДИРИЖЁР</text></svg>`;
  }
  document.querySelectorAll('[data-seating-map]').forEach(mount => {
    mount.className = 'seating-map';
    mount.innerHTML = `<div class="seating-map__visual">${stageMarkup()}<div class="seating-map__label">СХЕМАТИЧЕСКАЯ РАССАДКА / ILLUSTRATIVE SEATING MAP</div></div>
      <div class="seating-map__details"><div class="seating-map__photo"><img data-section-img alt="Фотография инструментальной группы"></div>
      <div class="seating-map__description"><span data-section-en></span><h3 data-section-name></h3><p data-section-desc></p></div>
      <div class="seat-legend" aria-label="Выберите инструментальную группу">${sections.map(s => `<button type="button" data-section="${s.id}">${s.ru}</button>`).join('')}</div>
      <div class="seating-map__links"><span>КАРТОЧКА ГРУППЫ</span><a data-section-link href="#">Подробнее ↗</a></div></div>`;
    let chosen = '';
    function choose(id) {
      const found = sections.find(s => s.id === id);
      if (!found || chosen === id) return;
      chosen = id;
      mount.querySelector('[data-section-img]').src = imageURL(found.image);
      mount.querySelector('[data-section-img]').alt = found.ru;
      mount.querySelector('[data-section-en]').textContent = found.en;
      mount.querySelector('[data-section-name]').textContent = found.ru;
      mount.querySelector('[data-section-desc]').textContent = found.description;
      mount.querySelector('[data-section-link]').href = pageURL('musicians/' + found.id);
      mount.querySelectorAll('[data-section]').forEach(node => {
        node.classList.toggle('is-selected', node.dataset.section === id);
        if (node.matches('button')) node.setAttribute('aria-pressed', String(node.dataset.section === id));
      });
    }
    mount.querySelectorAll('g[data-section]').forEach(group => {
      group.addEventListener('mouseenter', () => choose(group.dataset.section));
      group.addEventListener('focus', () => choose(group.dataset.section));
      group.addEventListener('click', () => choose(group.dataset.section));
      group.addEventListener('keydown', e => {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); choose(group.dataset.section); }
      });
    });
    mount.querySelectorAll('.seat-legend button').forEach(button => {
      button.addEventListener('click', () => choose(button.dataset.section));
    });
    choose(sections[0].id);
  });

  const filter = document.getElementById('composer-filter');
  const concertGrid = document.getElementById('concert-grid');
  function applyFilter() {
    const active = filter?.value || 'all';
    let visible = 0;
    concertGrid?.querySelectorAll('.concert-card').forEach(card => {
      const included = active === 'all' || card.querySelector('h3')?.textContent.includes(active);
      card.hidden = !included;
      if (included) visible++;
    });
    const empty = document.getElementById('filter-empty');
    if (empty) empty.hidden = visible > 0;
  }
  filter?.addEventListener('change', applyFilter);
  document.querySelectorAll('[data-view]').forEach(button => {
    button.addEventListener('click', () => {
      concertGrid?.classList.toggle('is-list', button.dataset.view === 'list');
      document.querySelectorAll('[data-view]').forEach(b => {
        const active = b === button;
        b.classList.toggle('is-active', active);
        b.setAttribute('aria-pressed', String(active));
      });
    });
  });

  // Accessible lightbox for photos; opens from the actual generated image library.
  const lightbox = document.getElementById('lightbox');
  const galleryJson = document.getElementById('gallery-data');
  if (lightbox && galleryJson) {
    const data = JSON.parse(galleryJson.textContent);
    const photo = document.getElementById('lightbox-image');
    const caption = document.getElementById('lightbox-caption');
    const counter = document.getElementById('lightbox-counter');
    let current = 0;
    let origin = null;
    let touchX = 0;
    const close = lightbox.querySelector('.lightbox__close');
    function show(index) {
      current = (index + data.length) % data.length;
      photo.src = data[current].src;
      photo.alt = data[current].alt;
      caption.textContent = data[current].alt;
      counter.textContent = `${String(current+1).padStart(2,'0')} / ${String(data.length).padStart(2,'0')}`;
    }
    function open(index, button) {
      origin = button; show(index); lightbox.hidden = false;
      document.body.classList.add('is-locked'); close.focus();
    }
    function shut() {
      lightbox.hidden = true; document.body.classList.remove('is-locked'); origin?.focus();
    }
    document.querySelectorAll('[data-lightbox]').forEach(btn => btn.addEventListener('click', () => open(Number(btn.dataset.lightbox), btn)));
    close.addEventListener('click', shut);
    lightbox.querySelector('.lightbox__prev').addEventListener('click', () => show(current-1));
    lightbox.querySelector('.lightbox__next').addEventListener('click', () => show(current+1));
    lightbox.addEventListener('click', e => { if (e.target === lightbox) shut(); });
    lightbox.addEventListener('touchstart', e => { touchX = e.changedTouches[0].screenX; }, { passive: true });
    lightbox.addEventListener('touchend', e => {
      const dx = e.changedTouches[0].screenX - touchX;
      if (Math.abs(dx) > 60) show(current + (dx < 0 ? 1 : -1));
    }, { passive: true });
    document.addEventListener('keydown', e => {
      if (lightbox.hidden) return;
      if (e.key === 'Escape') shut();
      else if (e.key === 'ArrowRight') show(current+1);
      else if (e.key === 'ArrowLeft') show(current-1);
      else if (e.key === 'Tab') { e.preventDefault(); close.focus(); }
    });
  }

  // Local-only contact form: user explicitly gets the formatted text; no sending or stored data.
  const form = document.getElementById('contact-form');
  form?.addEventListener('submit', async e => {
    e.preventDefault();
    if (!form.reportValidity()) return;
    const formData = new FormData(form);
    const request = [
      'Обращение в Valleys Symphony Orchestra',
      'Имя: ' + formData.get('name'),
      'Организация: ' + (formData.get('org') || '—'),
      'Email: ' + formData.get('email'),
      'Тип обращения: ' + formData.get('type'),
      '',
      String(formData.get('message')),
      '',
      'Сформировано локально на демонстрационном сайте. Не отправлено.'
    ].join('\n');
    const result = document.getElementById('form-result');
    try {
      await navigator.clipboard.writeText(request);
      result.textContent = 'Текст заявки скопирован. Форма ничего не отправляла.';
      notify('Заявка скопирована в буфер обмена. Автоматическая отправка не выполнялась.');
    } catch (_) {
      const ta = document.createElement('textarea');
      ta.value = request; ta.readOnly = true;
      ta.style.cssText = 'width:100%;height:185px;color:#fff;background:#151515;margin-top:12px;';
      result.textContent = 'Автоматическое копирование недоступно. Выделите и скопируйте текст ниже:';
      result.after(ta); ta.focus(); ta.select();
    }
  });
})();
