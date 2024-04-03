from locust import HttpUser, task, between


class MyUser(HttpUser):
    wait_time = between(5, 9)

    @task
    def view_item(self):
        self.client.get("/store")

    @task
    def add_to_cart(self):
        self.client.post("/add_to_cart", json={"product_id": 1})

    @task
    def view_profile(self):
        self.client.get("/profile")

    @task
    def edit_profile(self):
        self.client.post("/edit_profile", json={"username": "new_username", "email": "new_email@example.com"})

    @task
    def view_orders(self):
        self.client.get("/orders")

    @task
    def logout(self):
        self.client.get("/logout")
