from locust import HttpUser, TaskSet, task, between


class UserBehavior(HttpUser):
    @task
    def all_users(self):
        self.client.get("/API/user")

    @task
    def login(self):
        self.client.get("/API/user/login", json={
            "user_email": "test2@gmail.com",
            "user_password": "this_is_a_test"
        })

    @task
    def outage_map(self):
        self.client.get("/API/outagesmap")
