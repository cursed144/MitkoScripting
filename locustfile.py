from locust import HttpUser, task, between, SequentialTaskSet
import random
import string
import json

def random_string(n=8):
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=n))

class ApiTasks(SequentialTaskSet):
    """
    Example sequential user journey (optional). Tasks below run in sequence;
    Locust will loop through them with the user's wait_time in between.
    """

    @task
    def get_root(self):
        # simple GET to /get (httpbin returns details about the request)
        self.client.get("/get", name="GET /get")

    @task
    def get_with_query(self):
        q = random_string(6)
        self.client.get(f"/get?search={q}", name="GET /get?search")

    @task
    def head(self):
        # HEAD returns headers only
        self.client.head("/get", name="HEAD /get")

    @task
    def post_json(self):
        payload = {"id": random.randint(1, 1000), "name": random_string(6)}
        with self.client.post("/post", json=payload, name="POST /post", catch_response=True) as resp:
            # simple validation example
            if resp.status_code != 200:
                resp.failure(f"Unexpected status {resp.status_code}")
            else:
                # optionally inspect returned json structure
                try:
                    data = resp.json()
                    if "json" not in data:
                        resp.failure("Response missing 'json' field")
                except Exception:
                    resp.failure("Invalid JSON in response")

    @task
    def put(self):
        payload = {"update": random_string(10)}
        self.client.put("/put", json=payload, name="PUT /put")

    @task
    def patch(self):
        payload = {"patch": random_string(6)}
        self.client.patch("/patch", json=payload, name="PATCH /patch")

    @task
    def delete(self):
        self.client.delete("/delete", name="DELETE /delete")


class HttpBinUser(HttpUser):
    host = "https://httpbin.org"
    tasks = [ApiTasks]   # use the SequentialTaskSet above
    wait_time = between(1, 2)

    def on_start(self):
        # set a header for all requests from this virtual user
        self.client.headers.update({"User-Agent": "LocustHttpBinTest/1.0"})
