function createProduct(productData) {
    const csrftoken = getCookie('csrftoken');

    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(productData)
    };

    fetch('/create_product/', requestOptions)
        .then(response => {
            if (!response.ok) {
                throw new Error('Сетевой ответ не был успешным');
            }
            return response.json();
        })
        .then(data => {
            console.log('Продукт успешно создан:', data);
        })
        .catch(error => {
            console.error('Ошибка при создании продукта:', error);
        });
}


function updateData(productId, updatedData) {
    // Получаем CSRF-токен из cookie
    const csrftoken = getCookie('csrftoken');

    // Формируем тело запроса, включая данные для обновления
    const requestBody = JSON.stringify(updatedData);

    // Опции для запроса
    const requestOptions = {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: requestBody
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
            closeDeleteModal();
            window.location.reload();

        })
        .catch(error => {
            console.error('Ошибка при удалении продукта:', error);
        });
}

function closeDeleteModal() {
    $('#deleteRecordModal').modal('hide');
}
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
            console.error('currentProductId:', currentProductId);


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

        let newProductData = {
            name: name,
            price: price,
            quantity: quantity,
            description: description
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

        let updatedData = {
            name: name,
            price: price,
            quantity: quantity,
            description: description
        };
        console.error('currentProductId:', currentProductId);
        console.error('productId:', productId);
        // Вызываем функцию для отправки обновленных данных на сервер
        updateData(productId, updatedData);
    });


    // Обработчик клика на кнопку удаления
    document.getElementById("remove-item-btn").addEventListener("click", function(event) {

            // Получаем идентификатор продукта из атрибута data-product-id
            const productId = this.getAttribute('data-product-id');

        console.log("Идентификатор товара для удаления:", productId);
        // Передаем идентификатор продукта в модальное окно
        document.getElementById('delete-record').setAttribute('data-product-id', productId);

            // Обработчик клика на кнопку подтверждения удаления
            document.getElementById('delete-record').addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');

                deleteProduct(productId);
            });

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

    // Функция для очистки полей модального окна при его скрытии
    document.getElementById("showModal").addEventListener("hidden.bs.modal", function() {
        document.getElementById("name").value = "";
        document.getElementById("price").value = "";
        document.getElementById("quantity").value = "";
        document.getElementById("description").value = "";

        // Сбрасываем текущий productId
        currentProductId = null;
    });





