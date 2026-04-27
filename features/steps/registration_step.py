from behave import *
from Utilities import configReader
from features.pageobjects.RegistrationPage import RegistrationPage
import time


@given(u'I navigate to way2automation.com')
def step_impl(context):
    context.reg = RegistrationPage(
        context.page,
        context.scenario_logger
    )
    context.reg.open(
        configReader.readConfig("urls", "testSiteUrl")
    )


@given(u'I navigate to Swag Labs')
def step_impl(context):
    context.reg = RegistrationPage(
        context.page,
        context.scenario_logger
    )
    context.reg.open(
        configReader.readConfig("urls", "loginTestUrl")
    )


@when("I verify the user using API")
def step_impl(context):
    response = context.api_request.get(
        configReader.readConfig("urls", "apiBaseTestUrl") + "/api/users"
    )

    assert response.status == 200, (
        f"Unexpected status code: {response.status}"
    )


@when(u'I LogIn into the App with personal credentials')
def step_impl(context):
    context.reg.set_swaglabs_username(configReader.readConfig("credentials", "SwagLabsUserName"))
    context.reg.set_swaglabs_password(configReader.readConfig("credentials", "SwagLabsPassw"))
    time.sleep(2)
    context.reg.submit_swaglabs_login()


@when(u'I LogIn into the App with different credentials')
def step_impl(context):
    row = context.table[0]
    username = row["UserName"]
    password = row["Password"]

    context.reg.set_swaglabs_username(username)
    context.reg.set_swaglabs_password(password)
    time.sleep(2)
    context.reg.submit_swaglabs_login()


@when(u'I enter the name as "{name}"')
def step_impl(context, name):
    context.reg.set_name(name)


@then(u'I see Products Page')
def step_impl(context):
    expected_title = context.reg.get_products_page_title()
    assert expected_title == "Products", f"Page title: {expected_title}"


@then(u'I enter the phone number as "{phonenumber}"')
def step_impl(context, phonenumber):
    context.reg.set_phone_number(phonenumber)


@then(u'I enter the email as "{email}"')
def step_impl(context, email):
    context.reg.set_email(email)


@then(u'I enter the country as "{country}"')
def step_impl(context, country):
    context.reg.set_country(country)


@then(u'I enter the city as "{city}"')
def step_impl(context, city):
    context.reg.set_city(city)


@then(u'I enter the username as "{username}"')
def step_impl(context, username):
    context.reg.set_username(username)


@then(u'I enter the password as "{password}"')
def step_impl(context, password):
    context.reg.set_password(password)


@then(u'I click on the submit button')
def step_impl(context):
    context.reg.submit_form()


@then(u'I see expected Email is "{email}"')
def step_impl(context, email):
    page = context.page

    entered_email = context.reg.get_email()
    assert entered_email == email, (
        f"Expected Email is '{email}' but got '{entered_email}'"
    )

    #assert page.input_value("input[name='name']") == "JQ"
    #assert page.input_value("input[name='phone']") == "1234567"
    #assert page.input_value("input[name='email']") == "jq@mail.com"