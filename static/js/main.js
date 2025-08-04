
let form = document.querySelector('form')
let select = document.querySelector('select')
let input = document.querySelector('input')
let shiftDiv = document.querySelector('.shift')

function setValuesAsBefore() {
    let selected = document.querySelector('select')
    selected.value = selected.value
}

// Save the selected value before form submits
form.addEventListener('submit', function () {
  localStorage.setItem('query', this.elements[0].value)
  localStorage.setItem('selectedValue', this.elements[1].value);
});

// Restore previously selected value from localStorage
window.addEventListener('DOMContentLoaded', () => {
  let savedValue = localStorage.getItem('selectedValue');
  let query = localStorage.getItem('query');

  if (savedValue, query) {
    form.elements[0].value = query
    form.elements[1].value = savedValue;
  }
});


select.addEventListener('change', function () {
  if (select.value === 'shift') {
    shiftDiv.classList.remove('dp-none');
  } else {
    shiftDiv.classList.add('dp-none');
  }
});


