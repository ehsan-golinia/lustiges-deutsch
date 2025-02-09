function red_green(answer, german) {
    let h4 = document.createElement('h4');
    for (let i = 0; i < german.length; i++) {
        let span = document.createElement('span');
        span.textContent = german.charAt(i);
        if (answer.charAt(i) === german.charAt(i)) {
            span.classList.add('text-success');
        } else {
            span.classList.add('text-danger');
        }
        h4.appendChild(span);
        }
    return h4;
}