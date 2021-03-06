# TODO App
[![CircleCI](https://circleci.com/gh/shoito/todo-app.svg?style=svg&circle-token=6348560d58ff8f4a67c661162c67ad2398312c9c)](https://circleci.com/gh/shoito/todo-app)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Todoアプリケーション用API。

Todoの作成、変更、削除、検索の機能を提供する。

![Todoアプリケーションアーキテクチャ](images/todo_app_arc.png "Todoアプリケーションアーキテクチャ")


## 認証
### apiKey

|Name|In|
|---|---|
|x-api-key|header|


## /todos
### Method: POST
Summary: Todo登録API

Description: Todo情報を登録します

Parameters

| Name | Located in | Required | Schema | Description |
| ---- | ---------- | -------- | ------ | ----------- |
| body | body | Yes | [Todo](#todo) | 登録するTodo情報(タイトル、説明など) |

Responses

| Code | Description |
| ---- | ----------- |
| 201 | Todoの作成に成功 |
| 400 | 不正なリクエストによりTodoの作成に失敗 |


### Method: GET
Summary: Todo検索API

Description: クエリ指定された条件に合うTodo情報を返します

Parameters

| Name | Located in | Required | Schema | Description |
| ---- | ---------- | -------- | ------ | ----------- |
| todo_status | query | No | string | 検索対象のステータス |

Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | Todoの検索に成功 | [ [Todo](#todo) ] |
| 400 | 不正なリクエストによりTodoの検索に失敗 |


## /todos/{id}
### Method: GET
Summary: Todo取得API

Description: 指定されたIDのTodo情報を返します

Parameters

| Name | Located in | Required | Schema | Description |
| ---- | ---------- | -------- | ------ | ----------- |
| id | path | Yes | string | 取得対象のTodo ID |
| body | body | Yes | [Todo](#todo) | 取得するTodo情報(タイトル、説明など) |

Responses

| Code | Description |
| ---- | ----------- |
| 200 | Todoの取得に成功 |
| 404 | 取得対象のTodo情報が存在しない |


### Method: PUT
Summary: Todo更新API

Description: 指定されたIDのTodo情報を更新します

Parameters

| Name | Located in | Required | Schema | Description |
| ---- | ---------- | -------- | ------ | ----------- |
| id | path | Yes | string | 更新対象のTodo ID |
| body | body | Yes | [Todo](#todo) | 更新するTodo情報(タイトル、説明など) |

Responses

| Code | Description |
| ---- | ----------- |
| 204 | Todoの更新に成功 |
| 400 | 不正なリクエストによりTodoの更新に失敗 |
| 404 | 削除対象のTodo情報が存在しない |


### Method: DELETE
Summary: Todo削除API

Description: 指定されたIDのTodo情報を削除します

Parameters

| Name | Located in | Required | Schema | Description |
| ---- | ---------- | -------- | ------ | ----------- |
| id | path | Yes | string | 削除対象のTodo ID |

Responses

| Code | Description |
| ---- | ----------- |
| 204 | Todoの削除に成功 |
| 404 | 削除対象のTodo情報が存在しない |


## リクエスト/レスポンスモデル
<a name="todo"></a>Todo


| Name | Type | Required | Description |
| ---- | ---- | -------- | ----------- |
| id | string | No | ID |
| title | string | No | タイトル |
| description | string | No | Todoの詳細説明 |
| due_date | string | No | 期日 |
| todo_status | string | No | ステータス(TODO, DOING, DONE) |


# 開発
## ユニットテスト実行

```bash
docker-compose up -d
TABLE_NAME=ut_todos DEFAULT_REGION=ap-northeast-1 DYNAMODB_ENDPOINT=http://localhost:4569 python -m pytest tests/ -v
```

## サンプル実行
### 変数設定

```bash
BASE_URL=
API_KEY=
```

### 登録

```bash
curl $BASE_URL/todos \
    -d '{"title": "t1", "description": "d1", "due_date": "2018-06-12T15:00:00Z"}' \
    -H "x-api-key:$API_KEY" \
    -XPOST -v
```

```bash
curl $BASE_URL/todos \
    -d '{"title": "t2", "description": "d2", "due_date": "2018-06-15T15:00:00Z"}' \
    -H "x-api-key:$API_KEY" \
    -XPOST -v
```

```bash
curl $BASE_URL/todos \
    -d '{"title": "t3", "description": "d3", "due_date": "2018-06-21T15:00:00Z"}' \
    -H "x-api-key:$API_KEY" \
    -XPOST -v
```

### 全件取得

```bash
curl $BASE_URL/todos \
    -H "x-api-key:$API_KEY" \
    -XGET -v
```

### 1件取得

```bash
curl $BASE_URL/todos/$TODO_ID \
    -H "x-api-key:$API_KEY" \
    -XGET -v
```

### 更新

```bash
curl $BASE_URL/todos/$TODO_ID \
    -d '{"title": "tx", "description": "dx", "due_date": "2018-06-21T15:00:00Z", "todo_status": "DOING"}' \
    -H "x-api-key:$API_KEY" \
    -XPUT -v
```

### 1件取得

```bash
curl $BASE_URL/todos/$TODO_ID \
    -H "x-api-key:$API_KEY" \
    -XGET -v
```

### 絞り込み取得

```bash
curl "$BASE_URL/todos?todo_status=DOING" \
    -H "x-api-key:$API_KEY" \
    -XGET -v
```

### 削除

```bash
curl $BASE_URL/todos/$TODO_ID \
    -H "x-api-key:$API_KEY" \
    -XDELETE -v
```