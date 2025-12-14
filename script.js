function checkLink() {
    const url = document.getElementById("urlInput").value;

    fetch("/check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url })
    })
    .then(res => res.json())
    .then(data => {
        
        document.getElementById("result").style.display = "block";

        const badge = document.getElementById("statusBadge");
        const summary = document.getElementById("summaryText");
        const list = document.getElementById("issueList");

        list.innerHTML = ""; // Clear old list

        if (data.safe) {
            badge.className = "badge safeBadge";
            badge.innerText = "🟢 SAFE LINK";
        } else {
            badge.className = "badge dangerBadge";
            badge.innerText = "🔴 WARNING";
        }

        summary.innerText = data.summary;

        data.issues.forEach(issue => {
            const li = document.createElement("li");
            li.innerText = issue;
            list.appendChild(li);
        });

    });
}
