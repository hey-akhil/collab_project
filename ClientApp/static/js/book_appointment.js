document.addEventListener("DOMContentLoaded", function () {
  const serviceSelect = document.getElementById("service");
  const datetimeInput = document.getElementById("datetime");

  const overviewService = document.getElementById("overview-service");
  const overviewPrice = document.getElementById("overview-price");
  const overviewDatetime = document.getElementById("overview-datetime");

  // Update service & price
  serviceSelect.addEventListener("change", function () {
    const selectedOption = serviceSelect.options[serviceSelect.selectedIndex];
    overviewService.textContent = selectedOption.value;
    overviewPrice.textContent = "$" + selectedOption.getAttribute("data-price");
  });

  // Update date & time
  datetimeInput.addEventListener("change", function () {
    overviewDatetime.textContent = new Date(datetimeInput.value).toLocaleString();
  });

  // Initialize default values
  serviceSelect.dispatchEvent(new Event("change"));
});