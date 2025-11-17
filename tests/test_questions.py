def test_get_questions_empty(client):
    """Тест получения пустого списка вопросов"""
    response = client.get("/questions/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_question_success(client):
    """Тест успешного создания вопроса"""
    question_data = {
        "text": "Как продать гараж?",
    }
    response = client.post("/questions/", json=question_data)
    assert response.status_code == 201
    data = response.json()
    assert data["text"] == question_data["text"]
    assert "id" in data


def test_create_question_validation_error(client):
    """Тест валидации при создании вопроса"""
    invalid_data = {
        "text": "",
    }
    response = client.post("/questions/", json=invalid_data)
    assert response.status_code == 422


def test_get_question_detail(client):
    """Тест получения деталей вопроса"""
    question_data = {
        "text": "Вопрос таков",
    }
    create_response = client.post("/questions/", json=question_data)
    question_id = create_response.json()["id"]

    detail_response = client.get(f"/questions/{question_id}")
    assert detail_response.status_code == 200
    question_detail = detail_response.json()
    assert question_detail["id"] == question_id
    assert "answers" in question_detail


def test_get_nonexistent_question(client):
    """Тест получения несуществующего вопроса"""
    response = client.get("/questions/999")
    assert response.status_code == 404


def test_delete_nonexistent_question(client):
    """Тест удаления несуществующего вопроса"""
    response = client.delete("/questions/999")
    assert response.status_code == 204


def test_create_many_answers(client):
    """Тест создания нескольких ответов одного пользователя."""
    question_data = {
        "text": "Как создать апи?",
    }
    create_response = client.post("/questions/", json=question_data)
    question_id = create_response.json()["id"]

    answers_text = ["Ответ1", "Ответ2"]
    user_uuid = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    for answer in answers_text:
        answer_data = {
            "user_id": user_uuid,
            "text": answer
        }
        client.post(f"/questions/{question_id}/answers", json=answer_data)
    get_question_detail = client.get(f"/questions/{question_id}")
    assert len(get_question_detail.json()["answers"]) == 2


def test_cascade_delete(client):
    """Тест каскадного удаления ответов"""
    question_data = {
        "text": "Как создать апи?",
    }
    create_response = client.post("/questions/", json=question_data)
    question_id = create_response.json()["id"]

    answers_text = ["Ответ1", "Ответ2"]
    user_uuid = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    answers_ids = []
    for answer in answers_text:
        answer_data = {
            "user_id": user_uuid,
            "text": answer
        }
        res = client.post(f"/questions/{question_id}/answers", json=answer_data)
        answers_ids.append(res.json()["id"])
    delete_response = client.delete(f"/questions/{question_id}")
    assert delete_response.status_code == 204
    get_response = client.get(f"/questions/{question_id}")
    assert get_response.status_code == 404
    first_answer = client.get(f"/answers/{answers_ids[0]}")
    assert first_answer.status_code == 404
    second_answer = client.get(f"/answers/{answers_ids[1]}")
    assert second_answer.status_code == 404
