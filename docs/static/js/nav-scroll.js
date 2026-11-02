// On phones and tablets the header slides away when scrolling down and returns when scrolling up.
(function () {
  var nav = document.querySelector(".site-nav");
  if (!nav) return;
  var small = window.matchMedia("(max-width: 991.98px)");
  var last = window.scrollY;
  var ticking = false;

  function update() {
    var y = Math.max(window.scrollY, 0);
    var delta = y - last;
    ticking = false;
    if (!small.matches || y < nav.offsetHeight + 20) {
      nav.classList.remove("nav-hidden");
    } else if (delta > 6) {
      nav.classList.add("nav-hidden");
    } else if (delta < -6) {
      nav.classList.remove("nav-hidden");
    }
    if (Math.abs(delta) > 6 || y === 0) last = y;
  }

  window.addEventListener("scroll", function () {
    if (!ticking) { ticking = true; window.requestAnimationFrame(update); }
  }, { passive: true });
  // Keyboard users must always be able to reach the links.
  nav.addEventListener("focusin", function () { nav.classList.remove("nav-hidden"); });
})();
