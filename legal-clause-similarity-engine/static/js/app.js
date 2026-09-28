document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    if (!form) return;

    form.addEventListener('submit', function (event) {
        const input = document.querySelector('input[name="query"]');
        if (!input || !input.value.trim()) {
            event.preventDefault();
            alert('Please enter a clause to search.');
        }
    });
});
