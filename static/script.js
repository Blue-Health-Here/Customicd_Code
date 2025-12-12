// document.addEventListener("DOMContentLoaded", () => {
//   const input = document.getElementById("medication-input");
//   const icdBox = document.getElementById("icd10-buttons");
//   const icdField = document.getElementById("icd10-code");

//   input.addEventListener("input", () => {
//     const query = input.value.trim();
//     icdBox.innerHTML = "";
//     if (query.length < 3) return;

//     fetch(`/get_icd10_codes?medication=${encodeURIComponent(query)}`)
//       .then(res => res.json())
//       .then(data => {
//         data.forEach(code => {
//           const btn = document.createElement("button");
//           btn.type = "button";
//           btn.classList.add("icd10-btn");
//           btn.textContent = code;
//           btn.onclick = () => {
//             icdField.value = code;
//             icdBox.innerHTML = "";
//           };
//           icdBox.appendChild(btn);
//         });
//       });
//   });
// });





document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("medication-input");
  const icdBox = document.getElementById("icd10-buttons");
  const icdField = document.getElementById("icd10-code");
  const descField = document.getElementById("icd10-desc"); // may be null if you skipped it

  input.addEventListener("input", () => {
    const query = input.value.trim();
    icdBox.innerHTML = "";
    if (query.length < 3) return;

    fetch(`/get_icd10_codes?medication=${encodeURIComponent(query)}`)
      .then(res => res.json())
      .then(items => {
        icdBox.innerHTML = "";
        items.forEach(({ code, description }) => {
          const btn = document.createElement("button");
          btn.type = "button";
          btn.classList.add("icd10-btn");
          // Show code + description on the chip
          btn.textContent = description ? `${code} — ${description}` : code;

          btn.onclick = () => {
            icdField.value = code;
            if (descField) descField.value = description || "";
            icdBox.innerHTML = "";
          };

          icdBox.appendChild(btn);
        });
      })
      .catch(console.error);
  });
});
