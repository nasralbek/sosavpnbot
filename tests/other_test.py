import pytest
from configs.main_config import get_os_attr,os_attr_not_defined

class TestGetOs():
    def test1(self):
        get_os_attr("PATH")

    def test2(self):
        with pytest.raises(os_attr_not_defined):
            get_os_attr("lllllllllllllllll")