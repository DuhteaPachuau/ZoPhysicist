const body = document.body;
const navToggle = document.querySelector(".nav-toggle");
const siteNav = document.querySelector(".site-nav");
const themeToggles = document.querySelectorAll(".theme-toggle");
const scrollTop = document.querySelector(".scroll-top");
const progress = document.getElementById("readingProgress");

document.documentElement.classList.add(localStorage.getItem("theme") || "theme-dark");

window.addEventListener("load", () => {
  document.querySelector(".page-loader")?.classList.add("loaded");
});

navToggle?.addEventListener("click", () => {
  const open = navToggle.getAttribute("aria-expanded") === "true";
  navToggle.setAttribute("aria-expanded", String(!open));
  siteNav?.classList.toggle("open");
});

themeToggles.forEach((themeToggle) => {
  themeToggle.addEventListener("click", () => {
    const html = document.documentElement;
    const next = html.classList.contains("theme-light") ? "theme-dark" : "theme-light";
    html.classList.remove("theme-dark", "theme-light");
    html.classList.add(next);
    localStorage.setItem("theme", next);
  });
});

const updateProgress = () => {
  const total = document.documentElement.scrollHeight - window.innerHeight;
  const value = total > 0 ? (window.scrollY / total) * 100 : 0;
  if (progress) progress.style.width = `${value}%`;
  scrollTop?.classList.toggle("visible", window.scrollY > 600);
};

window.addEventListener("scroll", updateProgress, { passive: true });
updateProgress();

scrollTop?.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));

const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("visible");
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.15 });

document.querySelectorAll(".reveal").forEach((el) => revealObserver.observe(el));

const content = document.getElementById("lessonContent");
const toc = document.getElementById("tocList");
if (content && toc) {
  const headings = content.querySelectorAll("h2, h3");
  headings.forEach((heading, index) => {
    if (!heading.id) heading.id = `section-${index + 1}`;
    const link = document.createElement("a");
    link.href = `#${heading.id}`;
    link.textContent = heading.textContent;
    link.className = heading.tagName.toLowerCase();
    toc.appendChild(link);
  });
}

document.querySelectorAll("[data-share]").forEach((button) => {
  button.addEventListener("click", async () => {
    const url = window.location.href;
    if (button.dataset.share === "x") {
      window.open(`https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}`, "_blank", "noopener");
      return;
    }
    await navigator.clipboard?.writeText(url);
    button.textContent = "Copied";
    setTimeout(() => { button.textContent = "Link"; }, 1400);
  });
});

const liveInput = document.querySelector("[data-live-search]");
const suggestions = document.getElementById("suggestions");
let searchTimer;
liveInput?.addEventListener("input", () => {
  clearTimeout(searchTimer);
  const q = liveInput.value.trim();
  if (!q || q.length < 2) {
    if (suggestions) suggestions.innerHTML = "";
    return;
  }
  searchTimer = setTimeout(async () => {
    const response = await fetch(`/search/?q=${encodeURIComponent(q)}`, {
      headers: { "x-requested-with": "XMLHttpRequest" },
    });
    const data = await response.json();
    if (!suggestions) return;
    suggestions.innerHTML = data.suggestions.map((item) => `
      <a href="/lessons/${item.slug}/">
        <strong>${item.title}</strong>
        <span>${item.short_description}</span>
      </a>
    `).join("");
  }, 180);
});

document.querySelectorAll("img").forEach((img) => {
  img.addEventListener("load", () => img.classList.add("loaded"));
});

const tocToggle = document.querySelector(".toc-toggle");
const tocPanel = document.querySelector(".toc");
tocToggle?.addEventListener("click", () => {
  const isOpen = tocToggle.getAttribute("aria-expanded") === "true";
  tocToggle.setAttribute("aria-expanded", String(!isOpen));
  tocPanel?.classList.toggle("collapsed", isOpen);
});

const answerButton = document.querySelector(".reveal-answer");
const answerPanel = document.querySelector(".answer-panel");
const optionButtons = document.querySelectorAll(".option-button");

answerButton?.addEventListener("click", () => {
  const answer = answerButton.dataset.answer;
  answerPanel.hidden = false;
  answerButton.textContent = "Answer shown";
  optionButtons.forEach((button) => {
    button.classList.toggle("correct", button.dataset.option === answer);
  });
});

optionButtons.forEach((button) => {
  button.addEventListener("click", () => {
    optionButtons.forEach((item) => item.classList.remove("selected"));
    button.classList.add("selected");
  });
});

document.querySelectorAll(".mobile-nav-parent, .mobile-category-toggle").forEach((button) => {
  button.addEventListener("click", () => {
    const isOpen = button.getAttribute("aria-expanded") === "true";
    button.setAttribute("aria-expanded", String(!isOpen));
    button.nextElementSibling?.classList.toggle("open", !isOpen);
  });
});

function setupCanvas(canvas) {
  if (!canvas) return null;
  const ctx = canvas.getContext("2d");
  const resize = () => {
    const rect = canvas.getBoundingClientRect();
    const ratio = window.devicePixelRatio || 1;
    canvas.width = Math.max(320, rect.width * ratio);
    canvas.height = Math.max(240, rect.height * ratio);
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
  };
  resize();
  window.addEventListener("resize", resize);
  return { ctx, size: () => canvas.getBoundingClientRect() };
}

const waveCanvas = document.getElementById("waveCanvas");
if (waveCanvas) {
  const lab = setupCanvas(waveCanvas);
  const amp = document.getElementById("waveAmp");
  const freq = document.getElementById("waveFreq");
  const speed = document.getElementById("waveSpeed");
  const toggle = document.getElementById("waveToggle");
  let running = true;
  let t = 0;
  toggle?.addEventListener("click", () => {
    running = !running;
    toggle.textContent = running ? "Pause" : "Play";
  });
  document.querySelectorAll("[data-wave-preset]").forEach((button) => {
    button.addEventListener("click", () => {
      const preset = button.dataset.wavePreset;
      amp.value = preset === "calm" ? 35 : 95;
      freq.value = preset === "calm" ? 2 : 8;
      speed.value = preset === "calm" ? 2 : 7;
    });
  });
  const draw = () => {
    const { ctx, size } = lab;
    const { width, height } = size();
    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = "rgba(85, 215, 255, 0.06)";
    for (let x = 0; x < width; x += 34) ctx.fillRect(x, 0, 1, height);
    ctx.beginPath();
    for (let x = 0; x <= width; x += 3) {
      const y = height / 2 + Math.sin((x / width) * Number(freq.value) * Math.PI * 2 + t) * Number(amp.value);
      if (x === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.strokeStyle = "#55d7ff";
    ctx.lineWidth = 4;
    ctx.shadowColor = "#55d7ff";
    ctx.shadowBlur = 18;
    ctx.stroke();
    ctx.shadowBlur = 0;
    if (running) t += Number(speed.value) * 0.025;
    requestAnimationFrame(draw);
  };
  draw();
}

const pendulumCanvas = document.getElementById("pendulumCanvas");
if (pendulumCanvas) {
  const lab = setupCanvas(pendulumCanvas);
  const lengthInput = document.getElementById("pendulumLength");
  const gravityInput = document.getElementById("pendulumGravity");
  const angleInput = document.getElementById("pendulumAngle");
  const reset = document.getElementById("pendulumReset");
  let angle = Number(angleInput.value) * Math.PI / 180;
  let velocity = 0;
  reset?.addEventListener("click", () => {
    angle = Number(angleInput.value) * Math.PI / 180;
    velocity = 0;
  });
  const draw = () => {
    const { ctx, size } = lab;
    const { width, height } = size();
    const length = Number(lengthInput.value);
    const gravity = Number(gravityInput.value) / 1000;
    const origin = { x: width / 2, y: 45 };
    const accel = -gravity * Math.sin(angle);
    velocity += accel;
    velocity *= 0.995;
    angle += velocity;
    const bob = { x: origin.x + Math.sin(angle) * length, y: origin.y + Math.cos(angle) * length };
    ctx.clearRect(0, 0, width, height);
    ctx.strokeStyle = "rgba(255,255,255,.16)";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(origin.x, origin.y);
    ctx.lineTo(bob.x, bob.y);
    ctx.stroke();
    ctx.fillStyle = "#a66cff";
    ctx.shadowColor = "#a66cff";
    ctx.shadowBlur = 22;
    ctx.beginPath();
    ctx.arc(bob.x, bob.y, 18, 0, Math.PI * 2);
    ctx.fill();
    ctx.shadowBlur = 0;
    requestAnimationFrame(draw);
  };
  draw();
}

const lensCanvas = document.getElementById("lensCanvas");
if (lensCanvas) {
  const lab = setupCanvas(lensCanvas);
  const objectInput = document.getElementById("lensObject");
  const focalInput = document.getElementById("lensFocal");
  const readout = document.getElementById("lensReadout");
  const draw = () => {
    const { ctx, size } = lab;
    const { width, height } = size();
    const center = width / 2;
    const axis = height / 2;
    const objectDistance = Number(objectInput.value);
    const focal = Number(focalInput.value);
    const imageDistance = 1 / ((1 / focal) - (1 / objectDistance));
    const magnification = -imageDistance / objectDistance;
    ctx.clearRect(0, 0, width, height);
    ctx.strokeStyle = "rgba(255,255,255,.2)";
    ctx.beginPath();
    ctx.moveTo(20, axis);
    ctx.lineTo(width - 20, axis);
    ctx.stroke();
    ctx.strokeStyle = "#55d7ff";
    ctx.lineWidth = 5;
    ctx.beginPath();
    ctx.moveTo(center, 45);
    ctx.quadraticCurveTo(center + 24, axis, center, height - 45);
    ctx.quadraticCurveTo(center - 24, axis, center, 45);
    ctx.stroke();
    const objectX = center - objectDistance;
    const imageX = center + Math.max(-400, Math.min(400, imageDistance));
    const objectH = 90;
    const imageH = objectH * magnification;
    ctx.strokeStyle = "#6cf0b6";
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(objectX, axis);
    ctx.lineTo(objectX, axis - objectH);
    ctx.stroke();
    ctx.strokeStyle = "#a66cff";
    ctx.beginPath();
    ctx.moveTo(imageX, axis);
    ctx.lineTo(imageX, axis - imageH);
    ctx.stroke();
    ctx.strokeStyle = "rgba(85,215,255,.6)";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(objectX, axis - objectH);
    ctx.lineTo(center, axis - objectH);
    ctx.lineTo(imageX, axis - imageH);
    ctx.moveTo(objectX, axis - objectH);
    ctx.lineTo(center, axis);
    ctx.lineTo(imageX, axis - imageH);
    ctx.stroke();
    readout.textContent = Number.isFinite(imageDistance)
      ? `Image distance: ${imageDistance.toFixed(1)} px | magnification: ${magnification.toFixed(2)}`
      : "Image at infinity";
    requestAnimationFrame(draw);
  };
  draw();
}

const spectrumOrb = document.getElementById("spectrumOrb");
if (spectrumOrb) {
  const red = document.getElementById("redMix");
  const green = document.getElementById("greenMix");
  const blue = document.getElementById("blueMix");
  const readout = document.getElementById("spectrumReadout");
  const update = () => {
    const color = `rgb(${red.value}, ${green.value}, ${blue.value})`;
    spectrumOrb.style.background = color;
    spectrumOrb.style.boxShadow = `0 0 80px ${color}`;
    readout.textContent = color;
  };
  [red, green, blue].forEach((input) => input.addEventListener("input", update));
  update();
}
