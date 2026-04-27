from playwright.sync_api import sync_playwright
from Utilities import configReader


def test_get_API():
    print("\n*****Starting test_get_API*****\n")

    with sync_playwright() as p:
        request_context = p.request.new_context()
        response = request_context.get(configReader.readConfig("urls", "apiBaseTestUrl") + "/api/users")

        assert response.status == 200, f"Unexpected status code : {response.status}"

        print(f"Status Code {response.status}")
        print(f"Response body: {response.text()}")

        json_response = response.json()

        # Verificar que es lista
        assert isinstance(json_response, list)

        # Imprimir Id y Firstname de cada usuario
        for id in json_response:
            print("Id is ", id.get("id"))
            print("First Name is ", id.get("firstName"))

    print("\n*****Ending test_get_API*****\n")


def test_post_API_create_user():
    print("\n*****Starting test_post_API_create_user*****\n")
    base_url = configReader.readConfig("urls", "apiBaseTestUrl")

    with sync_playwright() as p:
        request_context = p.request.new_context()

        payload = {
            "email": "juangooooooo@test.com",
            "firstName": "Nini",
            "lastName": "Quiceno"
        }

        response = request_context.post(
            base_url + "/api/users",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Accept": "*/*",
                "Cache-Control": "no-cache"
            }
        )

        # ✅ Validar solo lo que la API promete
        assert response.status in [200, 201, 204]

        # ✅ Confirmar que no hay body
        assert response.text() == ""

        print("\nUser created successfully (no response body)")

        print("Status:", response.status)
        print("Response text:", repr(response.text()))
        print("Headers:", response.headers)

        response = request_context.get("http://localhost:8080/api/users")

        assert response.status == 200, f"Unexpected status code : {response.status}"

        json_response = response.json()

        for user in json_response:
            print("Id is ", user.get("id"))
            print("First Name is ", user.get("firstName"))
            print("Last Name is ", user.get("lastName"))

    print("\n*****Ending test_post_API_create_user*****\n")

