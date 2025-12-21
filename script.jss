// Simple scroll reveal (guaranteed to work)

const revealItems = document.querySelectorAll(
  ".section, .card, .timeline-item"
);

function revealOnScroll() {
  const windowHeight = window.innerHeight;

  revealItems.forEach(item => {
    const elementTop = item.getBoundingClientRect().top;

    if (elementTop < windowHeight - 100) {
      item.classList.add("reveal-active");
    }
  });
}

window.addEventListener("scroll", revealOnScroll);
window.addEventListener("load", revealOnScroll);
