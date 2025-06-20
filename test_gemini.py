import google.generativeai as genai
import os
 
# 環境変数からAPIキーを読み込む
api_key = os.environ.get("gemini")
 
if not api_key:
    print("エラー: GOOGLE_API_KEY が環境変数に設定されていません。")
    print("APIキーを取得し、'export GOOGLE_API_KEY=\"YOUR_API_KEY\"' (Mac/Linux) または 'set GOOGLE_API_KEY=\"YOUR_API_KEY\"' (Windows) で設定してください。")
    exit()
 
try:
    genai.configure(api_key=api_key)
except Exception as e:
    print(f"エラー: APIキーの設定中に問題が発生しました。エラー内容: {e}")
    print("APIキーが有効であるか、Google AI Studio で確認してください。")
    exit()
 
# !!! ここを修正します !!!
# あなたの環境で利用可能な最新のプロモデルを選択します。
# もし 'models/gemini-1.5-pro-latest' でうまくいかない場合、
# 'models/gemini-1.5-flash-latest' や 'models/gemini-2.5-pro' など、
# 上記リストにある別のモデル名を試してみてください。
model_name = 'models/gemini-1.5-flash-latest'
 
try:
    model = genai.GenerativeModel(model_name)
    print(f"モデル '{model_name}' のロードに成功しました。")
except Exception as e:
    print(f"\nエラー: モデル '{model_name}' のロードに失敗しました。詳細: {e}")
    print("上記の利用可能なモデルリストを確認し、正しいモデル名を使用してください。")
    exit()
 
# チャットセッションを開始
chat = model.start_chat(history=[])
 
print("\n-----------------------------------------------------")
print("チャットボットへようこそ！ '終了' と入力するとチャットを終了します。")
print("-----------------------------------------------------")
 
while True:
    user_message = input("あなた: ")
 
    if user_message.lower() == '終了':
        print("チャットを終了します。またのご利用をお待ちしております！")
        break
   
    try:
        # ユーザーのメッセージをモデルに送信し、応答を取得
        response = chat.send_message(user_message)
        print(f"ボット: {response.text}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        print("インターネット接続を確認するか、別のモデル名で試してみてください。")
        print("もう一度お試しいただくか、'終了' と入力してください。")