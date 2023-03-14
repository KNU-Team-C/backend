def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the params and password(hashed) fields are defined correctly
    """
    assert new_user.first_name == "Maxer"
    assert new_user.last_name == "Yudkin"
    assert new_user.email == "hort@gmail.com"
    assert new_user.phone_number == "111-111-111"
    assert new_user.password != "111"
