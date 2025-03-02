document.getElementById("search").addEventListener("input", function () {
    let query = this.value.toLowerCase();
    let articles = document.querySelectorAll(".note");

    articles.forEach(article => {
        if (article.textContent.toLowerCase().includes(query)) {
            article.style.display = "block";
        } else {
            article.style.display = "none";
        }
    });
});
