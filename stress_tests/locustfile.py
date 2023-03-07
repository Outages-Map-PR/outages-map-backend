from locust import HttpUser, TaskSet, task, between


class UserBehavior(HttpUser):
    @task
    def login(self):
        self.client.get("/API/user/login", json={
            "user_email": "test2@gmail.com",
            "user_password": "this_is_a_test"
        })