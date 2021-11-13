# cloud functionを別のcloud functionsからcloud pub/subで起動するサンプル

## 各関数の説明
- hello_world
    - 受け取ったメッセージをそのまま出力する
- deco_message
    - 受け取ったメッセージをデコレーションしてnumbering_messageに渡す
- numbering_message
    - メッセージに連番をつけてhello_worldにわたす

## 事前準備

### pub/subトピックを作成

```
gcloud pubsub topics create sample_hello_world
gcloud pubsub topics create sample_deco_message
gcloud pubsub topics create sample_numbering_message

```

### functionsをdeploy
```
gcloud functions deploy sample_hello_world \
    --entry-point hello_world \
    --runtime python39 \
    --trigger-topic sample_hello_world \
    --env-vars-file=env.yaml \
    --region asia-northeast1 \
    --timeout 540

gcloud functions deploy sample_deco_message \
    --entry-point deco_message \
    --runtime python39 \
    --trigger-topic sample_deco_message \
    --env-vars-file=env.yaml \
    --region asia-northeast1 \
    --timeout 540

gcloud functions deploy sample_numbering_message \
    --entry-point numbering_message \
    --runtime python39 \
    --trigger-topic sample_numbering_message \
    --env-vars-file=env.yaml \
    --region asia-northeast1 \
    --timeout 540
```

## 実行
```
gcloud pubsub topics publish sample_hello_world --message onigiri
gcloud pubsub topics publish sample_deco_message --message onigiri
```

## 参考
- https://cloud.google.com/functions/docs/tutorials/pubsub
- https://qiita.com/kenkanayama/items/681440c05f79c2e61051