document.addEventListener('DOMContentLoaded', function() {
    var rangeInput = document.getElementById('summaryLength');
    var selectedLengthDisplay = document.getElementById('selectedLength');

    rangeInput.addEventListener('input', function() {
        selectedLengthDisplay.innerText = rangeInput.value;
    });
});