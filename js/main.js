(function () {
  document.getElementById('year').textContent = new Date().getFullYear();

  var toggle = document.querySelector('.nav-toggle');
  var links = document.getElementById('nav-links');
  toggle.addEventListener('click', function () {
    var open = links.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
  });
  links.addEventListener('click', function (e) {
    if (e.target.tagName === 'A') {
      links.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    }
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
