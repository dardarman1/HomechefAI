using UnityEngine;

public class Hyperlink : MonoBehaviour
{
    public string url;
    public void Open() {
        Application.OpenURL(url);
    }
}
