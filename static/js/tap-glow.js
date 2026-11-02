// A soft glow wherever someone taps on a phone or tablet.
(function () {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  document.addEventListener("pointerdown", function (e) {
    if (e.pointerType !== "touch") return;
    var glow = document.createElement("span");
    glow.className = "touch-glow";
    glow.setAttribute("aria-hidden", "true");
    glow.style.left = e.clientX + "px";
    glow.style.top = e.clientY + "px";
    glow.addEventListener("animationend", function () { glow.remove(); });
    document.body.appendChild(glow);
  }, { passive: true });
})();
