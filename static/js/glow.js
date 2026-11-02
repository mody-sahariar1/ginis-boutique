// A soft warm light that follows the mouse, and a glow wherever someone taps.
(function () {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  var light = document.createElement("div");
  light.className = "cursor-light";
  light.setAttribute("aria-hidden", "true");
  document.body.appendChild(light);

  document.addEventListener("pointermove", function (e) {
    if (e.pointerType !== "mouse") return;
    light.style.transform = "translate(" + e.clientX + "px," + e.clientY + "px)";
    light.classList.add("is-on");
  }, { passive: true });

  document.documentElement.addEventListener("mouseleave", function () {
    light.classList.remove("is-on");
  });

  document.addEventListener("pointerdown", function (e) {
    var glow = document.createElement("span");
    glow.className = "touch-glow";
    glow.setAttribute("aria-hidden", "true");
    glow.style.left = e.clientX + "px";
    glow.style.top = e.clientY + "px";
    glow.addEventListener("animationend", function () { glow.remove(); });
    document.body.appendChild(glow);
  }, { passive: true });
})();
