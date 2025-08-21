document.addEventListener('DOMContentLoaded', () => {
    const integrityCheck = document.getElementById("integrity");
    const hashInput = document.querySelectorAll(".hash");
    const text = document.getElementById("text-input");
    const fileElement = document.querySelectorAll(".file-element");
    const integrityElement = document.querySelectorAll(".integrity-element");
    const textareaElement = document.querySelectorAll(".textarea-element");
    const btn = document.querySelector(".btn-element");
    const resetBtn = document.querySelector(".reset-btn")

    // hiding all the elment if the user enter in textarea
    text.addEventListener('input', function () {
        const textValueEmpty = this.value.trim() !== "";

        // hiding File input box
        fileElement.forEach(element => {
            if (textValueEmpty) {
                element.classList.add('hidden');
            } else {
                element.classList.remove('hidden');
            }
        });

        // hiding integrity checkbox
        integrityElement.forEach(element => {
            if (textValueEmpty) {
                element.classList.add('hidden')

            }
            else {
                element.classList.remove('hidden')
            }
        })

        // hinding integrity input box
        hashInput.forEach(element => {
            if (textValueEmpty) {
                element.classList.add('hidden')
            }
            else {
                element.classList.remove('hidden')
            }
        })

        if (textValueEmpty) {
            integrityElement[0].checked = false
            integrityCheck.dispatchEvent(new Event('change'));


        }

    });


    // hiding textarea and rm-file-label if the user added the file 
    fileElement[1].addEventListener('change', function () {
        const fileValueEmpty = this.value == "";
        textareaElement.forEach(element => {
            if (fileValueEmpty) {
                element.classList.remove('hidden');

            } else {
                element.classList.add('hidden');
            }
        })
    });

    // implement reset button
    resetBtn.addEventListener("click", function () {
        fileElement[1].value = "";
        fileElement[1].dispatchEvent(new Event('change'));
        text.value = "";
        text.dispatchEvent(new Event('input'));

        // triggering event for integrity input box
        integrityCheck.dispatchEvent(new Event('change'));

    })




    // changing the btn text if user tick the check integrity
    // add hash input box if user enable Check Integrity checkbox else hide it
    integrityCheck.addEventListener('change', function () {
        hashInput.forEach(input => {
            if (this.checked) {
                btn.textContent = "Check Integrity"
                input.classList.remove('hidden');

            }
            else {
                btn.textContent = "Generate Hashes"
                input.classList.add('hidden');

            }
        })

    });

})  