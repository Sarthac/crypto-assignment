document.addEventListener('DOMContentLoaded', () => {
    const cipherForm = document.getElementById('cipher-form');
    const algoSelect = document.getElementById('algo-select');
    const keywordGroup = document.getElementById('keyword-group');
    const keyword = document.getElementById('keyword-input');

    const keyGroup = document.getElementById('key-group')
    const shiftGroup = document.getElementById('shift-group');
    const cipherAlphabetsGroup = document.getElementById('cipher-alphabets-group');
    const textInput = document.getElementById('text-input');

    const keyword_base_algorithm = new Set(["mixed_alphabet", "alberti", "vigenere", "beaufort", "autokey"]);
    // Function to toggle visibility of conditional form groups
    const toggleConditionalFields = () => {
        const selectedAlgo = algoSelect.value;
        keywordGroup.style.display = (keyword_base_algorithm.has(selectedAlgo)) ? 'block' : 'none';
        shiftGroup.style.display = selectedAlgo === 'shift' ? 'block' : 'none';
        cipherAlphabetsGroup.style.display = selectedAlgo === 'simple_substitution' ? 'block' : 'none';
    };

    // Event listener for algorithm selection change
    algoSelect.addEventListener('change', toggleConditionalFields);

    // Initial check to set the correct form fields visibility
    toggleConditionalFields();
});