import unittest
import app

class Form(object):
    def __init__(self, data: dict) -> None:
        self.form = data

    def items(self) -> dict:
        return self.form.items()


class TestPages(unittest.TestCase):
    """
    Test the main pages are available and redirects are working
    as exepcted.
    """

    def setUp(self):
        app.app.config["TESTING"] = True
        self.app = app.app.test_client()

    def test_welcome_page_available(self):
        res = self.app.get("/welcome")
        self.assertEqual(res.status_code, 200)

    def test_root_redirect_to_welcome(self):
        res = self.app.get("/")
        self.assertEqual(res.status_code, 302)
        self.assertIn("/welcome", res.location)

    def test_start_redirect_to_question(self):
        res = self.app.get("/start")
        self.assertEqual(res.status_code, 302)
        self.assertIn("/question/0", res.location)

    def test_question_redirect_to_welcome(self):
        res = self.app.get("/question/0")
        self.assertEqual(res.status_code, 302)
        self.assertIn("/welcome", res.location)

    def test_result_redirect_to_welcome(self):
        res = self.app.get("/result")
        self.assertEqual(res.status_code, 302)
        self.assertIn("/welcome", res.location)


class TestQuestionnaire(unittest.TestCase):
    """
    Test the logic of the application.
    """

    def setUp(self):
        app.app.config["TESTING"] = True
        self.app = app.app.test_client()
        with self.app.session_transaction() as sess:
            sess["score"] = 0

    def test_start_form_on_welcome_page(self):
        res = self.app.get("/welcome")
        self.assertIn(b'<form action="/start">', res.data)

    def test_start_value_on_welcome_page(self):
        res = self.app.get("/welcome")
        self.assertIn(
            b'<input type="hidden" id="startTest" name="startTest" value="startTest">',
            res.data,
        )

    def test_submit_btn_on_welcome_page(self):
        res = self.app.get("/welcome")
        self.assertIn(b'<input type="submit"', res.data)

    def test_result_page_with_score(self):
        res = self.app.get("/result")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'<span class="result"', res.data)

    def test_question_page_available(self):
        res = self.app.get("/question/0")
        self.assertEqual(res.status_code, 200)

    def test_question_page_not_available(self):
        res = self.app.get("/question/999")
        self.assertEqual(res.status_code, 404)

    def test_answer_form_in_question_page(self):
        res = self.app.get("/question/0")
        self.assertIn(b'<form id="answer"', res.data)

    def test_answer_form_contains_submit_btn(self):
        res = self.app.get("/question/0")
        self.assertIn(b'<input type="submit"', res.data)

    def test_update_score(self):
        data = {"questionId": 0, "answers": 0, "isLast": 0}
        res = self.app.post("/update_score", data=Form(data))
        self.assertEqual(res.status_code, 302)
        self.assertIn("/question/1", res.location)

    def test_update_score_redirect_ro_result(self):
        data = {"questionId": 1, "answers": 1, "isLast": 1}
        res = self.app.post("/update_score", data=Form(data))
        self.assertEqual(res.status_code, 302)
        self.assertIn("/result", res.location)


if __name__ == "__main__":
    unittest.main()
