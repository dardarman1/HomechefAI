using System;
using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

public class Capture : MonoBehaviour
{
    [Serializable]
    public class SessionResponse
    {
        public string session_id;
    }

    private string sessionId;

    IEnumerator Start() {
        using (UnityWebRequest www = UnityWebRequest.Get("https://my-service-894665829957.us-central1.run.app/start_session"))
        {
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError(www.error);
            }
            else
            {
                var jsonResponse = JsonUtility.FromJson<SessionResponse>(www.downloadHandler.text);
                sessionId = jsonResponse.session_id;
            }
        }
    }

    public void CaptureContent() {
        CameraFootage cameraFootage = FindAnyObjectByType<CameraFootage>();

        Texture2D texture = new Texture2D(cameraFootage.rawImage.texture.width, cameraFootage.rawImage.texture.height);
        texture.SetPixels(cameraFootage.webcamTexture.GetPixels());
        texture.Apply();

        byte[] imageBytes = ImageConversion.EncodeToPNG(texture);
        string base64String = Convert.ToBase64String(imageBytes);

        cameraFootage.DisableCamera();

        StartCoroutine(Upload(base64String));
    }

    IEnumerator Upload(string image) {
        using (UnityWebRequest www = UnityWebRequest.Post("https://my-service-894665829957.us-central1.run.app/get_ingredients",
                                                          $"{{\"session_id\": {sessionId}, \"image\": {image}}}", "application/json"))
        {
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError(www.error);
            }
            else
            {
                Debug.Log(www.downloadHandler.text);
            }
        }
    }
}
