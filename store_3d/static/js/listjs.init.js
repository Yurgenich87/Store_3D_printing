function createProduct(productData) {
    // Получаем CSRF-токен из cookie
    const csrftoken = getCookie('csrftoken');

    // Создаем новый объект FormData
    const formData = new FormData();

    // Добавляем текстовые данные в FormData
    formData.append('name', productData.name);
    formData.append('price', productData.price);
    formData.append('quantity', productData.quantity);
    formData.append('description', productData.description);

    // Если изображение было выбрано, добавляем его в FormData
    if (productData.image) {
        formData.append('image', productData.image);
    }

    // Опции для запроса
    const requestOptions = {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: formData // Используем FormData в качестве тела запроса
    };

    // Отправляем POST-запрос на создание продукта
    fetch('/create_product/', requestOptions)
        .then(response => {
            if (!response.ok) {
                throw new Error('Сетевой ответ не был успешным');
            }
            return response.json();
        })
        .then(data => {
                console.log('Продукт успешно создан:', data);
                $('#showModal').modal('hide'); // Скрыть модальное окно

                // Показать уведомление об успешном создании продукта
                showNotification('Продукт успешно создан.');
            })
        .catch(error => {
                console.error('Ошибка при создании продукта:', error);
            });
}

function updateData(productId, updatedData) {
    // Получаем CSRF-токен из cookie
    const csrftoken = getCookie('csrftoken');

    // Создаем новый объект FormData
    const formData = new FormData();

    // Добавляем текстовые данные в FormData
    formData.append('name', updatedData.name);
    formData.append('price', updatedData.price);
    formData.append('quantity', updatedData.quantity);
    formData.append('description', updatedData.description);

    // Если изображение было выбрано, добавляем его в FormData
    if (updatedData.image) {
        formData.append('image', updatedData.image);
    }

    // Опции для запроса
    const requestOptions = {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: formData // Используем FormData в качестве тела запроса
    };

    fetch(`/update_product/${productId}/`, requestOptions)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Data updated successfully:', data);
            $('#showModal').modal('hide');
            showNotification('Продукт успешно обновлен.');
        })
        .catch(error => {
            console.error('Error updating data:', error);
        });
}


function deleteProduct(productId) {
    const csrftoken = getCookie('csrftoken');

    // Опции для запроса
    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
    };

    fetch(`/delete_product/${productId}/`, requestOptions)
        .then(response => {
            if (!response.ok) {
                throw new Error('Сетевой ответ не был успешным');
            }
        showNotification('Продукт успешно удален.');

        })
        .catch(error => {
            console.error('Ошибка при удалении продукта:', error);
        });
}

function showNotification(message) {
    console.log('showNotification:', message);

    // Создаем элемент для сообщения
    let notificationElement = document.createElement('div');
    notificationElement.textContent = message;

    // Находим элемент для отображения уведомления
    let updateSuccessMessage = document.getElementById('update-success-message');

    // Добавляем сообщение внутрь элемента "update-success-message"
    updateSuccessMessage.innerHTML = ''; // Очищаем содержимое, если уже что-то было
    updateSuccessMessage.appendChild(notificationElement);

    console.log('showNotification start: ', notificationElement);

    // Показываем элемент с уведомлением
    updateSuccessMessage.style.display = 'block';

    // Скрываем сообщение через некоторое время
    setTimeout(function() {
        notificationElement.remove(); // Удаляем элемент из DOM
        updateSuccessMessage.style.display = 'none'; // Скрываем элемент с уведомлением
    }, 4000); // 3000 миллисекунд (3 секунды)

    // Создаем обещание для обновления страницы через 3 секунды
    const reloadPromise = new Promise(resolve => {
        setTimeout(() => {
            resolve(location.reload());
        }, 1000);
    });

    // Возвращаем обещание
    return reloadPromise;
}

function showToast(message, duration = 4000) {
    const toast = document.createElement('div');
    toast.classList.add('toast');
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');

    const toastHeader = document.createElement('div');
    toastHeader.classList.add('toast-header');

    const toastBody = document.createElement('div');
    toastBody.classList.add('toast-body');
    toastBody.textContent = message;

    toast.appendChild(toastHeader);
    toast.appendChild(toastBody);

    document.querySelector('.toast-container').appendChild(toast);

    const bootstrapToast = new bootstrap.Toast(toast);
    bootstrapToast.show();

    setTimeout(() => {
        toast.remove(); // Удаляем уведомление из DOM
    }, duration);


}
// function updateRemoveButton(productId, quantity) {
//     const removeButtons = document.querySelectorAll('.remove-from-cart-btn');
//     removeButtons.forEach(button => {
//         if (button.getAttribute('data-product-id') === productId) {
//             button.textContent = `Удалить из корзины: ${quantity} шт.`;
//         }
//     });
// }


function updateTableData(days) {
    filterProducts(days);
}

function displayFilteredData(filteredData) {
    var tableBody = document.getElementById('customerTable').getElementsByTagName('tbody')[0];
    tableBody.innerHTML = '';

    filteredData.forEach(function(product) {
        var newRow = tableBody.insertRow();
        newRow.innerHTML = `
            <td class="id">${product.id}</td>
            <td class="name">${product.name}</td>
            <td class="price">${product.price}</td>
            <td class="quantity">${product.quantity}</td>
            <td class="description">${product.description}</td>
            <td class="at_data">${product.at_data}</td>
            <td>
                <div class="d-flex gap-2">
                    <div class="edit">
                        <button type="button" class="blue edit-item-btn" data-bs-toggle="modal" data-bs-target="#showModal" data-product-id="${product.id}" onclick="editProduct(${product.id})">Редактировать</button>
                    </div>
                    <div class="remove">
                        <button type="button" class="red remove-item-btn" data-bs-toggle="modal" data-bs-target="#deleteRecordModal" data-product-id="${product.id}">Удалить</button>
                    </div>
                </div>
            </td>
        `;
    });
}

function filterProducts(days) {
    fetch(`/filter_products/${days}/`)
        .then(response => {
            if (response.ok) {
                return response.text();
                console.error('days:', days);

            }
            throw new Error('Ошибка при получении данных');
        })
        .then(html => {
            // Обновить содержимое страницы с отфильтрованным списком товаров
            document.querySelector('body').innerHTML = html;
            console.info('days:', days);
        })
        .catch(error => console.error('Ошибка при фильтрации товаров:', error));
}

function filterProductsInCart(days) {
    fetch(`/filter_products_in_cart/${days}/`)
        .then(response => {
            if (response.ok) {
                return response.text();
            }
            throw new Error('Ошибка при получении данных');
        })
        .then(html => {
            // Обновить содержимое страницы с отфильтрованным списком товаров в корзине
            document.querySelector('body').innerHTML = html;
        })
        .catch(error => console.error('Ошибка при фильтрации товаров в корзине:', error));
}

function filterOrders(days) {
    fetch(`/filter_order/${days}/`)
        .then(response => {
            if (response.ok) {
                return response.text();
            }
            throw new Error('Ошибка при получении данных');
        })
        .then(html => {
            // Обновить содержимое страницы с отфильтрованным списком заказов
            document.querySelector('body').innerHTML = html;
        })
        .catch(error => console.error('Ошибка при фильтрации заказов:', error));
}

function resetFilter() {
    // Сбросить фильтр, например, перезагрузить страницу
    window.location.reload();
}

function applyCustomDaysFilter(type) {
    var value = document.getElementById('customDaysInput').value;
    if (value === 'reset') {
        resetFilter();
    } else {
        if (type === 'cart') {
            filterProductsInCart(value);
        } else if (type === 'order') {
            filterOrders(value);
        } else {
            filterProducts(value);
        }
    }
}

function handleFilterChange(value, type) {
    if (value === 'reset') {
        resetFilter();
    console.error('value:', value, 'type', type );

    } else {
        if (type === 'cart') {
            filterProductsInCart(value);
        } else if (type === 'order') {
            filterOrders(value);
        } else {
            filterProducts(value);
        }
    }
}

function updateCartItemCount(count) {
    const cartItemCountElement = document.getElementById('cartItemCount');
    if (cartItemCountElement) {
        cartItemCountElement.textContent = count;
    }
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Находим все кнопки увеличения и уменьшения количества товара
const increaseButtons = document.querySelectorAll('.SnowShoppingcartProductList_ProductNumAction__button__eac55:first-child');
const decreaseButtons = document.querySelectorAll('.SnowShoppingcartProductList_ProductNumAction__button__eac55:last-child');

// Добавляем обработчики событий для кнопок увеличения и уменьшения количества товара
increaseButtons.forEach(button => {
    button.addEventListener('click', function() {
        // Находим элемент с количеством товара
        const quantityElement = this.parentElement.querySelector('.SnowShoppingcartProductList_ProductNumAction__quantity__eac55');
        // Увеличиваем количество товара на 1
        const newQuantity = parseInt(quantityElement.textContent) + 1;
        // Обновляем количество товара на странице
        quantityElement.textContent = newQuantity;
    });
});

decreaseButtons.forEach(button => {
    button.addEventListener('click', function() {
        // Находим элемент с количеством товара
        const quantityElement = this.parentElement.querySelector('.SnowShoppingcartProductList_ProductNumAction__quantity__eac55');
        // Уменьшаем количество товара на 1, но не меньше 1
        const newQuantity = Math.max(parseInt(quantityElement.textContent) - 1, 1);
        // Обновляем количество товара на странице
        quantityElement.textContent = newQuantity;
    });
});



const csrfToken = "{{ csrf_token }}";
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
let currentProductId = null;
var datepicker = new Datepicker('#datepicker');


document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("showModal") && (document.getElementById("showModal").addEventListener("show.bs.modal", function(e) {
        if (e.relatedTarget.classList.contains("edit-item-btn")) {
            document.getElementById("exampleModalLabel").innerHTML = "Редактирование товара";
            document.getElementById("showModal").querySelector(".modal-footer").style.display = "block";
            document.getElementById("add-btn").style.display = "none";
            document.getElementById("edit-btn").style.display = "block";

            // Устанавливаем текущий productId
            currentProductId = e.relatedTarget.dataset.productId;


            // Fetch product data using AJAX
            let productId = currentProductId; // Передаем текущий productId

            fetch(`/products_list/`)
                .then(response => response.json())
                .then(data => {
                    let product = data.find(item => item.id === parseInt(productId));
                    document.getElementById("name").value = product.name;
                    document.getElementById("price").value = product.price;
                    document.getElementById("quantity").value = product.quantity;
                    document.getElementById("description").value = product.description;

                })
                .catch(error => console.error('Error fetching product details:', error));
        } else if (e.relatedTarget.classList.contains("add-btn")) {
            document.getElementById("exampleModalLabel").innerHTML = "Добавление товара";
            document.getElementById("showModal").querySelector(".modal-footer").style.display = "block";
            document.getElementById("edit-btn").style.display = "none";
            document.getElementById("add-btn").style.display = "block";
        } else {

            document.getElementById("exampleModalLabel").innerHTML = "Редактирование товара";
            document.getElementById("showModal").querySelector(".modal-footer").style.display = "none";
        }
    }));


    // Добавляем обработчик события клика на кнопку "Добавить товар"
    document.getElementById("add-btn").addEventListener("click", function(event) {
        event.preventDefault();

        // Получаем данные из полей модального окна
        let name = document.getElementById("name").value;
        let price = document.getElementById("price").value;
        let quantity = document.getElementById("quantity").value;
        let description = document.getElementById("description").value;

        // Получаем файл изображения, если он был выбран пользователем
        let imageInput = document.getElementById("image");
        let image = null;
        if (imageInput.files.length > 0) {
            image = imageInput.files[0];
        }

        // Формируем объект с данными о новом продукте
        let newProductData = {
            name: name,
            price: price,
            quantity: quantity,
            description: description,
            image: image  // Добавляем информацию об изображении в объект данных
        };

        // Вызываем функцию для отправки данных на сервер для создания товара
        createProduct(newProductData);
    });

    // Добавляем обработчик события клика на кнопку "Обновить"
    document.getElementById("edit-btn").addEventListener("click", function(event) {
        event.preventDefault();

        // Получаем ID текущего товара
        let productId = currentProductId;

        // Получаем данные из полей модального окна
        let name = document.getElementById("name").value;
        let price = document.getElementById("price").value;
        let quantity = document.getElementById("quantity").value;
        let description = document.getElementById("description").value;

        // Получаем файл изображения, если он был выбран пользователем
        let imageInput = document.getElementById("image");
        let image = null;
        if (imageInput.files.length > 0) {
            image = imageInput.files[0];
        }

        // Формируем объект с обновленными данными
        let updatedData = {
            name: name,
            price: price,
            quantity: quantity,
            description: description
        };

        // Если изображение было выбрано, добавляем его в объект с данными
        if (image) {
            updatedData['image'] = image;
        }

        // Вызываем функцию для отправки обновленных данных на сервер
        updateData(productId, updatedData);
    });


    // Добавляем обработчик события, который вызывается при открытии модального окна
    $('#deleteRecordModal').on('show.bs.modal', function (event) {
        // Находим кнопку "Удалить" внутри модального окна
        const deleteButton = document.getElementById('delete-record');
        // Получаем идентификатор продукта из кнопки "Удалить", которая была нажата для открытия модального окна
        const productId = event.relatedTarget.getAttribute('data-product-id');
        // Устанавливаем атрибут data-product-id для кнопки "Да, удалить!"
        deleteButton.setAttribute('data-product-id', productId);

        // Назначаем обработчик события клика на кнопку "Да, удалить!"
        deleteButton.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            console.log("Идентификатор товара для удаления:", productId);
            deleteProduct(productId);
        });
    });

    // Функция для очистки полей модального окна при его скрытии
    document.getElementById("showModal").addEventListener("hidden.bs.modal", function() {
        document.getElementById("name").value = "";
        document.getElementById("price").value = "";
        document.getElementById("quantity").value = "";
        document.getElementById("description").value = "";

        // Сбрасываем текущий productId
        currentProductId = null;
    });

});


// Обработка нажатия на кнопку "Добавить в корзину"
    document.querySelectorAll('.add-to-cart-btn').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            const csrftoken = getCookie('csrftoken');

            fetch(`/add_to_cart/${productId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({ product_id: productId })
            })
            .then(response => response.json())
            .then(data => {
                // Обновление информации о корзине на странице
                const cartItemCountElement = document.getElementById('cartItemCount');
                if (cartItemCountElement) {
                    cartItemCountElement.textContent = data.cartItemCount;
                }
                location.reload();
                // Например, показать уведомление об успешном добавлении товара в корзину
                showToast('Товар успешно добавлен в корзину');
            })
            .catch(error => {
                console.error('Ошибка при добавлении товара в корзину:', error);
                // Обработка ошибки, если не удалось добавить товар в корзину
                showToast('Ошибка при добавлении товара в корзину. Пожалуйста, попробуйте еще раз.');
            });
        });
    });


// Обработка нажатия на кнопку "Удалить из корзины"
document.querySelectorAll('.remove-from-cart-btn').forEach(button => {
    button.addEventListener('click', function() {
        const productId = this.getAttribute('data-product-id');
        const csrftoken = getCookie('csrftoken');

        // AJAX запрос на удаление товара из корзины
        fetch(`/remove_from_cart/${productId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
        })
        .then(response => response.json())
        .then(data => {
            // Обновление содержимого корзины на основе данных из ответа
            if (data.success) {
                // Успешно удалено, обновляем отображение корзины
            const cartItemCountElement = document.getElementById('cartItemCount');
            if (cartItemCountElement) {
                cartItemCountElement.textContent = data.cartItemCount;
            }
            location.reload();

                // Дополнительно можно обновить другие части страницы, отображающие содержимое корзины
            } else {
                // Возникла ошибка при удалении товара из корзины, обработаем её
                console.error(data.error);
            }
        })
        .catch(error => {
            console.error('Ошибка при выполнении AJAX запроса:', error);
        });
    });
});








