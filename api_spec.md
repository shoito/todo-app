Todo App API
============
Todoアプリケーション用API。
Todoの作成、変更、削除、検索の機能を提供する。


Version: 0.0.1

License: [MIT License](https://opensource.org/licenses/MIT)

## セキュリティ
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
| 401 | 認証が必要 |


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
| 401 | 認証が必要 |


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
| 401 | 認証が必要 |
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
| 401 | 認証が必要 |
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
| 401 | 認証が必要 |
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