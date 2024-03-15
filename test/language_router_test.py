from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_summarize():
    response = client.post("/language/",
                           json={
                               "memberId": 1,
                               "memberName": "홍길동",
                               "memberEmail": "test@test.com",
                               "memberStatement": "내일 저녁 6시에 친구랑 잠실종합운동장역 앞에서 만나기로 했어. 친구랑 만난 후에는 조용필 콘서트를 볼거야",
                               "requestedDate": "2021-11-22T14:"
                           })
    assert response.status_code == 201
