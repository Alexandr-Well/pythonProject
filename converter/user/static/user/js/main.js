const spinnerBox = document.getElementById('spinner-box')
const btn = document.getElementById('btn-id')
const form = document.getElementById('form-id')
const fileBox = document.getElementById('user-form')
const name = document.getElementsByName('file')

name[0].addEventListener('change', () => {
    if (name[0].value) {
        btn.addEventListener('click', () => {
            spinnerBox.classList.remove('not-visible')
            form.classList.add('not-visible')

        });
    }
});