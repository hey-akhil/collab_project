 // Function to animate numbers
  function animateCounters() {
    const counters = document.querySelectorAll('.counter');
    const speed = 500; // smaller = faster

    counters.forEach(counter => {
      const updateCount = () => {
        const target = +counter.getAttribute('data-target');
        const count = +counter.innerText;
        const increment = target / speed;

        if (count < target) {
          counter.innerText = Math.ceil(count + increment);
          setTimeout(updateCount, 5);
        } else {
          counter.innerText = target.toLocaleString(); // format with commas
        }
      };

      updateCount();
    });
  }

  // Run when section is visible (using IntersectionObserver)
  const statsSection = document.querySelector('.stats-section');
  const observer = new IntersectionObserver(entries => {
    if (entries[0].isIntersecting) {
      animateCounters();
      observer.disconnect(); // run only once
    }
  }, { threshold: 0.5 });

  observer.observe(statsSection);