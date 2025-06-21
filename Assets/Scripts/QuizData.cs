// このスクリプトは、データをやり取りするための「設計図」なので、
// Unityのオブジェクトにアタッチする必要はありません。

[System.Serializable]
public class QuizData
{
    public string question;
    public string[] options;
    public string answer;
}