import pytest


@pytest.mark.query_validation
def test_get_by_id_validation():
    from src.api.api import get
    from src.utils.err_utils import IDValidationError
    err_dict = IDValidationError().__dict__
    invalid_parameter_id = [
        ' ', '', 'ab cd', '*', '@', '$', '%', '^', '&', '?', '(', ')', '!'
    ]
    for user_id in invalid_parameter_id:
        assert get(user_id=user_id) == err_dict, 'test failed'
