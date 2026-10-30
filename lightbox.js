// Full-size view of the site's pictures: a click on an image marked data-full opens it over the page; arrows or the
// side buttons go through the other pictures of the page, Esc or a click on the dark area closes it.
(function () {
  var style = document.createElement('style');
  style.textContent =
    '[data-full]{cursor:zoom-in}' +
    '.lb{position:fixed;inset:0;z-index:50;background:rgba(8,10,12,.92);display:flex;align-items:center;justify-content:center;flex-direction:column;padding:16px}' +
    '.lb[hidden]{display:none}' +
    '.lb img{max-width:100%;max-height:calc(100vh - 80px);border-radius:6px;box-shadow:0 8px 40px rgba(0,0,0,.6)}' +
    '.lb p{color:#e7e4dc;margin:10px 0 0;font:15px/1.4 system-ui,sans-serif;text-align:center}' +
    '.lb button{position:absolute;background:rgba(0,0,0,.45);color:#fff;border:1px solid rgba(255,255,255,.25);border-radius:8px;' +
    'font:22px/1 system-ui,sans-serif;width:44px;height:44px;cursor:pointer}' +
    '.lb .close{top:12px;right:12px}.lb .prev{left:12px;top:50%}.lb .next{right:12px;top:50%}';
  document.head.appendChild(style);
  var box = document.createElement('div');
  box.className = 'lb';
  box.hidden = true;
  box.innerHTML = '<img alt=""><p></p><button class="close" aria-label="Close">×</button>' +
    '<button class="prev" aria-label="Previous">‹</button><button class="next" aria-label="Next">›</button>';
  document.body.appendChild(box);
  var big = box.querySelector('img'), caption = box.querySelector('p'), list = [], at = 0;

  function visible() {
    return Array.prototype.filter.call(document.querySelectorAll('[data-full]'), function (el) { return el.offsetParent !== null; });
  }
  function show(i) {
    at = (i + list.length) % list.length;
    var el = list[at];
    big.src = el.dataset.full;
    big.alt = el.alt || '';
    caption.textContent = el.alt || '';
    box.querySelector('.prev').hidden = box.querySelector('.next').hidden = list.length < 2;
  }
  function close() { box.hidden = true; big.src = ''; }

  document.addEventListener('click', function (e) {
    var el = e.target.closest ? e.target.closest('[data-full]') : null;
    if (!el) return;
    e.preventDefault();
    list = visible();
    box.hidden = false;
    show(Math.max(0, list.indexOf(el)));
  });
  box.addEventListener('click', function (e) {
    if (e.target.classList.contains('prev')) show(at - 1);
    else if (e.target.classList.contains('next')) show(at + 1);
    else if (e.target !== big) close();
  });
  document.addEventListener('keydown', function (e) {
    if (box.hidden) return;
    if (e.key === 'Escape') close();
    else if (e.key === 'ArrowLeft') show(at - 1);
    else if (e.key === 'ArrowRight') show(at + 1);
  });
})();
