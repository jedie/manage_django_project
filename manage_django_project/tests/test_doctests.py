from bx_py_utils.test_utils.unittest_utils import BaseDocTests

import manage_django_project
import manage_django_project_example


class DocTests(BaseDocTests):
    def test_doctests(self):
        self.run_doctests(
            modules=(manage_django_project, manage_django_project_example),
        )
