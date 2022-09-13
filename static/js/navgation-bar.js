const items = document.querySelectorAll(".nav-item");

function addid() {
  for (let i = 0; i < items.length; i++) {
    items[i].id = `${i}`;
  }
}

for (const item of items) {
  item.addEventListener("click", function (event) {
    console.log(item.id);
  });
}
