// 影之刃零 攻略 — filters, progress, lightbox, spoilers
(function () {
  var page = document.body.getAttribute('data-page') || 'x';
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };

  // hide broken images (and their frame) gracefully
  document.querySelectorAll('img[data-hide-broken]').forEach(function (img) {
    img.addEventListener('error', function () {
      var box = img.closest('.shot, .mapthumb');
      if (box) box.classList.add('hidden');
      var hero = img.closest('.boss-hero');
      if (hero) { img.remove(); hero.classList.add('noimg'); }
      var shots = img.closest('.shots');
      if (shots && !shots.querySelector('.shot:not(.hidden)')) {
        shots.classList.add('hidden');
        var g = shots.closest('.item-grid'); if (g) g.classList.remove('has-img');
      }
    });
  });

  // lightbox
  var lb = document.createElement('div');
  lb.className = 'lb';
  lb.innerHTML = '<img alt=""><div class="cap"></div>';
  document.body.appendChild(lb);
  document.addEventListener('click', function (e) {
    var z = e.target.closest('[data-zoom]');
    if (z && !z.querySelector('.spoiler:not(.revealed)')) {
      var img = z.querySelector('img');
      if (!img) return;
      lb.querySelector('img').src = img.currentSrc || img.src;
      lb.querySelector('.cap').textContent = z.getAttribute('data-zoom') || '';
      lb.classList.add('on');
    }
  });
  lb.addEventListener('click', function () { lb.classList.remove('on'); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') lb.classList.remove('on'); });

  // spoilers
  document.addEventListener('click', function (e) {
    var s = e.target.closest('.spoiler');
    if (s) { e.stopPropagation(); s.classList.add('revealed'); }
  }, true);

  // done checkboxes + progress
  var entries = [].slice.call(document.querySelectorAll('.entry[data-id]'));
  function updateProgress() {
    var el = document.getElementById('prog');
    if (!el) return;
    var all = entries.length, done = entries.filter(function (x) { return x.classList.contains('done'); }).length;
    el.innerHTML = '已完成 <b>' + done + '</b> / ' + all;
  }
  entries.forEach(function (en) {
    var key = 'pbz:' + page + ':' + en.getAttribute('data-id');
    var cb = en.querySelector('.check input');
    if (!cb) return;
    if (store.get(key) === '1') { cb.checked = true; en.classList.add('done'); }
    cb.addEventListener('change', function () {
      en.classList.toggle('done', cb.checked);
      store.set(key, cb.checked ? '1' : '0');
      updateProgress();
    });
  });
  updateProgress();

  // filters
  var chips = [].slice.call(document.querySelectorAll('.chip[data-f]'));
  var hideDone = false;
  function apply(f) {
    document.querySelectorAll('.entry').forEach(function (en) {
      var tags = (en.getAttribute('data-tags') || '').split(' ');
      var show = f === 'all' || tags.indexOf(f) >= 0 || tags.indexOf('always') >= 0;
      if (hideDone && en.classList.contains('done')) show = false;
      en.classList.toggle('hidden', !show);
    });
  }
  var current = 'all';
  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      current = c.getAttribute('data-f');
      chips.forEach(function (x) { x.classList.toggle('on', x === c); });
      apply(current);
    });
  });
  var hd = document.getElementById('hidedone');
  if (hd) hd.addEventListener('click', function () {
    hideDone = !hideDone; hd.classList.toggle('on', hideDone); apply(current);
  });
})();
