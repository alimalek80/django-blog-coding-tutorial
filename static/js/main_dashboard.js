// Activate tab based on URL fragment (e.g., #security)
document.addEventListener('DOMContentLoaded', function () {
    const hash = window.location.hash;

    console.log("Current Hash:", hash); // Debugging

    if (hash) {
        const tabTrigger = document.querySelector(`a[href="${hash}"]`);
        if (tabTrigger) {
            new bootstrap.Tab(tabTrigger).show();
            console.log("Activated tab:", hash);
        } else {
            console.warn("No matching tab found for hash:", hash);
        }
    }
});