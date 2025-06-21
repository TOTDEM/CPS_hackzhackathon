using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.Collections;
using UnityEngine.Networking;

public class QuestionController : MonoBehaviour
{
    // --- ウェイターが使う道具（UI要素）を、後でUnityエディタから設定する場所 ---
    public TextMeshProUGUI questionText;
    public Button choiceAButton;
    public Button choiceBButton;
    public Button generateButton;
    public TextMeshProUGUI resultText;

    // --- キッチンの住所 ---
    private string serverUrl = "http://127.0.0.1:5000/quiz";

    // --- 受け取った料理（クイズデータ）を一時的に置くお皿 ---
    private QuizData currentQuiz;

    // --- 仕事開始時の準備 ---
    void Start()
    {
        // 最初はボタンなどを隠しておく
        questionText.text = "下のボタンを押して、キッチンからクイズをもらいましょう！";
        resultText.text = "";
        choiceAButton.gameObject.SetActive(false);
        choiceBButton.gameObject.SetActive(false);

        // 「問題生成」ボタンが押されたら、キッチンに注文を出すように設定
        generateButton.onClick.AddListener(OnGenerateButtonClicked);
        // 選択肢A/Bのボタンが押されたら、答え合わせをするように設定
        choiceAButton.onClick.AddListener(() => OnChoiceSelected(0));
        choiceBButton.onClick.AddListener(() => OnChoiceSelected(1));
    }

    // --- 「問題生成」ボタンが押された時の行動 ---
    void OnGenerateButtonClicked()
    {
        // 「キッチンに注文を出す」という行動を開始する
        StartCoroutine(GetQuizFromServer());
    }

    // --- キッチンに注文を出し、料理が届くまで待つ一連の行動 ---
    IEnumerator GetQuizFromServer()
    {
        // 注文中はボタンを非表示にしたり、メッセージを変えたりする
        generateButton.interactable = false;
        questionText.text = "キッチンに注文中です...";
        resultText.text = "";
        choiceAButton.gameObject.SetActive(false);
        choiceBButton.gameObject.SetActive(false);

        // UnityWebRequestという道具を使って、キッチンの住所に注文を出す
        using (UnityWebRequest webRequest = UnityWebRequest.Get(serverUrl))
        {
            // 料理が届くまで待つ
            yield return webRequest.SendWebRequest();

            // 料理が無事に届いたら（通信成功）
            if (webRequest.result == UnityWebRequest.Result.Success)
            {
                // 届いたJSON形式のデータを、注文伝票（QuizData）の形に変換する
                currentQuiz = JsonUtility.FromJson<QuizData>(webRequest.downloadHandler.text);
                // 料理をお客さんに見せる
                DisplayQuiz();
            }
            // 注文に失敗したら
            else
            {
                questionText.text = "厨房との通信に失敗しました。サーバーは起動していますか？";
                Debug.LogError("Server Error: " + webRequest.error);
            }
        }
        // 注文が終わったら、またボタンを押せるようにする
        generateButton.interactable = true;
    }

    // --- 届いた料理（クイズ）をお客さんに見せる行動 ---
    void DisplayQuiz()
    {
        questionText.text = currentQuiz.question;
        choiceAButton.GetComponentInChildren<TextMeshProUGUI>().text = currentQuiz.options[0];
        choiceBButton.GetComponentInChildren<TextMeshProUGUI>().text = currentQuiz.options[1];

        choiceAButton.gameObject.SetActive(true);
        choiceBButton.gameObject.SetActive(true);
        choiceAButton.interactable = true;
        choiceBButton.interactable = true;
    }

    // --- 答え合わせをする行動 ---
    void OnChoiceSelected(int choiceIndex)
    {
        // 正解かどうかを判定
        if (currentQuiz.options[choiceIndex] == currentQuiz.answer)
        {
            resultText.text = "正解！お見事！";
            resultText.color = Color.green;
        }
        else
        {
            resultText.text = $"残念... 正解は「{currentQuiz.answer}」でした";
            resultText.color = Color.red;
        }

        // 一度答えたら、ボタンを押せなくする
        choiceAButton.interactable = false;
        choiceBButton.interactable = false;
    }
}