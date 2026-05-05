const revealElements = document.querySelectorAll(".reveal-on-scroll");

if (revealElements.length > 0) {
  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("in-view");
      observer.unobserve(entry.target);
    });
  }, {
    root: null,
    threshold: 0.16,
    rootMargin: "0px 0px -30px 0px"
  });

  revealElements.forEach((element) => revealObserver.observe(element));
}
