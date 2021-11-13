import os
import base64
from google.cloud import pubsub_v1


def hello_world(event, context):
    """受け取ったメッセージをそのまま出力する
    Args:
         event (dict):  イベント固有のデータを持つ辞書。
                        `data` フィールドは、Base64エンコードされた文字列のPubsubMessageデータにマッピングされます。
                        `attributes`フィールドは、PubsubMessageの属性が存在する場合、その属性をマップします。

         context (google.cloud.functions.Context): イベントの属性を持つ辞書  
                        `event_id`（PubsubMessageのmessageIdに対応）
                        `timestamp`（PubsubMessageのpublishTimeに対応）
                        `event_type`（`google.pubsub.topic.publish`に対応）
                        `resource`（サービスAPIのエンドポイントであるpubsub.googleapis.com、トリガーとなるトピックの名前、トリガーとなるイベントのタイプを記述した辞書）
    Returns:
        None. The output is written to Cloud Logging.
    """
    print("""This Function was triggered by messageId {} published at {} to {}
    """.format(context.event_id, context.timestamp, context.resource["name"]))

    # メッセージを出力    
    if 'data' in event:
        message = base64.b64decode(event['data']).decode('utf-8')
    else:
        message = 'World'
    print(f'{message}')

    print("finish hello_world")


def deco_message(event, context):
    """受け取ったメッセージをデコレーションしてnumbering_messageに渡す
    """

    print("""This Function was triggered by messageId {} published at {} to {}
    """.format(context.event_id, context.timestamp, context.resource["name"]))

    # messageから受け取った情報    
    if 'data' in event:
        message = base64.b64decode(event['data']).decode('utf-8')
    else:
        message = 'No Message'
    print(f'{message}')
    
    # デコる
    deco_message = f'★{message}★'
    print(deco_message)

    # 次のpubsubを起動するための準備
    PROJECT_ID = os.getenv('PROJECT_ID')
    client = pubsub_v1.PublisherClient()
    topic_id = "sample_numbering_message" 
    topic_path = client.topic_path(PROJECT_ID, topic_id)

    # 起動
    data = deco_message.encode()
    client.publish(topic_path, data=data) 

    print('finish deco_message')


def numbering_message(event, context):
    """メッセージに連番をつけてhello_worldにわたす
    """
    print("""This Function was triggered by messageId {} published at {} to {}
    """.format(context.event_id, context.timestamp, context.resource["name"]))

    # topic_bから受け取った情報    
    if 'data' in event:
        message = base64.b64decode(event['data']).decode('utf-8')
    else:
        message = 'No Message'
    print(f'{message}')

    # 連番を振る数
    number = 3

    # 次にパスするトピックを設定
    PROJECT_ID = os.getenv('PROJECT_ID')
    client = pubsub_v1.PublisherClient()
    topic_id = "sample_hello_world" 
    topic_path = client.topic_path(PROJECT_ID, topic_id)

    # 連番を振ってhello_worldを起動
    for n in range(number):
        text = f"{n}. {message}"
        data = text.encode()
        client.publish(topic_path, data=data) 
    
    print('numbering_message')


if __name__=='__main':
    topic_b()