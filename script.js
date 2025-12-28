// ================================
// SMOOTH PAGE LOAD ANIMATIONS
// ================================

window.addEventListener("load", () => {

  // Fade in sections
  document.querySelectorAll(".section").forEach((section, index) => {
    section.style.opacity = "0";
    section.style.transform = "translateY(40px)";
    section.style.transition =
      "opacity 0.8s ease-out, transform 0.8s ease-out";

    setTimeout(() => {
      section.style.opacity = "1";
      section.style.transform = "translateY(0)";
    }, index * 120);
  });

  // Enhance card hover depth
  document.querySelectorAll(".card").forEach(card => {
    card.addEventListener("mouseenter", () => {
      card.style.transform = "translateY(-12px) scale(1.02)";
    });

    card.addEventListener("mouseleave", () => {
      card.style.transform = "translateY(0) scale(1)";
    });
  });

});
