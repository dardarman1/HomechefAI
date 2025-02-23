using System;
using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

public class Capture : MonoBehaviour
{
    public void CaptureContent() {
        CameraFootage cameraFootage = FindAnyObjectByType<CameraFootage>();

        Texture2D texture = new Texture2D(cameraFootage.rawImage.texture.width, cameraFootage.rawImage.texture.height);
        texture.SetPixels(cameraFootage.webcamTexture.GetPixels());
        texture.Apply();

        byte[] imageBytes = ImageConversion.EncodeToPNG(texture);
        string base64String = Convert.ToBase64String(imageBytes);

        cameraFootage.DisableCamera();
    }

    // IEnumerator Upload(string image) {
    //     string api_key = 

    //     using (UnityWebRequest www = UnityWebRequest.Post($"https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key={api_key}",
    //                                                       $"{{ \"image\": {image}}}", "application/json"))
    //     {
    //         yield return www.SendWebRequest();

    //         if (www.result != UnityWebRequest.Result.Success)
    //         {
    //             Debug.LogError(www.error);
    //         }
    //         else
    //         {
    //             Debug.Log("Form upload complete!");
    //         }
    //     }
    // }
}
