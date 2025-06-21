using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.Collections;
using UnityEngine.Networking;

public class QuestionController : MonoBehaviour
{
    // --- �E�F�C�^�[���g������iUI�v�f�j���A���Unity�G�f�B�^����ݒ肷��ꏊ ---
    public TextMeshProUGUI questionText;
    public Button choiceAButton;
    public Button choiceBButton;
    public Button generateButton;
    public TextMeshProUGUI resultText;

    // --- �L�b�`���̏Z�� ---
    private string serverUrl = "http://127.0.0.1:5000/quiz";

    // --- �󂯎���������i�N�C�Y�f�[�^�j���ꎞ�I�ɒu�����M ---
    private QuizData currentQuiz;

    // --- �d���J�n���̏��� ---
    void Start()
    {
        // �ŏ��̓{�^���Ȃǂ��B���Ă���
        questionText.text = "���̃{�^���������āA�L�b�`������N�C�Y�����炢�܂��傤�I";
        resultText.text = "";
        choiceAButton.gameObject.SetActive(false);
        choiceBButton.gameObject.SetActive(false);

        // �u��萶���v�{�^���������ꂽ��A�L�b�`���ɒ������o���悤�ɐݒ�
        generateButton.onClick.AddListener(OnGenerateButtonClicked);
        // �I����A/B�̃{�^���������ꂽ��A�������킹������悤�ɐݒ�
        choiceAButton.onClick.AddListener(() => OnChoiceSelected(0));
        choiceBButton.onClick.AddListener(() => OnChoiceSelected(1));
    }

    // --- �u��萶���v�{�^���������ꂽ���̍s�� ---
    void OnGenerateButtonClicked()
    {
        // �u�L�b�`���ɒ������o���v�Ƃ����s�����J�n����
        StartCoroutine(GetQuizFromServer());
    }

    // --- �L�b�`���ɒ������o���A�������͂��܂ő҂�A�̍s�� ---
    IEnumerator GetQuizFromServer()
    {
        // �������̓{�^�����\���ɂ�����A���b�Z�[�W��ς����肷��
        generateButton.interactable = false;
        questionText.text = "�L�b�`���ɒ������ł�...";
        resultText.text = "";
        choiceAButton.gameObject.SetActive(false);
        choiceBButton.gameObject.SetActive(false);

        // UnityWebRequest�Ƃ���������g���āA�L�b�`���̏Z���ɒ������o��
        using (UnityWebRequest webRequest = UnityWebRequest.Get(serverUrl))
        {
            // �������͂��܂ő҂�
            yield return webRequest.SendWebRequest();

            // �����������ɓ͂�����i�ʐM�����j
            if (webRequest.result == UnityWebRequest.Result.Success)
            {
                // �͂���JSON�`���̃f�[�^���A�����`�[�iQuizData�j�̌`�ɕϊ�����
                currentQuiz = JsonUtility.FromJson<QuizData>(webRequest.downloadHandler.text);
                // ���������q����Ɍ�����
                DisplayQuiz();
            }
            // �����Ɏ��s������
            else
            {
                questionText.text = "�~�[�Ƃ̒ʐM�Ɏ��s���܂����B�T�[�o�[�͋N�����Ă��܂����H";
                Debug.LogError("Server Error: " + webRequest.error);
            }
        }
        // �������I�������A�܂��{�^����������悤�ɂ���
        generateButton.interactable = true;
    }

    // --- �͂��������i�N�C�Y�j�����q����Ɍ�����s�� ---
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

    // --- �������킹������s�� ---
    void OnChoiceSelected(int choiceIndex)
    {
        // �������ǂ����𔻒�
        if (currentQuiz.options[choiceIndex] == currentQuiz.answer)
        {
            resultText.text = "�����I�������I";
            resultText.color = Color.green;
        }
        else
        {
            resultText.text = $"�c�O... �����́u{currentQuiz.answer}�v�ł���";
            resultText.color = Color.red;
        }

        // ��x��������A�{�^���������Ȃ�����
        choiceAButton.interactable = false;
        choiceBButton.interactable = false;
    }
}