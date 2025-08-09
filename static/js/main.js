document.addEventListener('DOMContentLoaded', () => {
    const cipherForm = document.getElementById('cipher-form');
    const algoSelect = document.getElementById('algo-select');
    const keywordGroup = document.getElementById('keyword-group');
    const shiftGroup = document.getElementById('shift-group');
    const cipherAlphabetsGroup = document.getElementById('cipher-alphabets-group');
    const textInput = document.getElementById('text-input');

    // Function to toggle visibility of conditional form groups
    const toggleConditionalFields = () => {
        const selectedAlgo = algoSelect.value;
        keywordGroup.style.display = selectedAlgo === 'mixed_alphabet' ? 'flex' : 'none';
        shiftGroup.style.display = selectedAlgo === 'shift' ? 'flex' : 'none';
        cipherAlphabetsGroup.style.display = selectedAlgo === 'simple_substitution' ? 'flex' : 'none';
    };

    // Event listener for algorithm selection change
    algoSelect.addEventListener('change', toggleConditionalFields);

    // Save form state to localStorage before submission
    cipherForm.addEventListener('submit', () => {
        localStorage.setItem('selectedAlgo', algoSelect.value);
        localStorage.setItem('textInputValue', textInput.value);
    });

    // Restore form state on page load
    const savedAlgo = localStorage.getItem('selectedAlgo');
    const savedText = localStorage.getItem('textInputValue');

    if (savedAlgo) {
        algoSelect.value = savedAlgo;
    }

    if (savedText) {
        textInput.value = savedText;
    }

    // Initial check to set the correct form fields visibility
    toggleConditionalFields();
});