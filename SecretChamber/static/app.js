function search() {
    const q = document.getElementById("searchBox").value;

    fetch("/search?q=" + encodeURIComponent(q))
        .then(r => r.json())
        .then(d => {
            document.getElementById("searchResult").textContent =
                JSON.stringify(d, null, 2);
        });
}

function checkStatus() {
    fetch("/api/status")
        .then(r => r.json())
        .then(d => {
            document.getElementById("statusResult").textContent =
                JSON.stringify(d, null, 2);
        });

    fetch("/vault", {
        headers: {
            "Authorization": "Bearer " + localStorage.getItem("token")
        }
    }).catch(() => {});
}


// token logic migrated
// assets optimized
// legacy admin tokens deprecated
