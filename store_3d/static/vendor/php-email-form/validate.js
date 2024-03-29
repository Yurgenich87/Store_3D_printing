(function () {
  "use strict";

  let forms = document.querySelectorAll('.php-email-form');

  forms.forEach(function (e) {
    e.addEventListener('submit', function (event) {
      event.preventDefault();

      let thisForm = this;

      let action = thisForm.getAttribute('action');

      if (!action) {
        displayError(thisForm, 'The form action property is not set!');
        return;
      }
      thisForm.querySelector('.loading').classList.add('d-block');
      thisForm.querySelector('.error-message').classList.remove('d-block');
      thisForm.querySelector('.sent-message').classList.remove('d-block');

      let formData = new FormData(thisForm);

      php_email_form_submit(thisForm, action, formData);
    });
  });

  function php_email_form_submit(thisForm, action, formData) {
    fetch(action, {
      method: 'POST',
      body: formData,
      headers: {'X-Requested-With': 'XMLHttpRequest'}
    })
    .then(response => {
        if (response.ok) {
            console.info('response.ok');
            return response.json();
            // Парсим JSON-ответ
        } else {
            console.info('response -> else');
            throw new Error(`${response.status} ${response.statusText} ${response.url}`);
        }
    })
    .then(data => {
        console.info('data:', data);
        if (data.success) {
            thisForm.querySelector('.sent-message').classList.add('d-block');
            thisForm.querySelector('.loading').classList.remove('d-block'); // Убираем состояние загрузки
            // Опционально: сбросить поля формы
            thisForm.reset();
            // Скрыть сообщение об успешной отправке через 5 секунд
            setTimeout(() => {
              thisForm.querySelector('.sent-message').classList.remove('d-block');
            }, 5000);
        } else {
            console.info('data -> else');
            throw new Error(data.message); // Бросаем ошибку, если отправка не удалась
        }
    })
    .catch((error) => {
        displayError(thisForm, error);
        thisForm.querySelector('.loading').classList.remove('d-block'); // Убираем состояние загрузки в случае ошибки
      });

  }

  function displayError(thisForm, error) {
    thisForm.querySelector('.loading').classList.remove('d-block');
    thisForm.querySelector('.error-message').innerHTML = error;
    thisForm.querySelector('.error-message').classList.add('d-block');
  }

})();
