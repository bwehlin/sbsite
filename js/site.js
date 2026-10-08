// Feature slideshow: auto-advances, pauses on hover/focus and via the pause button,
// starts paused under prefers-reduced-motion.
const show = document.querySelector(".slideshow");
const slides = show.querySelectorAll(".slide");
const dots = show.querySelectorAll(".dots button");
const pauseButton = show.querySelector(".pause");
let current = 0;
let paused = matchMedia("(prefers-reduced-motion: reduce)").matches;
let hovered = false;

function go(i) {
  current = (i + slides.length) % slides.length;
  slides.forEach((s, j) => (s.hidden = j !== current));
  dots.forEach((d, j) => d.setAttribute("aria-current", j === current));
}

function setPaused(p) {
  paused = p;
  pauseButton.textContent = p ? "Play" : "Pause";
  pauseButton.setAttribute("aria-pressed", p);
}

dots.forEach((d, i) => d.addEventListener("click", () => go(i)));
pauseButton.addEventListener("click", () => setPaused(!paused));
show.addEventListener("mouseenter", () => (hovered = true));
show.addEventListener("mouseleave", () => (hovered = false));
setPaused(paused);
setInterval(() => {
  if (!paused && !hovered && !show.contains(document.activeElement)) go(current + 1);
}, 6000);

// Copy buttons: data-copy holds the id of the element whose text to copy.
document.querySelectorAll("[data-copy]").forEach((b) =>
  b.addEventListener("click", async () => {
    await navigator.clipboard.writeText(document.getElementById(b.dataset.copy).textContent);
    b.textContent = "Copied";
    setTimeout(() => (b.textContent = "Copy"), 2000);
  })
);
