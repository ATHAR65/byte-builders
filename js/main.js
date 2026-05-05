const header = document.querySelector(".site-header");
const navToggle = document.querySelector(".nav-toggle");
const mobileMenu = document.querySelector(".mobile-menu");
const page = document.body.dataset.page;
const cursorDot = document.querySelector(".cursor-dot");

if (header && !header.classList.contains("solid-header")) {
  const onScroll = () => {
    header.classList.toggle("scrolled", window.scrollY > 80);
  };
  onScroll();
  window.addEventListener("scroll", onScroll);
}

if (navToggle && mobileMenu) {
  navToggle.addEventListener("click", () => {
    const isOpen = mobileMenu.classList.toggle("open");
    navToggle.setAttribute("aria-expanded", String(isOpen));
  });

  mobileMenu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      mobileMenu.classList.remove("open");
      navToggle.setAttribute("aria-expanded", "false");
    });
  });
}

document.querySelectorAll("[data-link]").forEach((link) => {
  if (link.dataset.link === page) link.classList.add("active");
});

const counters = document.querySelectorAll(".counter");
if (counters.length > 0) {
  const counterObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      const target = Number(el.dataset.target || 0);
      const duration = 1200;
      const start = performance.now();

      const tick = (now) => {
        const progress = Math.min((now - start) / duration, 1);
        el.textContent = String(Math.floor(target * progress));
        if (progress < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
      observer.unobserve(el);
    });
  }, { threshold: 0.5 });

  counters.forEach((counter) => counterObserver.observe(counter));
}

const track = document.getElementById("testimonial-track");
if (track) {
  let autoplay;
  const start = () => {
    autoplay = setInterval(() => {
      track.scrollBy({ left: 310, behavior: "smooth" });
      if (track.scrollLeft + track.clientWidth >= track.scrollWidth - 20) {
        track.scrollTo({ left: 0, behavior: "smooth" });
      }
    }, 3200);
  };
  const stop = () => clearInterval(autoplay);
  track.addEventListener("mouseenter", stop);
  track.addEventListener("mouseleave", start);
  start();
}

if (cursorDot && window.matchMedia("(pointer:fine)").matches) {
  cursorDot.style.display = "block";
  window.addEventListener("mousemove", (event) => {
    cursorDot.style.left = `${event.clientX}px`;
    cursorDot.style.top = `${event.clientY}px`;
  });
}

const contactForm = document.querySelector("form[name='project-inquiry']");
if (contactForm) {
  const isLocalPreview = ["localhost", "127.0.0.1"].includes(window.location.hostname);
  if (isLocalPreview) {
    // Local static servers cannot process POST forms, so we simulate success.
    contactForm.addEventListener("submit", (event) => {
      event.preventDefault();
      window.location.href = "thank-you.html";
    });
  }
}
