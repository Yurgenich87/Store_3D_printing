let currentProductId = null;
let currentOrderId = null;
var datepicker = new Datepicker('#datepicker');


function updateProfile(userId, formData) {
    fetch(`/edit_profile/${userId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: formData
    })
    .then(function (response) {
        return response.json();  // Преобразуем ответ в JSON
    })
    .then(function (data) {
        if (data.success) {
            // showNotification('Profile updated successfully');
            console.info('Profile updated successfully');
            // Перезагрузить текущую страницу
        } else {
            console.error('Failed to update profile');
        }
    })
    .catch(function (error) {
        console.error('Error:', error);
    });
}

function createProduct(productData) {
   const csrftoken = getCookie('csrftoken');

    const formData = new FormData();

    formData.append('name', productData.name);
    formData.append('price', productData.price);
    formData.append('quantity', productData.quantity);
    formData.append('description', productData.description);

    if (productData.category_id) {
        formData.append('category_id', productData.category_id);
    } else {
        formData.append('category_id', 1);
    }


    if (productData.image) {
        formData.append('image', productData.image);
    }

    const requestOptions = {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: formData
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
                $('#showModal').modal('hide');

                showNotification('Продукт успешно создан.');
            })
        .catch(error => {
                console.error('Ошибка при создании продукта:', error);
            });
}

function updateData(productId, updatedData) {
    const csrftoken = getCookie('csrftoken');

    const formData = new FormData();

    formData.append('name', updatedData.name);
    formData.append('price', updatedData.price);
    formData.append('quantity', updatedData.quantity);
    formData.append('description', updatedData.description);
    formData.append('category_id', updatedData.category_id);


    if (updatedData.image) {
        formData.append('image', updatedData.image);
    }

    const requestOptions = {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: formData
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

function filterProducts(days) {
    fetch(`/filter_products/${days}/`)
        .then(response => {
            if (response.ok) {
                return response.text();

            }
            throw new Error('Ошибка при получении данных');
        })
        .then(html => {
            document.querySelector('body').innerHTML = html;
            console.info('days:', days);
        })
        .catch(error => console.error('Ошибка при фильтрации товаров:', error));
}

function updateOrder(orderId, updatedOrderData) {
    const csrftoken = getCookie('csrftoken');
    const formOrder = new FormData();

    formOrder.append('user', updatedOrderData.user);
    formOrder.append('product', updatedOrderData.product);

    fetch(`/update_order/${orderId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: formOrder
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to update order');
        }
        showNotification('Заказ изменен успешно');
        $('#showOrderModal').modal('hide');

        console.log('Order updated successfully');
    })
    .catch(error => {
        console.error('Error updating order:', error);
    });
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
            document.querySelector('body').innerHTML = html;
        })
        .catch(error => console.error('Ошибка при фильтрации заказов:', error));
}

function deleteOrder(orderId) {
    fetch(`/delete_order/${orderId}/`, {
        method: 'POST',
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to delete order');
        }
        showNotification('Заказ удален успешно');
        console.log('Order deleted successfully');
    })
    .catch(error => {
        console.error('Error deleting order:', error);
    });
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
            document.querySelector('body').innerHTML = html;
        })
        .catch(error => console.error('Ошибка при фильтрации товаров в корзине:', error));
}

function deleteProductFromCart(productId) {
    const csrftoken = getCookie('csrftoken');

    fetch(`/remove_from_cart/${productId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
            const cartItemCountElement = document.getElementById('cartItemCount');
            if (cartItemCountElement) {
                cartItemCountElement.textContent = data.cartItemCount;
            }
            location.reload();

            } else {
                console.error(data.error);
            }
        })
        .catch(error => {
            console.error('Ошибка при выполнении AJAX запроса:', error);
        });
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

function resetFilter() {
    window.location.reload();
}

function showNotification(message) {
    console.log('showNotification:', message);

    let notificationElement = document.createElement('div');
    notificationElement.textContent = message;

    let updateSuccessMessage = document.getElementById('update-success-message');

    updateSuccessMessage.innerHTML = ''; // Очищаем содержимое, если уже что-то было
    updateSuccessMessage.appendChild(notificationElement);

    console.log('showNotification start: ', notificationElement);

    updateSuccessMessage.style.display = 'block';

    setTimeout(function() {
        notificationElement.remove();
        updateSuccessMessage.style.display = 'none';
    }, 4000);

    return new Promise(resolve => {
        setTimeout(() => {
            location.reload();
            resolve(null);
        }, 3000);
    });
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


//___________________________________________________Products___________________________________________________________
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("showModal") && (document.getElementById("showModal").addEventListener("show.bs.modal", function(e) {
        if (e.relatedTarget.classList.contains("edit-item-btn")) {
            document.getElementById("exampleModalLabel").innerHTML = "Редактирование товара";
            document.getElementById("showModal").querySelector(".modal-footer").style.display = "block";
            document.getElementById("add-btn").style.display = "none";
            document.getElementById("edit-btn").style.display = "block";

            currentProductId = e.relatedTarget.dataset.productId;


            let productId = currentProductId;

            fetch('/api/categories/')
                .then(response => response.json())
                .then(categories => {
                    let categorySelect = document.getElementById("edit-category");
                    categorySelect.innerHTML = '';
                    categories.forEach(category => {
                        let option = document.createElement('option');
                        option.value = category.id;
                        option.text = category.name;
                        categorySelect.appendChild(option);
                    });
                    let productCategory = data.find(item => item.id === parseInt(product.category_id));
                    if (productCategory) {
                        categorySelect.value = productCategory.id;
                    }
                })
                .catch(error => console.error('Error fetching categories:', error));
                        fetch('/api/products/')
                .then(response => response.json())
                .then(data => {
                    let product = data.find(item => item.id === parseInt(productId));
                    document.getElementById("name").value = product.name;
                    document.getElementById("price").value = product.price;
                    document.getElementById("quantity").value = product.quantity;
                    document.getElementById("description").value = product.description;
                    document.getElementById("edit-category").value = product.category_id;

                })
                .catch(error => console.error('Error fetching product details:', error));

        } else if (e.relatedTarget.classList.contains("create-btn")) {
            document.getElementById("exampleModalLabel").innerHTML = "Добавление товара";
            document.getElementById("showModal").querySelector(".modal-footer").style.display = "block";
            document.getElementById("edit-btn").style.display = "none";
            document.getElementById("add-btn").style.display = "block";

            fetch('/api/categories/')
                .then(response => response.json())
                .then(categories => {
                    let categorySelect = document.getElementById("edit-category");
                    categorySelect.innerHTML = '';
                    categories.forEach(category => {
                        let option = document.createElement('option');
                        option.value = category.id;
                        option.text = category.name;
                        categorySelect.appendChild(option);
                    });
                    let productCategory = data.find(item => item.id === parseInt(product.category_id));
                    if (productCategory) {
                        categorySelect.value = productCategory.id;
                    }
                })
        }
    }));


    // Обработчик события клика на кнопку "Добавить товар"
    document.getElementById("add-btn").addEventListener("click", function(event) {
        event.preventDefault();

        let name = document.getElementById("name").value;
        let price = document.getElementById("price").value;
        let quantity = document.getElementById("quantity").value;
        let description = document.getElementById("description").value;
        let category_id = document.getElementById("edit-category").value;

        let imageInput = document.getElementById("image");
        let image = null;
        if (imageInput.files.length > 0) {
            image = imageInput.files[0];
        }

        let newProductData = {
            name: name,
            price: price,
            quantity: quantity,
            description: description,
            category_id: category_id,
            image: image
        };

        createProduct(newProductData);
    });

    // Обработчик события клика на кнопку "Обновить"
    document.getElementById("edit-btn").addEventListener("click", function(event) {
        event.preventDefault();

        let productId = currentProductId;

        let name = document.getElementById("name").value;
        let price = document.getElementById("price").value;
        let quantity = document.getElementById("quantity").value;
        let description = document.getElementById("description").value;
        let category_id = document.getElementById("edit-category").value;

        let imageInput = document.getElementById("image");
        let image = null;
        if (imageInput.files.length > 0) {
            image = imageInput.files[0];
        }

        let updatedData = {
            name: name,
            price: price,
            quantity: quantity,
            description: description,
            category_id: category_id,

        };

        if (image) {
            updatedData['image'] = image;
        }

        updateData(productId, updatedData);
    });


    // Обработчик события, который вызывается при открытии модального окна
    $('#deleteRecordModal').on('show.bs.modal', function (event) {
        const deleteButton = document.getElementById('delete-record');
        const productId = event.relatedTarget.getAttribute('data-product-id');
        deleteButton.setAttribute('data-product-id', productId);

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

        currentProductId = null;
    });

});

//___________________________________________________Cart___________________________________________________________
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
                const cartItemCountElement = document.getElementById('cartItemCount');
                if (cartItemCountElement) {
                    cartItemCountElement.textContent = data.cartItemCount;
                }
                location.reload();
                showNotification('Товар успешно добавлен в корзину');
            })
            .catch(error => {
                console.error('Ошибка при добавлении товара в корзину:', error);
                showNotification('Ошибка при добавлении товара в корзину. Пожалуйста, попробуйте еще раз.');
            });
        });
    });

document.querySelectorAll('.remove-from-cart-btn').forEach(button => {
    button.addEventListener('click', function() {
        const productId = this.getAttribute('data-product-id');
        deleteProductFromCart(productId);

    });
});

const increaseButtons = document.querySelectorAll('.SnowShoppingcartProductList_ProductNumAction__button__eac55:first-child');
const decreaseButtons = document.querySelectorAll('.SnowShoppingcartProductList_ProductNumAction__button__eac55:last-child');

increaseButtons.forEach(button => {
    button.addEventListener('click', function() {
        const quantityElement = this.parentElement.querySelector('.SnowShoppingcartProductList_ProductNumAction__quantity__eac55');
        const newQuantity = parseInt(quantityElement.textContent) + 1;
        quantityElement.textContent = newQuantity;
    });
});

decreaseButtons.forEach(button => {
    button.addEventListener('click', function() {
        const quantityElement = this.parentElement.querySelector('.SnowShoppingcartProductList_ProductNumAction__quantity__eac55');
        const newQuantity = Math.max(parseInt(quantityElement.textContent) - 1, 1);
        quantityElement.textContent = newQuantity;
    });
});

//___________________________________________________Orders___________________________________________________________
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("showOrderModal") && (document.getElementById("showOrderModal").addEventListener("show.bs.modal", function(e) {
        if (e.relatedTarget.classList.contains("edit-order")) {
            document.getElementById("orderModalLabel").innerHTML = "Редактирование заказа";
            document.getElementById("showOrderModal").querySelector(".modal-footer").style.display = "block";
            document.getElementById("edit-order-btn").style.display = "block";

            currentOrderId = e.relatedTarget.dataset.orderId;

            let orderId = currentOrderId;

            fetch('/api/users/')
                .then(response => response.json())
                .then(users => {
                    const userSelect = document.getElementById('user_id');
                    users.forEach(user => {
                        const option = document.createElement('option');
                        option.value = user.id;
                        option.textContent = user.username;
                        userSelect.appendChild(option);
                    });
                })
                .catch(error => console.error('Error loading users:', error));
            fetch('/api/products/')
                .then(response => response.json())
                .then(products => {
                    const productSelect = document.getElementById('product_id');
                    products.forEach(product => {
                        const option = document.createElement('option');
                        option.value = product.id;
                        option.textContent = product.name;
                        productSelect.appendChild(option);
                    });
                })
                .catch(error => console.error('Error loading products:', error));
            fetch(`/api/orders/`)
                .then(response => response.json())
                .then(data => {
                    let order = data.find(item => item.id === parseInt(orderId));
                    document.getElementById("user_id").value = order.user
                    document.getElementById("product_id").value = order.product;
                })
                .catch(error => console.error('Error fetching order details:', error));
        }
    }));

    // Добавляем обработчик события клика на кнопку "Обновить заказ"
    document.getElementById("edit-order-btn").addEventListener("click", function(event) {
        event.preventDefault();

        let orderId = currentOrderId;
        console.info('edit-order-btn currentOrderId = ', currentOrderId)
        console.info('edit-order-btn orderId = ', orderId)

        let user = document.getElementById("user_id").value;
        let product = document.getElementById("product_id").value;
        console.info('edit-order-btn user_id = ', user)
        console.info('edit-order-btn product_id = ', product)

        let updatedOrderData = {
            user: user,
            product: product,
        };

        console.info('updatedOrderData = ', updatedOrderData)

        updateOrder(orderId, updatedOrderData);
    });

    $('#deleteOrderModal').on('show.bs.modal', function (event) {
        const deleteOrderButton = document.getElementById('delete-order');
        const orderId = event.relatedTarget.getAttribute('data-orderId');
        deleteOrderButton.setAttribute('data-orderId', orderId);

        deleteOrderButton.addEventListener('click', function() {
            const orderId = this.getAttribute('data-orderId');
            console.log("Идентификатор заказа для удаления:", orderId);
            deleteOrder(orderId);
        });
    });

    // Функция для очистки полей модального окна при его скрытии
    document.getElementById("showOrderModal").addEventListener("hidden.bs.modal", function() {
        document.getElementById("user_id").value = "";
        document.getElementById("product_id").value = "";

        currentOrderId = null;
    });
});


//___________________________________________________Profile___________________________________________________________

document.addEventListener('DOMContentLoaded', function () {
    var form = document.querySelector('#editProfileForm');

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        var formData = new FormData(form);
        updateProfile(formData); // Вызываем функцию отправки запроса
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contact-form');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(this);

        fetch('/contact_form_submit/', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(data => {
            document.querySelector('.sent-message').innerText = data;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('paymentForm');
    const loadingMessage = form.querySelector('.loading');
    const successMessage = form.querySelector('.sent-message');
    const errorMessage = form.querySelector('.error-message');
    const paymentOptions = document.querySelectorAll('.payment-option');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        let paymentOptionSelected = false;
        paymentOptions.forEach(function(option) {
            if (option.checked) {
                paymentOptionSelected = true;
            }
        });

        if (!paymentOptionSelected) {
            errorMessage.style.display = 'block';
            return;
        }

        loadingMessage.style.display = 'block';
        errorMessage.style.display = 'none';

        setTimeout(function() {
            const success = Math.random() < 0.8;

            loadingMessage.style.display = 'none';

            if (success) {
                successMessage.style.display = 'block';
                setTimeout(function() {
                    successMessage.style.display = 'none';
                    form.reset();
                    window.location.href = '/store/'; // Перенаправление на страницу магазина
                }, 5000);
            } else {
                errorMessage.style.display = 'block';
            }
        }, 2000);

        const formData = new FormData(this);

        fetch('/process_payment/', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
