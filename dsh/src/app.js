/* 影之刃零 · 江湖行止錄 */
(function () {
  'use strict';

  const $ = (s, r) => (r || document).querySelector(s);
  const $$ = (s, r) => Array.from((r || document).querySelectorAll(s));
  const store = {
    get(k, d) { try { const v = localStorage.getItem('pbz:' + k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem('pbz:' + k, JSON.stringify(v)); } catch (e) {} }
  };

  /* Mobile menu */
  const menuBtn = $('.menu-btn');
  const nav = $('.nav');
  if (menuBtn && nav) {
    menuBtn.addEventListener('click', () => {
      const open = nav.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
      menuBtn.textContent = open ? '✕' : '☰';
    });
    $$('.nav a').forEach(a => a.addEventListener('click', () => {
      nav.classList.remove('open');
      menuBtn.textContent = '☰';
    }));
  }

  /* Spoilers */
  const sp = $('.spoiler-toggle');
  const applySpoiler = (on) => {
    document.body.classList.toggle('show-spoilers', on);
    if (sp) {
      sp.setAttribute('aria-pressed', on ? 'true' : 'false');
      sp.querySelector('span:last-child').textContent = on ? '劇透已顯示' : '開啟劇透';
    }
  };
  applySpoiler(store.get('spoilers', false));
  if (sp) sp.addEventListener('click', () => {
    const on = !document.body.classList.contains('show-spoilers');
    applySpoiler(on);
    store.set('spoilers', on);
  });

  /* Reveal on scroll */
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(en => { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    $$('.reveal').forEach(el => io.observe(el));
  } else {
    $$('.reveal').forEach(el => el.classList.add('in'));
  }

  /* Reading progress */
  const bar = $('.readbar');
  const onScroll = () => {
    if (bar) {
      const h = document.documentElement.scrollHeight - innerHeight;
      bar.style.width = (h > 0 ? Math.min(100, scrollY / h * 100) : 0) + '%';
    }
  };
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* TOC active */
  const tocLinks = $$('.toc a[href^="#"]');
  if (tocLinks.length && 'IntersectionObserver' in window) {
    const map = new Map();
    tocLinks.forEach(a => {
      const el = document.getElementById(a.getAttribute('href').slice(1));
      if (el) map.set(el, a);
    });
    const tio = new IntersectionObserver((entries) => {
      entries.forEach(en => {
        if (en.isIntersecting) {
          tocLinks.forEach(a => a.classList.remove('active'));
          const a = map.get(en.target);
          if (a) a.classList.add('active');
        }
      });
    }, { rootMargin: '-18% 0px -70% 0px' });
    map.forEach((a, el) => tio.observe(el));
  }

  /* Checklists */
  $$('.checklist').forEach(list => {
    const key = 'check:' + (list.dataset.key || 'default');
    const boxes = $$('input[type=checkbox]', list);
    const saved = store.get(key, {});
    boxes.forEach(b => {
      const id = b.value || b.dataset.id;
      if (saved[id]) b.checked = true;
      b.addEventListener('change', () => {
        const state = {};
        boxes.forEach(x => { if (x.checked) state[x.value || x.dataset.id] = 1; });
        store.set(key, state);
        updateProgress();
      });
    });
    function updateProgress() {
      const done = boxes.filter(b => b.checked).length;
      const total = boxes.length;
      const fill = $('.check-progress .bar i', list.parentElement);
      const txt = $('.check-progress .txt', list.parentElement);
      if (fill) fill.style.width = (total ? done / total * 100 : 0) + '%';
      if (txt) txt.textContent = done + ' / ' + total + ' 已完成';
    }
    updateProgress();
  });

  /* Boss filter */
  const filters = $$('.filter');
  const tiles = $$('.boss-tile');
  if (filters.length && tiles.length) {
    filters.forEach(f => f.addEventListener('click', () => {
      filters.forEach(x => x.classList.remove('active'));
      f.classList.add('active');
      const cat = f.dataset.filter;
      let n = 0;
      tiles.forEach(t => {
        const show = cat === 'all' || t.dataset.chapter === cat || (cat === 'miss' && t.dataset.miss === '1');
        t.style.display = show ? '' : 'none';
        if (show) n++;
      });
      const empty = $('.empty');
      if (empty) empty.style.display = n ? 'none' : 'block';
    }));
  }

  /* Toast */
  let toastTimer;
  window.pbzToast = (msg) => {
    let t = $('.toast');
    if (!t) { t = document.createElement('div'); t.className = 'toast'; document.body.appendChild(t); }
    t.textContent = msg;
    requestAnimationFrame(() => t.classList.add('show'));
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => t.classList.remove('show'), 2200);
  };

  /* Checklist share/reset */
  $$('[data-reset]').forEach(btn => btn.addEventListener('click', () => {
    const list = document.getElementById(btn.dataset.reset);
    if (!list) return;
    $$('input[type=checkbox]', list).forEach(b => b.checked = false);
    const key = 'check:' + (list.dataset.key || 'default');
    store.set(key, {});
    location.reload();
  }));
})();
