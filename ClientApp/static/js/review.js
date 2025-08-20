let cards = document.querySelectorAll(".carousel-card");
    let current = 0;

    function showCards() {
      cards.forEach((card, i) => {
        card.classList.remove("active", "prev", "next");
        if (i === current) {
          card.classList.add("active");
        } else if (i === current - 1) {
          card.classList.add("prev");
        } else if (i === current + 1) {
          card.classList.add("next");
        }
      });
    }

    function nextCard() {
      current++;
      if (current >= cards.length) current = 0;
      showCards();
    }

    // init
    showCards();
    setInterval(nextCard, 3000);