(function () {
  document.getElementById('year').textContent = new Date().getFullYear();

  var toggle = document.querySelector('.nav-toggle');
  var links = document.getElementById('nav-links');
  toggle.addEventListener('click', function () {
    var open = links.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
  });
  function closeNav() {
    links.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
  }
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && links.classList.contains('open')) { closeNav(); toggle.focus(); }
  });
  document.addEventListener('click', function (e) {
    if (links.classList.contains('open') && !e.target.closest('.nav')) closeNav();
  });
  window.matchMedia('(min-width: 961px)').addEventListener('change', function (e) { if (e.matches) closeNav(); });
  links.addEventListener('click', function (e) {
    if (e.target.tagName === 'A') closeNav();
  });

  var list = document.getElementById('pub-list');
  document.querySelectorAll('.pub-filter .chip').forEach(function (chip) {
    chip.addEventListener('click', function () {
      document.querySelectorAll('.pub-filter .chip').forEach(function (c) { c.classList.remove('active'); });
      chip.classList.add('active');
      var key = chip.dataset.sort;
      var items = Array.prototype.slice.call(list.children);
      items.sort(function (a, b) {
        var primary = Number(b.dataset[key]) - Number(a.dataset[key]);
        if (primary !== 0) return primary;
        return key === 'year' ? Number(b.dataset.cites) - Number(a.dataset.cites) : Number(b.dataset.year) - Number(a.dataset.year);
      });
      items.forEach(function (li) { list.appendChild(li); });
    });
  });

  var copyBtn = document.getElementById('copy-bio');
  var copyStatus = document.querySelector('.copy-status');
  copyBtn.addEventListener('click', function () {
    var text = document.getElementById('short-bio').textContent.trim();
    var done = function () { copyStatus.textContent = 'Copied'; setTimeout(function () { copyStatus.textContent = ''; }, 2000); };
    if (navigator.clipboard) {
      navigator.clipboard.writeText(text).then(done, function () { copyStatus.textContent = 'Select and copy the text above'; });
    } else {
      copyStatus.textContent = 'Select and copy the text above';
    }
  });

  var navAnchors = document.querySelectorAll('.nav-links a');
  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          navAnchors.forEach(function (a) {
            a.classList.toggle('active', a.getAttribute('href') === '#' + entry.target.id);
          });
        }
      });
    }, { rootMargin: '-40% 0px -55% 0px' });
    document.querySelectorAll('main section[id]').forEach(function (s) { observer.observe(s); });
  }
})();
